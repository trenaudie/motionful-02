from dataclasses import dataclass
from typing import Optional
import anthropic

@dataclass
class AnthropicModel:
    """Base class for Anthropic Claude models with pricing information."""
    name: str
    description: str
    input_price_per_mtok: float  # Price per million tokens for input
    output_price_per_mtok: float  # Price per million tokens for output
    prompt_caching_write_price_per_mtok: float  # Price per million tokens for prompt caching write
    prompt_caching_read_price_per_mtok: float  # Price per million tokens for prompt caching read


@dataclass
class ClaudeOpus4(AnthropicModel):
    """Claude Opus 4 - Most intelligent model for complex tasks."""
    
    def __init__(self):
        super().__init__(
            name="claude-opus-4-20250514",
            description="Most intelligent model for complex tasks",
            input_price_per_mtok=15.0,
            output_price_per_mtok=75.0,
            prompt_caching_write_price_per_mtok=18.75,
            prompt_caching_read_price_per_mtok=1.50
        )


@dataclass
class ClaudeSonnet4(AnthropicModel):
    """Claude Sonnet 4 - Optimal balance of intelligence, cost, and speed."""
    
    def __init__(self):
        super().__init__(
            name="claude-sonnet-4-20250514",
            description="Optimal balance of intelligence, cost, and speed",
            input_price_per_mtok=3.0,
            output_price_per_mtok=15.0,
            prompt_caching_write_price_per_mtok=3.75,
            prompt_caching_read_price_per_mtok=0.30
        )


@dataclass
class ClaudeHaiku35(AnthropicModel):
    """Claude Haiku 3.5 - Fastest, most cost-effective model."""
    
    def __init__(self):
        super().__init__(
            name="claude-3-5-haiku-latest",
            description="Fastest, most cost-effective model",
            input_price_per_mtok=0.80,
            output_price_per_mtok=4.0,
            prompt_caching_write_price_per_mtok=1.0,
            prompt_caching_read_price_per_mtok=0.08
        )
@dataclass
class ClaudeSonnet37(AnthropicModel):
    """Claude Sonnet 3.7 - Fast, intelligent, cost-effective model."""
    
    def __init__(self):
        super().__init__(
            name="claude-3-7-sonnet-latest",
            description="Fastest, most cost-effective model",
            input_price_per_mtok=0.80,
            output_price_per_mtok=4.0,
            prompt_caching_write_price_per_mtok=1.0,
            prompt_caching_read_price_per_mtok=0.08
        )

# Model instances for easy access
CLAUDE_OPUS_4 = ClaudeOpus4()
CLAUDE_SONNET_4 = ClaudeSonnet4()
CLAUDE_HAIKU_35 = ClaudeHaiku35()

# List of all available models
ALL_MODELS = [CLAUDE_OPUS_4, CLAUDE_SONNET_4, CLAUDE_HAIKU_35]



def price_anthropic_call_no_caching(model:AnthropicModel, output_tokens:str, system_message_str:str, messages:list[dict]):
    input_tokens = anthropic.Anthropic().messages.count_tokens(
        model=model.name,
        system =[ {
                "type": "text",
                "text": system_message_str
            }],
        messages=messages
    )
    price_input = input_tokens * model.input_price_per_mtok / 1_000_000
    price_output = output_tokens * model.output_price_per_mtok / 1_000_000
    return price_input + price_output

def price_anthropic_call_with_input_caching(model:AnthropicModel, output_tokens:str, system_message_str:str, messages:list[dict]):
    # lets consider that the input tokens cache read are only the system message 
    input_tokens_cache_read = anthropic.Anthropic().messages.count_tokens(
        model=model.name,
        system=[{
            "type": "text",
            "text": system_message_str
        }],
        messages=[]
    )
    # lets consider that the input tokens no cache read are the messages
    input_tokens = anthropic.Anthropic().messages.count_tokens(
        model=model.name,
        messages=messages 
    )   
    price_input_cache_read = input_tokens_cache_read * model.prompt_caching_read_price_per_mtok / 1_000_000
    price_input_read = input_tokens * model.input_price_per_mtok / 1_000_000
    price_output = output_tokens * model.output_price_per_mtok / 1_000_000
    return price_input_cache_read + price_input_read + price_output