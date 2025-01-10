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

class Agent:
    def __init__(self, system="") :
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        response = self.execute()
        self.messages.append({"role": "assistant", "content": response})
        return response
    
    def execute(self):
        completion = client.chat.completions.create(
            model="gpt-4-0125-preview",
            temperature=0,
            messages=self.messages,
        )
        return completion.choices[0].message.content

#ReACT Pattern
prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:

Answer: A bulldog weights 51 lbs
""".strip()