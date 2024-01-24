# This file contains any site specific logic (e.g. formatting or url retrieval)
import re

import requests

ACCEPTED_FORMATS = ["mp4", "webm"]  # Discord embeddable

TWITTER_VIDEO_FORMATS = [".mp4", ".mov", ".webm"]
REDDIT_URL_PATTERNS = [
    r"https://.*720.mp4",
    r"https://.*480.mp4",
    r"https://.*360.mp4",
    r"https://.*240.mp4",
]


def replace_twitter(url: str) -> str:
    embed_api = "api.vxtwitter.com"

    embed_api_url = (
        url.replace("twitter.com", embed_api)
        .replace("t.co", embed_api)
        .replace("x.com", embed_api)
    )
    embed_response = requests.get(embed_api_url)

    if embed_response.status_code == 200:
        embed_urls = embed_response.json()["mediaURLs"]
        for embed_url in embed_urls:
            if any(ext in embed_url for ext in TWITTER_VIDEO_FORMATS):
                return embed_url


def replace_instagram(url: str) -> str:
    embed_service = "ddinstagram.com"
    return url.replace("instagram.com", embed_service)


def ytdlp_extract_reddit_format(info: dict) -> str:
    patterns = "(?:%s)" % "|".join(REDDIT_URL_PATTERNS)

    for f in reversed(info["formats"]):
        url = f["url"]
        if re.match(patterns, url):
            return url

    return general(info)  # Fallback


def general(info: dict):
    try:
        return search_format(info["requested_formats"])
    except KeyError:
        return search_format(info["formats"])


def search_format(formats):
    for f in formats:
        if f["ext"] in ACCEPTED_FORMATS:
            return f["url"]
