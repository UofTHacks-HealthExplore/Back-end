import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

restart_sequence = "\n"

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="The following is a list of companies and the categories they fall into:\n\nApple, Facebook, Fedex\n\nApple\nCategory:\n",
    temperature=0,
    max_tokens=6,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"]
)

print(response)
