
Anthropic API Prompt Caching Benchmark Experiment

Objective

Create a benchmark script to measure and compare the performance of Anthropic's streaming API with and without
prompt caching, specifically analyzing the streaming characteristics for animated visualization.

Experiment Design

Two Test Scenarios:

1. Message 1 (Cache Write): First request that writes to cache
2. Message 2 (Cache Read): Identical request that reads from cache

Both messages must ask:

"Can you repeat back to me the first two paragraphs of the Paul Graham essay, word for word?"

Required Implementation

1. Setup Requirements

import anthropic
import time
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

2. Data Collection Structure

For each message, collect these metrics in real-time during streaming:

benchmark_data = {
    "message_1_cache_write": {
        "time_to_first_token": 0.0,
        "total_time": 0.0,
        "tokens_per_second": 0.0,
        "streaming_timeline": [
            {"time_elapsed": 0.1, "tokens_received": 5, "cost_so_far": 0.001},
            {"time_elapsed": 0.2, "tokens_received": 12, "cost_so_far": 0.002},
            # ... continue for each streaming chunk
        ],
        "final_metrics": {
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "total_cost_dollars": 0.0,
            "percentage_cached": 0.0
        }
    },
    "message_2_cache_read": {
        # Same structure as above
    }
}

3. Streaming Data Collection

During each streaming response, capture:
- Time elapsed from request start (in seconds with millisecond precision)
- Cumulative tokens received at each chunk
- Estimated cost so far based on tokens received
- Time to first token (when first chunk arrives)
- Inter-chunk timing (time between chunks)

4. Cost Calculation

Use these pricing rates for Claude Haiku 3.5:
- Base Input Tokens: $0.80 / MTok
- Cache Write Tokens: $1.00 / MTok
- Cache Read Tokens: $0.08 / MTok
- Output Tokens: $4.00 / MTok

5. Implementation Requirements

A. Paul Graham Essay Fetching

def fetch_paul_graham_essay():
    """Fetch and clean Paul Graham's 'Great Work' essay"""
    try:
        response = requests.get("https://www.paulgraham.com/greatwork.html")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Clean HTML and extract text
        # Return clean text
    except Exception as e:
        # Provide fallback content
        return fallback_content

B. Streaming Benchmark Function

def benchmark_streaming_request(client, system_message, user_message, is_cache_write=True):
    """
    Execute streaming request and collect real-time metrics
    
    Returns:
    - streaming_timeline: List of {time_elapsed, tokens_received, cost_so_far}
    - final_metrics: Complete token usage and cost breakdown
    - performance_metrics: TTFT, total_time, tokens_per_second
    """

    # Record start time with high precision
    start_time = time.perf_counter()

    # Track metrics during streaming
    streaming_timeline = []
    cumulative_tokens = 0
    first_token_time = None

    # Configure request with/without cache_control
    # Execute streaming request
    # Collect data for each chunk received
    # Calculate final metrics

    return streaming_timeline, final_metrics, performance_metrics

C. Main Benchmark Runner

def run_caching_benchmark():
    """Execute complete benchmark and save results"""

    # 1. Setup client and fetch essay
    # 2. Run Message 1 (cache write)
    # 3. Run Message 2 (cache read) 
    # 4. Calculate comparative metrics
    # 5. Save results to JSON file with timestamp
    # 6. Print summary comparison

6. Output Requirements

A. Real-time Console Output

🚀 Starting Prompt Caching Benchmark
📄 Essay content: 15,234 characters fetched

📝 Message 1 (Cache Write):
Assistant: [streaming text with timing info]
⏱️  TTFT: 0.234s | Total: 2.156s | 45.2 tok/s | Cost: $0.0234

📝 Message 2 (Cache Read):
Assistant: [streaming text with timing info]
⏱️  TTFT: 0.089s | Total: 1.891s | 52.1 tok/s | Cost: $0.0098

💰 Cost Savings: 58.2% | ⚡ Speed Improvement: 12.3%

B. JSON Output File

Save complete benchmark data to benchmark_results_YYYYMMDD_HHMMSS.json with:
- Complete streaming timelines for both messages
- All token usage breakdowns
- Cost calculations and comparisons
- Performance metrics and improvements
- Timestamp and configuration details

7. Key Implementation Details

Error Handling

- Network failures during essay fetching
- API errors or rate limits
- Streaming interruptions
- Invalid token counts

Precision Requirements

- Use time.perf_counter() for high-precision timing
- Record times to millisecond precision (3 decimal places)
- Ensure accurate token counting during streaming

Cache Configuration

- Message 1: Include "cache_control": {"type": "ephemeral"} on system message
- Message 2: Same system message without cache_control (should read from cache)
- Use identical messages to ensure valid comparison

8. Expected Output Analysis

The benchmark should clearly demonstrate:
- Cache write penalty: Message 1 slightly slower due to cache creation
- Cache read benefit: Message 2 faster TTFT and potentially higher throughput
- Cost savings: Significant reduction in input token costs for Message 2
- Streaming patterns: Different token delivery patterns between cached/uncached

9. Animation Data Preparation

Ensure the streaming timeline data is formatted for easy graphing:
# For plotting tokens over time
x_axis = [point["time_elapsed"] for point in streaming_timeline]
y_axis_tokens = [point["tokens_received"] for point in streaming_timeline]
y_axis_cost = [point["cost_so_far"] for point in streaming_timeline]

Implement this benchmark to provide comprehensive insights into Anthropic's prompt caching performance
characteristics with streaming responses.