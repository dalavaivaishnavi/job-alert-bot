from db import JobStore
from scrapers.base import Job


def test_dedupe(tmp_path):
    store = JobStore(str(tmp_path / "t.db"))
    j = Job(title="Python Dev", company="Acme", url="https://x.com/1")
    assert store.is_new(j.id)
    store.mark_seen(j)
    assert not store.is_new(j.id)
