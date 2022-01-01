from __future__ import annotations

import logging
from collections.abc import Iterable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from py_executable_checklist.workflow import WorkflowBase

from twitter_utils.browser_session import BrowserSession
from twitter_utils.tweets_writer import write_raw_tweets
from twitter_utils.twitter_page import scroll_and_collect_tweets_from_page
from twitter_utils.twitter_url_builder import search_query_builder, status_endpoint


class CreateBrowserSession(WorkflowBase):
    browser_session: Any

    def run(self, _: dict) -> None:
        self.browser_session.start()


class GetAllTweetsOnPage(WorkflowBase):
    account: str
    tweet_id: str
    browser_session: BrowserSession

    def run(self, context: dict) -> None:
        full_url = status_endpoint(self.account, self.tweet_id)
        logging.info("🔎 Twitter status URL: %s", full_url)
        all_tweets: dict[str, str] = scroll_and_collect_tweets_from_page(self.browser_session, full_url)

        logging.info("✅ Total tweets: %s", len(all_tweets))
        context["all_tweets"] = all_tweets


class GetAllTweetsBetweenDateRange(WorkflowBase):
    account: str
    since: datetime
    until: datetime
    browser_session: BrowserSession

    def run(self, context: dict) -> None:
        all_tweets: dict[str, str] = {}
        for d in self.date_range(self.since, self.until):
            full_url = search_query_builder(self.account, d, d + timedelta(1))
            logging.info("🔎 Search URL: %s", full_url)
            all_tweets = {
                **all_tweets,
                **scroll_and_collect_tweets_from_page(self.browser_session, full_url),
            }

        logging.info("✅ Total tweets: %s", len(all_tweets))
        context["all_tweets"] = all_tweets

    def date_range(self, since: datetime, until: datetime) -> Iterable:
        for n in range(int((until - since).days)):
            yield since + timedelta(n)


class WriteTweetsToDirectory(WorkflowBase):
    account: str
    output_directory: Path
    all_tweets: dict

    def run(self, _: dict) -> None:
        output_directory = write_raw_tweets(self.output_directory, self.account, self.all_tweets)
        logging.info("📝 Tweets written in %s", output_directory)


class CloseBrowserSession(WorkflowBase):
    browser_session: BrowserSession

    def run(self, _: dict) -> None:
        self.browser_session.stop()
