import httpx

from app.core.config import TELEGRAM_BOT_TOKEN


class TelegramClient:

    BASE_URL = (
        "https://api.telegram.org/bot"
    )

    def __init__(
        self,
        token: str | None = None,
    ):
        self.token = (
            token
            or TELEGRAM_BOT_TOKEN
        )

        if not self.token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN não configurado."
            )

    def send_message(
        self,
        chat_id: str,
        text: str,
    ):

        response = httpx.post(
            f"{self.BASE_URL}"
            f"{self.token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": False,
            },
            timeout=20,
        )

        response.raise_for_status()

        return response.json()