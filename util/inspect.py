from urllib.parse import urlsplit
from functools import lru_cache
import youtube_dl
import logging
import re

from sites.sites import general, twitter, reddit

logging.basicConfig(filename="process.log",
                    filemode='a',
                    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

platforms = {
    "Twitter": twitter,
    "Reddit": reddit
}

# platforms = {
#     "Twitter": {"handler": twitter, "query": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"},
#     "Reddit": {"handler": reddit, "query": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"},
# }

def process_site(msg, sites):
    try:
        url = re.search(r"(?P<url>https?://[^\s]+)", msg).group("url")
        spoiler = bool(re.match(fr"\|\|{url}\|\|", msg))

        split_url = urlsplit(url)

        logging.debug(f"Using URL {url} parsed -> {split_url}")

        for site in sites:
            if sanitise_base_url(split_url.netloc) in site["catch"]:
                return site["name"], url, spoiler

        return None, url, spoiler
    except AttributeError:
        pass # URL not found in regex
    except Exception as e:
        logging.error(f"Error: Could not process URL {e}")
            
    return None, None, None

@lru_cache(maxsize=None)
def process_url(url, site_name, direct=False):
    try:
        if direct and not site_name:
            return general(extract_info(url))
        else:
            info = extract_info(url)
            
            if site_name in platforms.keys(): # There is a special handler for the URL 
                embed = platforms[site_name](info)
            else:
                embed = info["url"] # Attempt get key "URL"

            logging.debug(f"Result string: {embed}")

            return embed
    except Exception as e:
        logging.error(f"Error: Could not get direct link for URL {e}")

    return None

def extract_info(url):
    logging.debug(f"Getting URL {url} information")

    with youtube_dl.YoutubeDL({"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4", "quiet": True}) as ydl:
        try:
            return ydl.extract_info(url, download=False) # Also provides rich metadata info
        except Exception as e:
            logging.error(f"Error: Could not get video URL. {e}")

def sanitise_base_url(base):
    return base.replace("www.", "")