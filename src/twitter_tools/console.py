import logging
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter

from py_executable_checklist.workflow import run_workflow

from twitter_tools.workflow import workflow_steps


def setup_logging() -> None:
    logging.basicConfig(
        handlers=[logging.StreamHandler()],
        format="%(asctime)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    logging.captureWarnings(capture=True)


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-l", "--links-file", required=True, type=str, help="Path to links file"
    )
    parser.add_argument(
        "-t", "--post-title", required=True, type=str, help="Blog post title"
    )
    parser.add_argument(
        "-b",
        "--blog-directory",
        type=str,
        required=True,
        help="Full path to blog directory",
    )
    parser.add_argument(
        "-e",
        "--open-in-editor",
        action="store_true",
        default=False,
        help="Open blog site in editor",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        dest="verbose",
        help="Display context variables at each step",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()
    run_workflow(args.__dict__, workflow_steps())


if __name__ == "__main__":
    main()
