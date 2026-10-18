import argparse
import logging

import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from db import JobStore
from filters import matches
from notifier import TelegramNotifier
from scrapers import REGISTRY

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("job-alert-bot")


def run_once(config: dict, store: JobStore, notifier, seed: bool = False) -> int:
    f = config.get("filters", {})
    sent = 0
    for name in config["sources"]:
        try:
            jobs = REGISTRY[name]().scrape()
        except Exception as exc:
            log.exception("Scraper %s failed", name)
            if notifier and not seed:
                notifier.send(f"⚠️ Scraper '{name}' failed: {exc}")
            continue

        for job in jobs:
            if not store.is_new(job.id):
                continue
            store.mark_seen(job)
            if seed:
                continue  # first run: remember everything, alert on nothing
            if matches(job, f.get("include_keywords"), f.get("exclude_keywords"), f.get("locations")):
                notifier.send_job(job)
                sent += 1
        log.info("%s: %d jobs fetched", name, len(jobs))
    log.info("Run complete, %d alerts sent", sent)
    return sent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="run a single pass and exit")
    parser.add_argument("--seed", action="store_true", help="mark current jobs as seen without alerting")
    args = parser.parse_args()

    load_dotenv()
    config = yaml.safe_load(open("config.yaml"))
    store = JobStore()
    notifier = None if args.seed else TelegramNotifier()

    if args.seed or args.once:
        run_once(config, store, notifier, seed=args.seed)
        return

    run_once(config, store, notifier)
    sched = BlockingScheduler()
    sched.add_job(run_once, "interval", minutes=config.get("interval_minutes", 60),
                  args=[config, store, notifier])
    log.info("Scheduler started")
    sched.start()


if __name__ == "__main__":
    main()
