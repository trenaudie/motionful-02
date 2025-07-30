"""

Create a streamlit streaming animation, showing the results of a simple query to the antropic api 

use the cache control parameter just like here
class ConversationHistory:
    def __init__(self):
        # Initialize an empty list to store conversation turns
        self.turns = []

    def add_turn_assistant(self, content):
        # Add an assistant's turn to the conversation history
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
        # Add a user's turn to the conversation history
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
        # Retrieve conversation turns with specific formatting
        result = []
        user_turns_processed = 0
        # Iterate through turns in reverse order
        for turn in reversed(self.turns):
            if turn["role"] == "user" and user_turns_processed < 1:
                # Add the last user turn with ephemeral cache control
                result.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": turn["content"][0]["text"],
                            "cache_control": {"type": "ephemeral"}
                        }
                    ]
                })
                user_turns_processed += 1
            else:
                # Add other turns as they are
                result.append(turn)
        # Return the turns in the original order
        return list(reversed(result))

# Initialize the conversation history
conversation_history = ConversationHistory()

# System message containing the book content
# Note: 'book_content' should be defined elsewhere in the code
system_message = f"<file_contents> {book_content} </file_contents>"

# Predefined questions for our simulation
questions = [
    "What is the title of this novel?",
    "Who are Mr. and Mrs. Bennet?",
    "What is Netherfield Park?",
    "What is the main theme of this novel?"
]

def simulate_conversation():
    for i, question in enumerate(questions, 1):
        print(f"\nTurn {i}:")
        print(f"User: {question}")
        
        # Add user input to conversation history
        conversation_history.add_turn_user(question)

        # Record the start time for performance measurement
        start_time = time.time()

        # Make an API call to the assistant
        response = client.messages.create(
            model=MODEL_NAME,
            extra_headers={
              "anthropic-beta": "prompt-caching-2024-07-31"
            },
            max_tokens=300,
            system=[
                {"type": "text", "text": system_message, "cache_control": {"type": "ephemeral"}},
            ],
            messages=conversation_history.get_turns(),
        )

        # Record the end time
        end_time = time.time()

        # Extract the assistant's reply
        assistant_reply = response.content[0].text
        print(f"Assistant: {assistant_reply}")

        # Print token usage information
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        input_tokens_cache_read = getattr(response.usage, 'cache_read_input_tokens', '---')
        input_tokens_cache_create = getattr(response.usage, 'cache_creation_input_tokens', '---')
        print(f"User input tokens: {input_tokens}")
        print(f"Output tokens: {output_tokens}")
        print(f"Input tokens (cache read): {input_tokens_cache_read}")
        print(f"Input tokens (cache write): {input_tokens_cache_create}")

        # Calculate and print the elapsed time
        elapsed_time = end_time - start_time

        # Calculate the percentage of input prompt cached
        total_input_tokens = input_tokens + (int(input_tokens_cache_read) if input_tokens_cache_read != '---' else 0)
        percentage_cached = (int(input_tokens_cache_read) / total_input_tokens * 100 if input_tokens_cache_read != '---' and total_input_tokens > 0 else 0)

        print(f"{percentage_cached:.1f}% of input prompt cached ({total_input_tokens} tokens)")
        print(f"Time taken: {elapsed_time:.2f} seconds")

        # Add assistant's reply to conversation history
        conversation_history.add_turn_assistant(assistant_reply)

# Run the simulated conversation
simulate_conversation()



use st.write_stream to perform the streaming animation in Streamlit
Streamlit Version
Version 1.47.0
Stream a generator, iterable, or stream-like sequence to the app.
st.write_stream iterates through the given sequences and writes all chunks to the app. String chunks will be written using a typewriter effect. Other data types will be written using st.write.


import anthropic
client = anthropic.Anthropic()
with client.messages.stream(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
    model="claude-3-5-haiku-20241022",
) as stream:
  for text in stream.text_stream:
      print(text, end="", flush=True)
"""

#%% 
great_work_pgraham = """
July 2023
If you collected lists of techniques for doing great work in a lot of different fields, what would the intersection look like? I decided to find out by making it.
Partly my goal was to create a guide that could be used by someone working in any field. But I was also curious about the shape of the intersection. And one thing this exercise shows is that it does have a definite shape; it's not just a point labelled "work hard."
The following recipe assumes you're very ambitious.
The first step is to decide what to work on. The work you choose needs to have three qualities: it has to be something you have a natural aptitude for, that you have a deep interest in, and that offers scope to do great work.
"""
import streamlit as st
import anthropic
client = anthropic.Anthropic()
import time
st.header("Streaming Animation with Anthropic API")
if st.button("Stream data"):
    with st.spinner("Streaming..."):
        stream_data = []
        with client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": f"Hello can you repeat back to me this paragraph, five times exactly : \nparagraph: {great_work_pgraham}"}],
            # model="claude-3-5-haiku-20241022",
            model = "claude-3-7-sonnet-20250219"
        ) as stream:
            for text in stream.text_stream:
                stream_data.append(text)
                st.write_stream([text])
# %%
