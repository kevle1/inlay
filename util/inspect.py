from urllib.parse import urlsplit
import youtube_dl
import logging
import re

from sites.sites import twitter, reddit

logging.basicConfig(filename="process.log",
                    filemode='a',
                    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

platforms = {
    "Twitter": twitter,
    "Reddit": reddit
}

def process_msg(msg, sites, auto=False, direct=False):
    try:
        url = re.search("(?P<url>https?://[^\s]+)", msg).group("url") if auto else msg
        split_url = urlsplit(url)

        logging.debug(f"Using URL {url} -> {split_url}")

        if direct:
            return extract_info(url)["url"]

        for site in sites:
            if sanitise_base_url(split_url.netloc) in site["catch"]:
                logging.debug(f"Getting {site['name']} URL...")

                info = extract_info(url)

                if site["name"] in platforms.keys():
                    embed = platforms[site["name"]](info)
                else:
                    embed = info["url"]

                logging.debug(f"Formatted embed {embed}")

                return embed
    except AttributeError:
        pass # URL not found in regex
    except Exception as e:
        logging.error(f"Error: Could not process URL {e}")

    return None

def extract_info(url):
    with youtube_dl.YoutubeDL({"format": "bestvideo/best", "quiet": True}) as ydl:
        try:
            return ydl.extract_info(url, download=False) # Also provides rich metadata info
        except Exception as e:
            logging.error(f"Error: Could not get video URL. {e}")

def sanitise_base_url(base):
    return base.replace("www.", "")