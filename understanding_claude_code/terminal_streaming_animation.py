"""
Terminal streaming animation showing results of a simple query to the Anthropic API
Uses streaming to display text with typewriter effect in the terminal
"""

import anthropic
import time
import sys
import requests
from bs4 import BeautifulSoup

try:
    response = requests.get("https://www.paulgraham.com/greatwork.html")
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text content from the HTML
    for script in soup(["script", "style"]):
        script.extract()
    great_work_pgraham = soup.get_text()
    
    # Clean up the text
    lines = (line.strip() for line in great_work_pgraham.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    great_work_pgraham = '\n'.join(chunk for chunk in chunks if chunk)
    
    print("✅ Successfully fetched Paul Graham's 'Great Work' essay")
    print(f"📄 Content length: {len(great_work_pgraham)} characters")
    
except requests.RequestException as e:
    print(f"❌ Error fetching content: {e}")
    # Fallback content
    great_work_pgraham = """
July 2023
If you collected lists of techniques for doing great work in a lot of different fields, what would the intersection look like? I decided to find out by making it.
Partly my goal was to create a guide that could be used by someone working in any field. But I was also curious about the shape of the intersection. And one thing this exercise shows is that it does have a definite shape; it's not just a point labelled "work hard."
The following recipe assumes you're very ambitious.
The first step is to decide what to work on. The work you choose needs to have three qualities: it has to be something you have a natural aptitude for, that you have a deep interest in, and that offers scope to do great work.
"""
    print("🔄 Using fallback content")


class ConversationHistory:
    def __init__(self):
        self.turns = []

    def add_turn_assistant(self, content):
        self.turns.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": content
                }
            ]
        })

    def add_turn_user(self, content):
        self.turns.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": content
                }
            ]
        })

    def get_turns(self):
        result = []
        user_turns_processed = 0
        for turn in reversed(self.turns):
            if turn["role"] == "user" and user_turns_processed < 1:
                result.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": turn["content"][0]["text"],
                            # "cache_control": {"type": "ephemeral"}
                        }
                    ]
                })
                user_turns_processed += 1
            else:
                result.append(turn)
        return list(reversed(result))

def stream_terminal_animation():
    client = anthropic.Anthropic()
    conversation_history = ConversationHistory()
    
    system_message = f"<file_contents> {great_work_pgraham} </file_contents>"
    
    questions = [
        "What is the main theme of this text?",
        "What are the three qualities mentioned for choosing work?",
        "Summarize the key points in 2-3 sentences."
    ]
    
    print("🚀 Terminal Streaming Animation with Anthropic API")
    print("=" * 50)
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Turn {i}:")
        print(f"User: {question}")
        print(f"Assistant: ", end="", flush=True)
        
        conversation_history.add_turn_user(question)
        
        start_time = time.time()
        full_response = ""
        
        try:
            with client.messages.stream(
                model="claude-3-5-haiku-20241022",
                extra_headers={
                    "anthropic-beta": "prompt-caching-2024-07-31"
                },
                max_tokens=300,
                system=[
                    {"type": "text", "text": system_message, 
                     "cache_control": {"type": "ephemeral"}
                     },
                ],
                messages=conversation_history.get_turns(),
            ) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)
                    full_response += text
                    time.sleep(0.01)  # Small delay for visual effect
            
            print()  # New line after streaming
            
            # Get final message for token usage
            final_message = stream.get_final_message()
            end_time = time.time()
            
            # Print performance metrics
            input_tokens = final_message.usage.input_tokens
            output_tokens = final_message.usage.output_tokens
            input_tokens_cache_read = getattr(final_message.usage, 'cache_read_input_tokens', 0)
            input_tokens_cache_create = getattr(final_message.usage, 'cache_creation_input_tokens', 0)
            
            elapsed_time = end_time - start_time
            total_input_tokens = input_tokens + input_tokens_cache_read
            percentage_cached = (input_tokens_cache_read / total_input_tokens * 100 if total_input_tokens > 0 else 0)
            
            print(f"\n📊 Metrics:")
            print(f"   • Input tokens: {input_tokens}")
            print(f"   • Output tokens: {output_tokens}")
            print(f"   • Cache read tokens: {input_tokens_cache_read}")
            print(f"   • Cache write tokens: {input_tokens_cache_create}")
            print(f"   • {percentage_cached:.1f}% of input cached ({total_input_tokens} tokens)")
            print(f"   • Time taken: {elapsed_time:.2f} seconds")
            
            conversation_history.add_turn_assistant(full_response)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            break
        
        time.sleep(1)  # Pause between questions

if __name__ == "__main__":
    stream_terminal_animation()