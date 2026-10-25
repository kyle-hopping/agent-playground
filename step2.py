from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
messages = []


while True:
    user_input = input("User: ")
    if user_input.strip().lower() in ("exit", "quit"):
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model = "gpt-5-mini",
        messages = messages
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    print("Bot: ", reply)

    # Usually will have a max context window (tokens) for the model, so
    # eventually you will need to trim the messages list to fit within the
    # model's context window. Compaction!
