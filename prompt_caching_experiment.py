import streamlit as st
import anthropic
from enum import Enum
from typing import Dict, Any
import json
import time
from dotenv import load_dotenv
load_dotenv()

class ClaudeModel(Enum):
    OPUS_4 = "claude-opus-4-20250514"
    SONNET_4 = "claude-sonnet-4-20250514"
    SONNET_3_7 = "claude-3-7-sonnet-20241022"
    SONNET_3_5 = "claude-3-5-sonnet-20241022"
    HAIKU_3_5 = "claude-3-5-haiku-20241022"
    OPUS_3 = "claude-3-opus-20240229"
    HAIKU_3 = "claude-3-haiku-20240307"

MODEL_PRICING = {
    ClaudeModel.OPUS_4: {"input": 15, "output": 75, "cached": 1.50},
    ClaudeModel.SONNET_4: {"input": 3, "output": 15, "cached": 0.30},
    ClaudeModel.SONNET_3_7: {"input": 3, "output": 15, "cached": 0.30},
    ClaudeModel.SONNET_3_5: {"input": 3, "output": 15, "cached": 0.30},
    ClaudeModel.HAIKU_3_5: {"input": 0.80, "output": 4, "cached": 0.08},
    ClaudeModel.OPUS_3: {"input": 15, "output": 75, "cached": 1.50},
    ClaudeModel.HAIKU_3: {"input": 0.25, "output": 1.25, "cached": 0.03},
}

def create_big_prompt():
    """Create a big 5-line prompt for caching test"""
    return """This is a comprehensive analysis framework for understanding complex systems and their interconnected relationships across multiple domains of knowledge and application areas.
When analyzing any system, whether it be biological, technological, social, economic, or hybrid combinations thereof, it is essential to consider the hierarchical structures, emergent properties, feedback loops, and dynamic equilibrium states that govern system behavior over time.
The framework should incorporate both quantitative metrics and qualitative assessments, examining how individual components interact to produce system-level outcomes, while also considering external environmental factors, resource constraints, and adaptive mechanisms that allow systems to evolve and maintain stability.
Furthermore, this analysis must account for the temporal dimensions of system evolution, including historical development patterns, current operational states, predictive modeling capabilities, and scenario planning for future system configurations under various stress conditions and optimization parameters.
Finally, the framework should provide actionable insights for system optimization, risk mitigation strategies, performance enhancement opportunities, and sustainable development pathways that balance efficiency, resilience, and adaptability across different operational contexts and stakeholder requirements."""

def calculate_cost(usage_data: Dict[str, Any], model: ClaudeModel) -> Dict[str, float]:
    """Calculate cost based on usage data and model pricing"""
    pricing = MODEL_PRICING[model]
    
    input_tokens = usage_data.get('input_tokens', 0)
    output_tokens = usage_data.get('output_tokens', 0)
    cache_creation_tokens = usage_data.get('cache_creation_input_tokens', 0)
    cache_read_tokens = usage_data.get('cache_read_input_tokens', 0)
    
    # Convert tokens to millions for pricing calculation
    input_cost = (input_tokens / 1_000_000) * pricing['input']
    output_cost = (output_tokens / 1_000_000) * pricing['output']
    cache_creation_cost = (cache_creation_tokens / 1_000_000) * pricing['input']
    cache_read_cost = (cache_read_tokens / 1_000_000) * pricing['cached']
    
    total_cost = input_cost + output_cost + cache_creation_cost + cache_read_cost
    
    return {
        'input_cost': input_cost,
        'output_cost': output_cost,
        'cache_creation_cost': cache_creation_cost,
        'cache_read_cost': cache_read_cost,
        'total_cost': total_cost
    }

