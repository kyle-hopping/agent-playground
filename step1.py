from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model = "gpt-5-mini",
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Answer concisely in short sentences."},
        {"role": "user", "content": "Explain what an AI agent is in one sentence."},
        # {"role": "assistant", "content": "An AI agent is simply an LLM connected to tools in a loop"}
    ]
)

print(response.choices[0].message.content)