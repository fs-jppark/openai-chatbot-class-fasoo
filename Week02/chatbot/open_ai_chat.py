import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(
    dotenv_path="./env/.env",  # .env 경로를 절대 경로 또는 상대경로로 입력합니다.
    verbose=True)
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

# 아래 함수를 채워 보세요.
def chat(
        messages,
        temperature=1,
        top_p=1,
        model="gpt-4-vision-preview",
):

    completions_response = client.chat.completions.create (
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p
    )
    logging.info(f"completions_response: {completions_response}")

    return completions_response.choices.pop().message.content