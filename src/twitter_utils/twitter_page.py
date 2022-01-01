from __future__ import annotations

import logging
import random
import re
from time import sleep

from twitter_utils.browser_session import BrowserSession

DELAY = 5  # seconds
SELECTOR = "//*[@role='article']"


def scroll_and_collect_tweets_from_page(session: BrowserSession, full_url: str) -> dict:
    session.current().get(full_url)
    sleep(DELAY)
    tweets_with_html = {}
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        tweets_on_page, no_of_tweets_on_page = _get_tweets_on_page(session)
        for tweet in tweets_on_page:
            tweet_html = tweet.get_attribute("outerHTML")
            _, status_id = _extract_data_from(tweet_html, tweet.text)
            if status_id != "unknown":
                tweets_with_html[status_id] = tweet_html

        session.current().execute_script(f"window.scrollTo(0, {current_scroll_position});")
        new_height = session.current().execute_script("return document.body.scrollHeight;")
        current_scroll_position += _scroll_speed()
        logging.info("current_scroll_position: %s , new_height: %s", current_scroll_position, new_height)
        # Wait to any dynamic elements to load
        sleep(DELAY)
    return tweets_with_html


def _get_tweets_on_page(session: BrowserSession) -> tuple[list, int]:
    tweets_on_page = session.current().find_elements_by_xpath(SELECTOR)
    no_of_tweets_on_page = len(tweets_on_page)
    print(f"🔄 Total number of tweets on screen: {no_of_tweets_on_page}")
    return tweets_on_page, no_of_tweets_on_page


def _scroll_speed() -> int:
    return random.randint(300, 500)


def _extract_data_from(tweet: str, tweet_text: str) -> tuple[str, str]:
    rgx = re.compile(r'a\shref="/(\S+)/status/(\d+)"')

    matches = rgx.findall(tweet)

    twitter_handle = "unknown"
    status_id = "unknown"

    if not matches:
        print(f"❌ Unable to find twitter status identifier in \n => {tweet_text}")
    else:
        twitter_handle, status_id = matches[0]

    return twitter_handle, status_id
