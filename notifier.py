import html
import logging
import os

import requests

log = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, token: str | None = None, chat_id: str | None = None):
        self.token = token or os.environ["TELEGRAM_TOKEN"]
        self.chat_id = chat_id or os.environ["TELEGRAM_CHAT_ID"]

    def send(self, text: str) -> None:
        resp = requests.post(
            f"https://api.telegram.org/bot{self.token}/sendMessage",
            json={
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=15,
        )
        if not resp.ok:
            log.error("Telegram error: %s", resp.text)

    def send_job(self, job) -> None:
        esc = html.escape
        self.send(
            f"<b>{esc(job.title)}</b>\n"
            f"{esc(job.company)} · {esc(job.location)}\n"
            f"<i>{esc(job.source)}</i>\n"
            f'<a href="{esc(job.url, quote=True)}">Apply / View</a>'
        )
