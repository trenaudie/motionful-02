#!/usr/bin/env python3
"""
Extract tool calls from Claude Code JSON logs and convert to JSONL format.

This script reads the request_to_claude_code.json file, extracts all tool_use
objects from assistant messages, and writes them to tool_calls.jsonl in JSONL format.
"""

import json
import sys
from pathlib import Path


def extract_tool_calls(json_data):
    """
    Extract tool_use objects from the Claude Code JSON data.
    
    Args:
        json_data (dict): The parsed JSON data from request_to_claude_code.json
        
    Returns:
        list: List of tool_use objects
    """
    tool_calls = []
    
    # Navigate to the messages in the request body
    try:
        messages = json_data["request"]["body"]["messages"]
        
        for message in messages:
            # Only process assistant messages
            if message.get("role") == "assistant":
                content = message.get("content", [])
                
                # Look for tool_use objects in the content
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "tool_use":
                        tool_calls.append(item)
                        
    except KeyError as e:
        print(f"Error: Could not find expected structure in JSON: {e}", file=sys.stderr)
        return []
    
    return tool_calls


def extract_tool_definitions(json_data):
    """
    Extract tool definitions from the Claude Code JSON data.
    
    Args:
        json_data (dict): The parsed JSON data from request_to_claude_code.json
        
    Returns:
        list: List of tool definition objects
    """
    tool_definitions = []
    
    # Navigate to the tools array in the request body
    try:
        tools = json_data["request"]["body"]["tools"]
        
        for tool in tools:
            if isinstance(tool, dict):
                tool_definitions.append(tool)
                        
    except KeyError as e:
        print(f"Error: Could not find tools array in JSON: {e}", file=sys.stderr)
        return []
    
    return tool_definitions


def write_jsonl(tool_calls, output_file):
    """
    Write tool calls to JSONL format.
    
    Args:
        tool_calls (list): List of tool_use objects
        output_file (str): Path to output JSONL file
    """
    with open(output_file, 'w') as f:
        for tool_call in tool_calls:
            f.write(json.dumps(tool_call) + '\n')


def main():
    """Main function to process the JSON file and extract tool calls and definitions."""
    
    # Set up file paths
    script_dir = Path(__file__).parent
    input_file = script_dir / "request_to_claude_code.json"
    tool_calls_output = script_dir / "tool_calls.jsonl"
    tool_definitions_output = script_dir / "tool_definitions.jsonl"
    
    try:
        # Read the input JSON file
        print(f"Reading {input_file}...")
        with open(input_file, 'r') as f:
            json_data = json.load(f)
        
        # Extract tool calls
        print("Extracting tool calls...")
        tool_calls = extract_tool_calls(json_data)
        
        if tool_calls:
            print(f"Found {len(tool_calls)} tool calls")
            print(f"Writing tool calls to {tool_calls_output}...")
            write_jsonl(tool_calls, tool_calls_output)
            print(f"Successfully extracted {len(tool_calls)} tool calls to {tool_calls_output}")
            
            # Print summary of tools used
            tools_used = {}
            for tool_call in tool_calls:
                tool_name = tool_call.get("name", "unknown")
                tools_used[tool_name] = tools_used.get(tool_name, 0) + 1
                
            print("\nTools used:")
            for tool_name, count in sorted(tools_used.items()):
                print(f"  {tool_name}: {count}")
        else:
            print("No tool calls found in the JSON data.")
        
        # Extract tool definitions
        print("\nExtracting tool definitions...")
        tool_definitions = extract_tool_definitions(json_data)
        
        if tool_definitions:
            print(f"Found {len(tool_definitions)} tool definitions")
            print(f"Writing tool definitions to {tool_definitions_output}...")
            write_jsonl(tool_definitions, tool_definitions_output)
            print(f"Successfully extracted {len(tool_definitions)} tool definitions to {tool_definitions_output}")
            
            # Print summary of tool definitions
            print("\nTool definitions available:")
            for tool_def in tool_definitions:
                tool_name = tool_def.get("name", "unknown")
                description = tool_def.get("description", "No description")[:80] + "..." if len(tool_def.get("description", "")) > 80 else tool_def.get("description", "No description")
                print(f"  {tool_name}: {description}")
        else:
            print("No tool definitions found in the JSON data.")
            
    except FileNotFoundError:
        print(f"Error: Could not find input file {input_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()