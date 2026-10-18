from .base import BaseScraper, Job


class RemoteOKScraper(BaseScraper):
    name = "remoteok"
    URL = "https://remoteok.com/api"

    def scrape(self) -> list[Job]:
        data = self.fetch(self.URL).json()
        jobs = []
        for item in data:
            if "position" not in item:  # first element is a legal notice
                continue
            jobs.append(Job(
                title=item["position"],
                company=item.get("company", ""),
                url=item.get("url") or f"https://remoteok.com/{item.get('id')}",
                location=item.get("location", "") or "Remote",
                tags=item.get("tags", []),
                source=self.name,
            ))
        return jobs
