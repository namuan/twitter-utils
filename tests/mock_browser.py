from pathlib import Path
from typing import Any, Optional

from ward import fixture

import twitter_utils.twitter_page
from twitter_utils import random_string

twitter_utils.twitter_page.DELAY = 0


class TweetHtml:
    def __init__(self, html: str) -> None:
        self.html = html

    @property
    def text(self) -> str:
        return self.html

    def get_attribute(self, _: str) -> str:
        return self.html


class MockWebDriver:
    url_requested: str

    def get(self, url: str) -> str:
        self.url_requested = url
        return "<html></html>"

    def close(self) -> None:
        pass

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


@fixture
def output_directory() -> Path:
    return Path(".temp").joinpath(random_string(10))


@fixture
def mock_browser_session() -> Any:
    return MockBrowserSession()
