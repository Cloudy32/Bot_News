import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    db_path: str


def load_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise ValueError(
            "Bot token is empty. Set BOT_TOKEN (or TELEGRAM_BOT_TOKEN) in .env file."
        )

    db_path = os.getenv("DB_PATH", "news.db").strip() or "news.db"
    return Settings(bot_token=bot_token, db_path=db_path)
