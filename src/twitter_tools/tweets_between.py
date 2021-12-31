#!/usr/bin/env python3
"""
Downloads tweets between two dates.
"""
import datetime
import sys
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from pathlib import Path
from typing import List

from py_executable_checklist.workflow import run_workflow

from twitter_tools import setup_logging
from twitter_tools.browser_session import BrowserSession
from twitter_tools.workflows.tweets_between_workflow import (  # type: ignore
    workflow_steps,
)


def parse_args(args: List[str]) -> Namespace:
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-a", "--account", required=True, type=str, help="Twitter Handle")
    parser.add_argument(
        "-s",
        "--since",
        required=True,
        type=datetime.date.fromisoformat,
        help="Search from this date. Format YYYY-MM-DD",
    )
    parser.add_argument(
        "-u",
        "--until",
        required=True,
        type=datetime.date.fromisoformat,
        help="Search until this date. Format YYYY-MM-DD",
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
        "-o",
        "--output-directory",
        required=True,
        type=Path,
        help="Directory to save tweets to",
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


def run_workflow_steps(context: dict) -> None:
    run_workflow(context, workflow_steps())


def main() -> None:
    setup_logging()
    parsed_args = parse_args(sys.argv[1:])
    context = parsed_args.__dict__
    context["browser_session"] = BrowserSession(parsed_args.browser)
    run_workflow_steps(context)


if __name__ == "__main__":
    main()
