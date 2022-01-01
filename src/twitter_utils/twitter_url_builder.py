from datetime import datetime


def since_query_param(since: datetime) -> str:
    return f"since%3A{since}"


def until_query_param(until: datetime) -> str:
    return f"until%3A{until}"


def from_account_query_param(from_account: str) -> str:
    return f"from%3A{from_account}"


def search_query_builder(from_account: str, since: datetime, until: datetime) -> str:
    s = since_query_param(since)
    u = until_query_param(until)
    f = from_account_query_param(from_account)
    return f"https://twitter.com/search?q=({f})%20{u}%20{s}&src=typed_query"


def status_endpoint(from_account: str, tweet_id: str) -> str:
    return f"https://twitter.com/{from_account}/status/{tweet_id}"
