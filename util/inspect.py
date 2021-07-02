from urllib.parse import urlsplit, urlunsplit
import youtube_dl
import re

def process_msg(msg, sites, auto=False, direct=False): 
    url = re.search("(?P<url>https?://[^\s]+)", msg).group("url") if auto else msg
    split_url = urlsplit(url)

    print(f"Using URL {url} -> {split_url}")

    if direct:
        return get_direct_url(url) 

    for site in sites: 
        if(split_url.netloc in site['catch']):
            print(f"Getting {site['name']} URL...")

            direct_url = get_direct_url(url) 
            print(f"Direct URL {direct_url}")
            
            return direct_url

    return None

def get_direct_url(url):
    with youtube_dl.YoutubeDL({}) as ydl:
        try:
            return ydl.extract_info(url, download=False)["url"]
        except Exception as e:
            print(f"Error: Could not get video URL. {e}")