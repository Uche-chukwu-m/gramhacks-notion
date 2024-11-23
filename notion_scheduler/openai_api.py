import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_schedule(user_input, previous_responses=[]):
    messages = [{"role": "user", "content": user_input}]
    for response in previous_responses:
        messages.append({"role": "assistant", "content": response})

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
    )
    return completion.choices[0].message["content"]
