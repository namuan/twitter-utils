from typing import Any

from selenium import webdriver  # type: ignore


class BrowserSession:  # pragma: no cover
    def __init__(self, given_browser: Any) -> None:
        self.browser = given_browser
        self.session = webdriver.Firefox("fireprofile")

    def start(self) -> None:
        if self.browser == "safari":
            self.session = webdriver.Safari()
        elif self.browser == "chrome":
            self.session = webdriver.Chrome()

    def stop(self) -> None:
        self.session.close()

    def current(self) -> Any:
        return self.session