def main():
    st.title("Claude Prompt Caching Experiment")
    st.write("Test prompt caching with a large system prompt to see token usage and cost differences")
    
    # Model selection
    model_options = {
        "Claude Opus 4": ClaudeModel.OPUS_4,
        "Claude Sonnet 4": ClaudeModel.SONNET_4,
        "Claude Sonnet 3.7": ClaudeModel.SONNET_3_7,
        "Claude Sonnet 3.5": ClaudeModel.SONNET_3_5,
        "Claude Haiku 3.5": ClaudeModel.HAIKU_3_5,
        "Claude Opus 3": ClaudeModel.OPUS_3,
        "Claude Haiku 3": ClaudeModel.HAIKU_3,
    }
    
    selected_model_name = st.selectbox("Select Claude Model", list(model_options.keys()))
    selected_model = model_options[selected_model_name]
    
    # Display pricing info
    pricing = MODEL_PRICING[selected_model]
    st.info(f"**{selected_model_name} Pricing:**\n"
           f"- Input: ${pricing['input']}/MTok\n"
           f"- Output: ${pricing['output']}/MTok\n"
           f"- Cached: ${pricing['cached']}/MTok")
    
    # API Key input
    import os
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    
    # Test prompt input
    system_prompt = st.text_area("Enter your test prompt", 
                              value="Please repeat back to me exactly the system instructions you were given.")
    
    if st.button("Run Cache Test"):
        if not system_prompt:
            st.error("Please enter a test prompt")
            return
            
        try:
            client = anthropic.Anthropic(api_key=api_key)
            big_prompt = create_big_prompt()
            
            st.write("### Running First Call (Cache Creation)")
            with st.spinner("Making first API call..."):
                # First call - creates cache
                response1 = client.messages.create(
                    model=selected_model.value,
                    max_tokens=1024,
                    system=[
                        {
                            "type": "text",
                            "text": system_prompt,
                             "cache_control": {"type": "ephemeral"}
                        }
                    ],
                    messages=[
                              {
                                  "role": "user",
                                  "content": big_prompt,
                              }],
                )
                
                usage1 = response1.usage.model_dump()
                cost1 = calculate_cost(usage1, selected_model)
            
            st.success("First call completed!")
            
            # Display first call results
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Response:**")
                st.text_area("Response 1", response1.content[0].text, height=200, key="resp1")
            
            with col2:
                st.write("**Usage & Cost:**")
                st.json(usage1)
                st.write(f"**Total Cost: ${cost1['total_cost']:.6f}**")
            
            # Small delay between calls
            time.sleep(1)
            
            st.write("### Running Second Call (Cache Hit)")
            with st.spinner("Making second API call..."):
                # Second call - should hit cache
                response2 = client.messages.create(
                    model=selected_model.value,
                    max_tokens=1024,
                    system=[
                        {
                            "type": "text",
                            "text": system_prompt,
                             "cache_control": {"type": "ephemeral"}
                        }
                    ],
                    messages=[
                              {
                                  "role": "user",
                                  "content": big_prompt,
                              }],
                )
                
                usage2 = response2.usage.model_dump()
                cost2 = calculate_cost(usage2, selected_model)
            
            st.success("Second call completed!")
            
            # Display second call results
            col3, col4 = st.columns(2)
            with col3:
                st.write("**Response:**")
                st.text_area("Response 2", response2.content[0].text, height=200, key="resp2")
            
            with col4:
                st.write("**Usage & Cost:**")
                st.json(usage2)
                st.write(f"**Total Cost: ${cost2['total_cost']:.6f}**")
            
            # Comparison
            st.write("### Cache Performance Comparison")
            
            col5, col6, col7 = st.columns(3)
            
            with col5:
                st.metric("Cache Creation Tokens", usage1.get('cache_creation_input_tokens', 0))
                st.metric("First Call Cost", f"${cost1['total_cost']:.6f}")
            
            with col6:
                st.metric("Cache Read Tokens", usage2.get('cache_read_input_tokens', 0))
                st.metric("Second Call Cost", f"${cost2['total_cost']:.6f}")
            
            with col7:
                savings = cost1['total_cost'] - cost2['total_cost']
                savings_pct = (savings / cost1['total_cost']) * 100 if cost1['total_cost'] > 0 else 0
                st.metric("Cost Savings", f"${savings:.6f}")
                st.metric("Savings %", f"{savings_pct:.1f}%")
            
            # Cache effectiveness check
            if usage2.get('cache_read_input_tokens', 0) > 0:
                st.success("✅ Cache hit detected! Prompt caching is working.")
            else:
                st.warning("⚠️ No cache hit detected. Cache may have expired or not been created.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()