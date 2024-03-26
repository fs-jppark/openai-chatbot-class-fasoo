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
        model="gpt-3.5-turbo-1106",
):
    pass