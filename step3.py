import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"File {path} not found!"


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file at the given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to read."
                    }
                },
                "required": ["path"]
            }
        }
    }
]

messages = [
    {"role": "user", "content": "What is inside notes.txt? Summarize it in one line."}
]

while True:
    response = client.chat.completions.create(
            model = "gpt-5-mini",
            messages = messages,
            tools = TOOL_SCHEMAS
        )
    message = response.choices[0].message
    messages.append(message)

    # If no tool is called, it means the model is done and gave us a final answer
    if not message.tool_calls:
        print(message.content)
        break

    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        print(f"Tool call: {tool_call.function.name} with arguments {args}")

        result = read_file(**args)

        messages.append(
            {"role": "tool", "tool_call_id": tool_call.id, "content": result}
        )
