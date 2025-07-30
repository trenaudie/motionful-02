import anthropic
import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, Union
from typing import List
from datetime import datetime
from provider_models import AnthropicModel, CLAUDE_HAIKU_35


def fetch_essay(url: str = "https://www.paulgraham.com/greatwork.html"):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text content from the HTML
        for script in soup(["script", "style"]):
            script.extract()
        great_work_pgraham = soup.get_text()

        # Clean up the text
        lines = (line.strip() for line in great_work_pgraham.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        great_work_pgraham = "\n".join(chunk for chunk in chunks if chunk)

        print("✅ Successfully fetched Paul Graham's 'Great Work' essay")
        print(f"📄 Content length: {len(great_work_pgraham)} characters")

    except requests.RequestException as e:
        print(f"❌ Error fetching content: {e}")
        # Fallback content
        great_work_pgraham = """
        How to Do Great Work
        July 2023
        If you collected lists of techniques for doing great work in a lot of different fields, what would the intersection look like? I decided to find out by making it.
        Partly my goal was to create a guide that could be used by someone working in any field. But I was also curious about the shape of the intersection. And one thing this exercise shows is that it does have a definite shape; it's not just a point labelled "work hard."
        The following recipe assumes you're very ambitious.
        The first step is to decide what to work on. The work you choose needs to have three qualities: it has to be something you have a natural aptitude for, that you have a deep interest in, and that offers scope to do great work.
        In practice you don't have to worry much about the third criterion. Ambitious people are if anything already too conservative about it. So all you need to do is find something you have an aptitude for and great interest in. [1]
        That sounds straightforward, but it's often quite difficult. When you're young you don't know what you're good at or what different kinds of work are like. Some kinds of work you end up doing may not even exist yet. So while some people know what they want to do at 14, most have to figure it out.
        The way to figure out what to work on is by working. If you're not sure what to work on, guess. But pick something and get going. You'll probably guess wrong some of the time, but that's fine. It's good to know about multiple things; some of the biggest discoveries come from noticing connections between different fields.
        """
    return great_work_pgraham
import uuid 

class ConversationHistory:
    def __init__(self):
        self.turns = []

    def add_turn_assistant(self, content, msg_id:str):
        self.turns.append(
            {"role": "assistant", "content": [{"type": "text", "text": content}],
             "id": msg_id,  # Add an ID for tracking
             "timestamp": datetime.now()}  # Add a timestamp for tracking
        )

    def add_turn_user(self, content, msg_id:str):
        self.turns.append(
            {"role": "user", "content": [{"type": "text", "text": content}],
             "id": msg_id,  # Add an ID for tracking
             "timestamp" : datetime.now()}  # Add a timestamp for tracking
        )

    def get_turns(self, add_cache_control: bool = True):
        result = []
        user_turns_processed = 0
        for turn in reversed(self.turns):
            if turn["role"] == "user" and user_turns_processed < 1:
                message_content = {
                    "type": "text",
                    "text": turn["content"][0]["text"]
                }
                if add_cache_control:
                    message_content["cache_control"] = {"type": "ephemeral"}
                result.append({"role": "user", "content": [message_content],
                               "id": turn["id"],
                               "timestamp": turn["timestamp"]})
                user_turns_processed += 1
            else:
                result.append(turn)
        return list(reversed(result))
    def get_turns_before(self, timestamp: datetime, include:bool = True):
        result = []
        for turn in self.turns:
            if turn["timestamp"] < timestamp:
                result.append(turn)
            elif include and turn["timestamp"] == timestamp:
                result.append(turn)
        return result   


class ProfilerDataPoint:
    def __init__(self, chunk, timestamp, input_tokens, input_tokens_cache_read):
        self.chunk: str = chunk
        self.timestamp: datetime = timestamp

    @property
    def num_tokens(self):
        # TODO! NotImplemented
        return count_tokens(self.chunk)


class ProfilerStreaming:
    def __init__(self):
        self.start = None
        self.data_points: List[ProfilerDataPoint]
        self.system_message: str = None

    def cumulative_tokens_received_per_second(self):
        tokens_received = list([0])
        time_elapsed_list = list([self.start])
        for dpoint in self.data_points:
            tokens_received += [tokens_received[-1] + dpoint.num_tokens]
            time_elapsed_list += [dpoint.timestamp]

    def cumulative_cost_per_second(self, cache_used: bool, model: AnthropicModel):
        # graph with cumulative cost as a function of time elapsed
        from provider_models import (
            price_anthropic_call_with_input_caching,
            price_anthropic_call_no_caching,
        )

        prices_dpoints = list([0.0])
        time_elapsed_list = list([self.start])
        for dpoint in self.data_points:
            tokens_received = tokens_received + dpoint.num_tokens
            # lets consider that the tokens inputted are all cache read tokens in the case of streaming using cache.
            if cache_used:
                prices_dpoints += [
                    price_anthropic_call_with_input_caching(
                        model=model,
                        output_tokens=tokens_received,
                        system_message_str=self.system_message,
                        messages=self.messages
                    )
                ]
            time_elapsed_list += [dpoint.timestamp]


def run_double_message(
    system_prompt: str,
    user_query: str,
    model: AnthropicModel = CLAUDE_HAIKU_35,
    add_cache_control: bool = False,
):
    """
    - system :str. eg. the whole paul graham essay
    - user_query :str. eg. the question to ask about the essay. We will ask for a deterministic answer, if possible, so something like "Repeat back to me please!"
    """
    client = anthropic.Anthropic()
    conversation_history = ConversationHistory()

    system_message = f"<file_contents> {system_prompt} </file_contents>"

    questions = [
        "What is the main theme of this text?",
        "What are the three qualities mentioned for choosing work?",
        "Summarize the key points in 2-3 sentences.",
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
        system_message: str = "This is a system message."
        # Explicitly define the type for system_message_dict

        system_message_dict: Dict[str, Union[str, Dict[str, str]]] = {
            "type": "text",
            "text": system_message,
        }

        with client.messages.stream(
            model=model.name,
            extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
            max_tokens=300,
            system=[system_message_dict],
            messages=conversation_history.get_turns(add_cache_control),
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text
                time.sleep(0.01)  # Small delay for visual effect
        print()  # New line after streaming

        final_message = stream.get_final_message()
        end_time = time.time()
