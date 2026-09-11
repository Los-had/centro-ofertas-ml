import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")


# =========================
# DATABASE
# =========================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DATA_DIR / 'offers.db'}"
)


# =========================
# MERCADO LIVRE
# =========================

ML_SITE_ID = os.getenv("ML_SITE_ID", "MLB")

ML_CLIENT_ID = os.getenv("ML_CLIENT_ID")

ML_CLIENT_SECRET = os.getenv("ML_CLIENT_SECRET")

ML_ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")

ML_REFRESH_TOKEN = os.getenv("ML_REFRESH_TOKEN")


# =========================
# TELEGRAM
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

TELEGRAM_CHAT_IDS = os.getenv(
    "TELEGRAM_CHAT_IDS",
    ""
).split(",")


# =========================
# APPLICATION
# =========================

APP_NAME = "Central de Ofertas ML"

APP_VERSION = "0.1.0"