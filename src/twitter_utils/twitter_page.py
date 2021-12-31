from __future__ import annotations

import logging
import random
import re
from time import sleep
from typing import Any

from twitter_utils.browser_session import BrowserSession

DELAY = 5  # seconds
SELECTOR = "//*[@role='article']"


def url_builder(from_account: str, tweet_id: str) -> str:
    return f"https://twitter.com/{from_account}/status/{tweet_id}"


def get_first_tweet_on_page(session: BrowserSession) -> Any:
    tweets_on_page = session.current().find_elements_by_xpath(SELECTOR)
    return tweets_on_page[0]


def scroll_to_top(session: BrowserSession) -> None:
    sleep(DELAY)
    session.current().execute_script("window.scrollTo(0, 10);")


def get_tweets_on_page(session: BrowserSession) -> tuple[list, int]:
    tweets_on_page = session.current().find_elements_by_xpath(SELECTOR)
    no_of_tweets_on_page = len(tweets_on_page)
    print(f"🔄 Total number of tweets on screen: {no_of_tweets_on_page}")
    return tweets_on_page, no_of_tweets_on_page


def scroll_to_end(session: BrowserSession) -> None:
    sleep(DELAY)  # sleep before scrolling
    session.current().execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(DELAY)  # For the page to catch up before we count again
    print("⬇️ Scroll down")


def scroll_speed() -> int:
    return random.randint(300, 500)


def scroll_and_collect_tweets_from_page(session: BrowserSession, full_url: str) -> dict:
    session.current().get(full_url)
    sleep(DELAY)
    tweets_with_html = {}
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        tweets_on_page, no_of_tweets_on_page = get_tweets_on_page(session)
        for tweet in tweets_on_page:
            tweet_html = tweet.get_attribute("outerHTML")
            _, status_id = extract_data_from(tweet_html, tweet.text)
            tweets_with_html[status_id] = tweet_html

        session.current().execute_script(f"window.scrollTo(0, {current_scroll_position});")
        new_height = session.current().execute_script("return document.body.scrollHeight;")
        current_scroll_position += scroll_speed()
        logging.info("current_scroll_position: %s , new_height: %s", current_scroll_position, new_height)
        # Wait to any dynamic elements to load
        sleep(DELAY)
    return tweets_with_html


def collect_tweets_from_page(session: BrowserSession, full_url: str) -> dict:
    session.current().get(full_url)
    sleep(DELAY)

    tweets_with_html = {}

    tweets_not_changed_on_screen_counter = 0
    max_count_if_tweets_dont_change = 4
    last_count_tweets_on_page = 0

    tweets_on_page, no_of_tweets_on_page = get_tweets_on_page(session)

    while tweets_not_changed_on_screen_counter < max_count_if_tweets_dont_change:
        if no_of_tweets_on_page == last_count_tweets_on_page:
            tweets_not_changed_on_screen_counter += 1
            print(
                "🤔 Tweets not changed since last {} attempts - Last count: {}".format(
                    tweets_not_changed_on_screen_counter, last_count_tweets_on_page
                )
            )
        else:
            tweets_not_changed_on_screen_counter = 0

        last_count_tweets_on_page = no_of_tweets_on_page

        for tweet in tweets_on_page:
            tweet_html = tweet.get_attribute("outerHTML")
            _, status_id = extract_data_from(tweet_html, tweet.text)
            tweets_with_html[status_id] = tweet_html

        scroll_to_end(session)
        tweets_on_page, no_of_tweets_on_page = get_tweets_on_page(session)
    else:
        print("🤩 Looks like we are done")

    return tweets_with_html


def extract_data_from(tweet: str, tweet_text: str) -> tuple[str, str]:
    rgx = re.compile(r'a\shref="/(\S+)/status/(\d+)"')

    matches = rgx.findall(tweet)

    twitter_handle = "unknown"
    status_id = "unknown"

    if not matches:
        print(f"❌ Unable to find twitter status identifier in \n => {tweet_text}")
    else:
        twitter_handle, status_id = matches[0]

    return twitter_handle, status_id
