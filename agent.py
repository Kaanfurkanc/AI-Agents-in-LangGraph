import openai
import re
import httpx
import os
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv())

from openai import OpenAI

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello, who are you?"},
    ],
)

print(chat_completion.choices[0].message.content)