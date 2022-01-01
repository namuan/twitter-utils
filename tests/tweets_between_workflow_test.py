from pathlib import Path
from typing import Any

from twitter_utils.tweets_between import parse_args, tweets_between_workflow
from ward import test

from mock_browser import mock_browser_session, output_directory


@test("Should check if tweets are fetched for a given twitter handle between date range")
def test_verify_tweets_twitter_handle_date_range(
        output_directory: str = output_directory(), mock_browser_session: Any = mock_browser_session()
) -> None:
    parsed_args = parse_args(
        [
            "--query",
            "jack",
            "--since",
            "2020-02-01",
            "--until",
            "2020-02-02",
            "--output-directory",
            ".temp",
        ]
    )
    context = parsed_args.__dict__
    context["browser_session"] = mock_browser_session

    tweets_between_workflow(context)

    assert (
            mock_browser_session.current().url_requested
            == "https://twitter.com/search?q=(from%3Ajack)%20until%3A2020-02-02%20since%3A2020-02-01&src=typed_query"
    )
    files_in_output_folder = Path(output_directory).joinpath("raw-tweets", "user-jack").glob("*.html")
    assert len(list(files_in_output_folder)) == 1


@test("Should check if tweets are fetched for a given hash tag between date range")
def test_verify_tweets_hash_tag_date_range(
        output_directory: str = output_directory(), mock_browser_session: Any = mock_browser_session()
) -> None:
    parsed_args = parse_args(
        [
            "--query",
            "#web3",
            "--since",
            "2020-02-01",
            "--until",
            "2020-02-02",
            "--output-directory",
            ".temp",
        ]
    )
    context = parsed_args.__dict__
    context["browser_session"] = mock_browser_session

    tweets_between_workflow(context)

    assert (
            mock_browser_session.current().url_requested
            == "https://twitter.com/search?q=(from%3A%23web3)%20until%3A2020-02-02%20since%3A2020-02-01&src=typed_query"
    )

    files_in_output_folder = Path(output_directory).joinpath("raw-tweets", "hashtag-web3").glob("*.html")
    assert len(list(files_in_output_folder)) == 1
