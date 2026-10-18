import hashlib
import logging
import time
from dataclasses import dataclass, field

import requests

log = logging.getLogger(__name__)
HEADERS = {"User-Agent": "job-alert-bot/1.0 (personal project)"}


@dataclass
class Job:
    title: str
    company: str
    url: str
    location: str = ""
    tags: list = field(default_factory=list)
    source: str = ""

    @property
    def id(self) -> str:
        return hashlib.sha256(self.url.encode()).hexdigest()[:16]


class BaseScraper:
    name = "base"

    def fetch(self, url: str, retries: int = 3) -> requests.Response:
        """GET with exponential backoff."""
        for attempt in range(retries):
            try:
                resp = requests.get(url, headers=HEADERS, timeout=15)
                resp.raise_for_status()
                return resp
            except requests.RequestException as exc:
                log.warning("%s: attempt %d failed: %s", self.name, attempt + 1, exc)
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)

    def scrape(self) -> list[Job]:
        raise NotImplementedError
