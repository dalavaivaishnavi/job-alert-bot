import xml.etree.ElementTree as ET

from .base import BaseScraper, Job


class WeWorkRemotelyScraper(BaseScraper):
    name = "weworkremotely"
    URL = "https://weworkremotely.com/categories/remote-programming-jobs.rss"

    def scrape(self) -> list[Job]:
        root = ET.fromstring(self.fetch(self.URL).content)
        jobs = []
        for item in root.iter("item"):
            raw_title = (item.findtext("title") or "").strip()
            company, _, title = raw_title.partition(": ")
            if not title:
                company, title = "", raw_title
            jobs.append(Job(
                title=title,
                company=company,
                url=(item.findtext("link") or "").strip(),
                location=(item.findtext("region") or "Remote").strip(),
                source=self.name,
            ))
        return jobs
