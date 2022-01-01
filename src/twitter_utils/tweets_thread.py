#!/usr/bin/env python3
"""
Downloads tweets between two dates.
"""
from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from pathlib import Path

from py_executable_checklist.workflow import run_workflow

from twitter_utils import setup_logging
from twitter_utils.browser_session import BrowserSession
from twitter_utils.workflows.workflow_steps import (
    CloseBrowserSession,
    CreateBrowserSession,
    GetAllTweetsOnPage,
    WriteTweetsToDirectory,
)


def parse_args(args: list[str]) -> Namespace:
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-a", "--account", required=True, type=str, help="Twitter Handle")
    parser.add_argument(
        "-t",
        "--tweet-id",
        required=True,
        type=str,
        help="Tweet/Status ID",
    )
    parser.add_argument(
        "-o",
        "--output-directory",
        required=True,
        type=Path,
        help="Directory to save tweets to",
    )
    parser.add_argument(
        "-b",
        "--browser",
        required=False,
        type=str,
        default="firefox",
        help="Browser to use for web scraping. Default: firefox",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        dest="verbose",
        help="Display context variables at each step",
    )
    return parser.parse_args(args=args)


def workflow_steps() -> list:
    return [
        CreateBrowserSession,
        GetAllTweetsOnPage,
        WriteTweetsToDirectory,
        CloseBrowserSession,
    ]


def tweets_thread_workflow(context: dict) -> None:
    run_workflow(context, workflow_steps())


def main() -> None:  # pragma: no cover
    setup_logging()
    parsed_args = parse_args(sys.argv[1:])
    context = parsed_args.__dict__
    context["browser_session"] = BrowserSession(parsed_args.browser)
    tweets_thread_workflow(context)


if __name__ == "__main__":  # pragma: no cover
    main()
