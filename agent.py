import os, json, subprocess
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
MODEL = "gpt-5-mini"
SYSTEM_PROMPT = """You are a coding agent running inside the user's terminal.
You can list files, read files, write files, and run shell commands.
Use your tools to complete the user's requests, then summarize what you did.
The working directory is the folder the user launched this agent from."""

def list_files():
    entries = []
    for entry in os.scandir():
        entries.append(entry.name + ("/" if entry.is_dir() else ""))
    return "\n".join(sorted(entries)) or "(empty directory)"

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"File {path} not found!"

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Saved {path} ({len(content)} characters)"

def run_command(command):
    answer = input(f"Run command: {command} (y/n)? ")
    if answer.strip().lower() != "y":
        return "The user declined to run this command."
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=120
    )
    output = (result.stdout + result.stderr).strip()
    return output or f"(no output, exit code {result.returncode})"

TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List the files in the current directory.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file at the given path.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file at the given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command and return its output.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"]
            }
        }
    }
]

def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f"tool call: {name}({args})")
    try:
        return str(TOOLS[name](**args))
    except Exception as error:
        return f"Error: {error}"

def run_agent(messages):
    while True:
        response = client.chat.completions.create(
            model = MODEL,
            messages = messages,
            tools = TOOL_SCHEMAS
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            return message.content
        
        for tool_call in message.tool_calls:
            result = run_tool(tool_call)

            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            )

def main():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    print("Test agent is ready! Type 'exit' or 'quit' to shutdown.")

    while True:
        user_input = input("User: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        messages.append(
            {"role": "user", "content": user_input}
        )
        reply = run_agent(messages)
        print(f"\nAgent: {reply}")

if __name__ == "__main__":
    main()