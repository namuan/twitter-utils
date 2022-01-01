import time
import logging


def setup_logging() -> None:  # pragma: no cover
    logging.basicConfig(
        handlers=[logging.StreamHandler()],
        format="%(asctime)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    logging.captureWarnings(capture=True)


def sleep_for(seconds: int) -> None:  # pragma: no cover
    logging.info(f"😴 Sleeping for {seconds} seconds...")
    time.sleep(seconds)
