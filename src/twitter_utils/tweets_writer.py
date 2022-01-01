from pathlib import Path


def write_raw_tweets(output_directory: Path, tweets_group: str, tweets: dict) -> Path:
    output_directory = output_directory / "raw-tweets" / tweets_group
    output_directory.mkdir(parents=True, exist_ok=True)

    for tweet_id, tweet_html in tweets.items():
        output_directory.joinpath(tweet_id + ".html").write_text(tweet_html)

    return output_directory
