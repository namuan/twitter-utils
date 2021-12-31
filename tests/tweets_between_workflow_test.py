# mypy: ignore-errors

from pathlib import Path

from ward import test

import twitter_tools.twitter_page
from twitter_tools.tweets_between import parse_args, run_workflow_steps


class TweetHtml:
    def __init__(self, html):
        self.html = html

    @property
    def text(self):
        return self.html

    def get_attribute(self, attribute):
        if attribute == "outerHTML":
            return self.html

        return None


class MockWebDriver:
    def __init__(self):
        print("MockWebDriver.__init__()")
        self.url_requested = None

    def get(self, url: str) -> str:
        self.url_requested = url
        return "<html></html>"

    def close(self):
        print("MockWebDriver.close()")

    def find_elements_by_xpath(self, selector: str):
        assert selector
        return [TweetHtml("""<html><a href="/some-user/status/12345"></html>""")]

    def execute_script(self, script: str) -> None:
        assert script


class MockBrowserSession:
    def __init__(self):
        self.session = None

    def start(self):
        self.session = MockWebDriver()

    def current(self):
        return self.session

    def stop(self):
        self.session.close()


@test("Should check if tweets are fetched and written for the given date range")
def test_verify_tweets_written_between_date_range() -> None:
    twitter_tools.twitter_page.DELAY = 0
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
