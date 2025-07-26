import json
import os

def parse_jsonl_and_extract_tool_calls(input_file_path, output_file_path):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Open the input JSONL file and the output file
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            try:
                # Parse each line as a JSON object
                data = json.loads(line)
                print(f"Processing line: {data}")  # Debugging output

                # Extract tool calls (assuming they are under the 'tools' key)
                if 'tools' in data:
                    tools = data['tools']
                    for tool in tools:
                        # Write each tool call definition to the output file
                        json.dump(tool, output_file)
                        output_file.write('\n')  # Add a newline after each JSON object
                        return 
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON from line: {e}")

# Example usage
input_file_path = '/home/bits/motionful-02/logs/motionful-02_2025-07-26-09-02-06_d57622f3.jsonl'
output_file_path = '/home/bits/motionful-02/logs_important/tool_calls.jsonl'
parse_jsonl_and_extract_tool_calls(input_file_path, output_file_path)
