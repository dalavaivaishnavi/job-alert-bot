from filters import matches
from scrapers.base import Job


def job(title, tags=None, location="Remote"):
    return Job(title=title, company="Acme", url=f"https://x.com/{title}", location=location, tags=tags or [])


def test_include_match():
    assert matches(job("Python Developer"), include=["python"])


def test_include_no_match():
    assert not matches(job("Java Developer"), include=["python"])


def test_exclude_wins():
    assert not matches(job("Senior Python Developer"), include=["python"], exclude=["senior"])


def test_tags_are_searched():
    assert matches(job("Engineer", tags=["fastapi"]), include=["fastapi"])


def test_location_filter():
    assert matches(job("Python Dev", location="India"), include=["python"], locations=["india"])
    assert not matches(job("Python Dev", location="USA"), include=["python"], locations=["india"])
