from pathlib import Path
from typing import Any, Optional

from ward import test

import twitter_utils.twitter_page
from twitter_utils.tweets_between import parse_args, run_workflow_steps


class TweetHtml:
    def __init__(self, html: str) -> None:
        self.html = html

    @property
    def text(self) -> str:
        return self.html

    def get_attribute(self, attribute: str) -> Optional[str]:
        if attribute == "outerHTML":
            return self.html

        return None


class MockWebDriver:
    url_requested: str

    def __init__(self) -> None:
        print("MockWebDriver.__init__()")

    def get(self, url: str) -> str:
        self.url_requested = url
        return "<html></html>"

    def close(self) -> None:
        print("MockWebDriver.close()")

    def find_elements_by_xpath(self, selector: str) -> list:
        assert selector
        return [TweetHtml("""<html><a href="/some-user/status/12345"></html>""")]

    def execute_script(self, script: str) -> Optional[int]:
        assert script
        if "return" in script:
            return 100
        return None


class MockBrowserSession:
    session: Any

    def start(self) -> None:
        self.session = MockWebDriver()

    def current(self) -> Any:
        return self.session

    def stop(self) -> None:
        self.session.close()


@test("Should check if tweets are fetched and written for the given date range")
def test_verify_tweets_written_between_date_range() -> None:
    twitter_utils.twitter_page.DELAY = 0
    output_directory = ".temp"
    parsed_args = parse_args(
        [
            "--account",
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
    mock_browser_session = MockBrowserSession()
    context["browser_session"] = mock_browser_session

    run_workflow_steps(context)

    assert (
        mock_browser_session.current().url_requested
        == "https://twitter.com/search?q=(from%3Ajack)%20until%3A2020-02-02%20since%3A2020-02-01&src=typed_query"
    )
    files_in_output_folder = Path(output_directory).joinpath("raw-tweets", "jack").glob("*.html")
    assert len(list(files_in_output_folder)) == 1
