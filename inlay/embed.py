import logging
import re
from functools import lru_cache
from typing import List
from urllib.parse import urlsplit

import yt_dlp
from pydantic import BaseModel

from inlay.processors import (
    general,
    replace_instagram,
    replace_twitter,
    ytdlp_extract_reddit_format,
)

logging.basicConfig(
    filename="process.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

strategy_replace = {
    "Twitter": replace_twitter,
    "Instagram": replace_instagram,
}

ytdlp_postprocess = {
    "Reddit": ytdlp_extract_reddit_format,
}


class Site(BaseModel):
    name: str
    active: bool
    catch: List[str]


class ParsedSite(BaseModel):
    name: str
    url: str
    spoiler: bool = False

    def __hash__(self):
        return hash(self.url)


def parse_site(raw_msg: str, sites: list[Site]) -> ParsedSite:
    try:
        url = re.search(r"(?P<url>https?://[^\s]+)", raw_msg).group("url")
        spoiler = bool(re.match(rf"\|\|{url}\|\|", raw_msg))

        split_url = urlsplit(url)

        logging.debug(f"Parsed URL {url} into components: {split_url}")

        for site in sites:
            if sanitise_base_url(split_url.netloc) in site.catch and site.active:
                return ParsedSite(name=site.name, url=url, spoiler=spoiler)

        return ParsedSite(name=None, url=url, spoiler=spoiler)
    except AttributeError:
        pass  # No URL not found in regex
    except Exception as e:
        logging.error(f"Error: Could not process URL {e}")

    return None


@lru_cache(maxsize=None)
def generate_embed(site: ParsedSite, direct: bool = False):
    try:
        # Replace strategy
        if site.name in strategy_replace.keys():
            return strategy_replace[site.name](site.url)

        # yt-dlp strategy
        if direct and not site.name:
            return general(strategy_yt_dlp(site.url))
        else:
            ytdlp_extract = strategy_yt_dlp(site.url)

            if (
                site.name in ytdlp_postprocess.keys()
            ):  # There is a special handler for the URL
                embed = ytdlp_postprocess[site.name](ytdlp_extract)
            else:
                embed = ytdlp_extract["url"]  # Just try get the URL

            logging.debug(f"Result string: {embed}")

            return embed
    except Exception as e:
        logging.error(f"Error: Could not get direct link for URL {e}")

    return None


def strategy_yt_dlp(url: str) -> dict:
    logging.debug(f"Getting URL {url} information")

    with yt_dlp.YoutubeDL(
        {"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4", "quiet": True}
    ) as ydl:
        try:
            return ydl.extract_info(url, download=False)
        except Exception as e:
            logging.error(f"Error: Could not get video URL. {e}")


def sanitise_base_url(base):
    return base.replace("www.", "")
