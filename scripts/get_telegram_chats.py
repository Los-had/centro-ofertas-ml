import os

import httpx
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")

if not token:
    raise RuntimeError("TELEGRAM_BOT_TOKEN não configurado.")

url = f"https://api.telegram.org/bot{token}/getUpdates"

response = httpx.get(url, timeout=20)

print(response.status_code)
print(response.json())