import os

from dotenv import load_dotenv

from app.services.publishers.telegram.client import TelegramClient

load_dotenv()

chat_ids = [
    chat_id.strip()
    for chat_id in os.getenv("TELEGRAM_CHAT_IDS", "").split(",")
    if chat_id.strip()
]

if not chat_ids:
    raise RuntimeError("TELEGRAM_CHAT_IDS não configurado.")

client = TelegramClient()

for chat_id in chat_ids:
    result = client.send_message(
        chat_id,
        "🧪 TESTE — Central de Ofertas ML\n\n"
        "O bot conseguiu publicar automaticamente neste canal."
    )

    print(f"Enviado para {chat_id}: {result['ok']}")