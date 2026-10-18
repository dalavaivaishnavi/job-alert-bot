import re


def _word_hit(keywords, text):
    return any(re.search(rf"\b{re.escape(k.lower())}\b", text) for k in keywords)


def matches(job, include=None, exclude=None, locations=None) -> bool:
    include = [k.lower() for k in (include or [])]
    exclude = [k.lower() for k in (exclude or [])]
    locations = [l.lower() for l in (locations or [])]

    title = job.title.lower()
    text = f"{title} {' '.join(job.tags)}".lower()

    if exclude and _word_hit(exclude, title):
        return False
    if include and not any(k in text for k in include):
        return False
    if locations and not any(l in job.location.lower() for l in locations):
        return False
    return True