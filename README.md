# agent-playground

A step-by-step walkthrough of building a simple AI coding agent with the OpenAI Python SDK. Each script builds on the previous one, starting with a single API call and ending with an interactive agent that can use tools.

> An AI agent is simply an LLM connected to tools in a loop.

## Files

| File | What it shows |
| --- | --- |
| `step1.py` | One chat completion call with a system, user and assistant message. Prints the model's reply. |
| `step2.py` | An interactive chat loop. The conversation history is kept in a `messages` list so the model remembers earlier turns. Type `exit` or `quit` to stop. |
| `step3.py` | Tool calling. The model gets one tool, `read_file`, and is asked to summarize `notes.txt`. The script loops until the model stops calling tools and gives a final answer. |
| `agent.py` | The full agent. An interactive terminal assistant with four tools: `list_files`, `read_file`, `write_file` and `run_command`. Shell commands ask for `y/n` confirmation before they run. |

## How the agent loop works

1. Send the conversation history and the tool schemas to the model.
2. If the reply contains tool calls, run each tool and append its result to the history as a `tool` message.
3. Repeat until the model replies without tool calls. That reply is the final answer.

## Setup

Requires Python 3.9+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv
```

Create a `.env` file in the project root with your API key:

```
OPENAI_API_KEY=sk-...
```

`.env` is listed in `.gitignore`, so the key is not committed.

## Usage

```bash
python step1.py
python step2.py
python step3.py
python agent.py
```

All scripts use the `gpt-5-mini` model.

## Safety note

`agent.py` can write files and run shell commands in the directory it is launched from. Commands always ask for confirmation first, but file writes do not. Run it in a folder you don't mind it changing.
