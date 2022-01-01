from pathlib import Path
from typing import Any

from ward import test

import twitter_utils.twitter_page
from mock_browser import mock_browser_session, output_directory
from twitter_utils.tweets_thread import parse_args, tweets_thread_workflow


@test("Should check if tweets in a twitter thread are fetched and written")
def test_verify_tweets_on_a_page(
    output_directory: Path = output_directory(), mock_browser_session: Any = mock_browser_session()
) -> None:
    twitter_utils.twitter_page.DELAY = 0
    parsed_args = parse_args(
        [
            "--query",
            "jack",
            "--tweet-id",
            "1474263588651",
            "--output-directory",
            output_directory.as_posix(),
        ]
    )
    context = parsed_args.__dict__
    context["browser_session"] = mock_browser_session

    tweets_thread_workflow(context)

    assert mock_browser_session.current().url_requested == "https://twitter.com/jack/status/1474263588651"
    files_in_output_folder = output_directory.joinpath("raw-tweets", "user-jack").glob("*.html")
    assert len(list(files_in_output_folder)) == 1
