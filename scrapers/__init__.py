from .remoteok import RemoteOKScraper
from .weworkremotely import WeWorkRemotelyScraper

REGISTRY = {
    "remoteok": RemoteOKScraper,
    "weworkremotely": WeWorkRemotelyScraper,
}
