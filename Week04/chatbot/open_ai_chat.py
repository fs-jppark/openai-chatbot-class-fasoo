import logging
import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))


# 아래 함수를 채워 보세요.
def chat(
        messages,
        temperature=1,
        top_p=1,
        model="gpt-3.5-turbo-1106",
):
    completions_response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p
    )
    logging.info(f"completions_response: {completions_response}")

    return completions_response.choices.pop().message.content
