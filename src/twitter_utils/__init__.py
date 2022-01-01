import logging
import random
import string
import time


def setup_logging() -> None:  # pragma: no cover
    logging.basicConfig(
        handlers=[logging.StreamHandler()],
        format="%(asctime)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    logging.captureWarnings(capture=True)


def sleep_for(seconds: int) -> None:  # pragma: no cover
    logging.info("😴 Sleeping for %s seconds...", seconds)
    time.sleep(seconds)


def random_string(length: int) -> str:
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
