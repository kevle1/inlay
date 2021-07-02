from urllib.parse import urlsplit, urlunsplit
import youtube_dl
import re

def process_msg(msg, sites, auto=False, direct=False): 
    try:
        url = re.search("(?P<url>https?://[^\s]+)", msg).group("url") if auto else msg
        split_url = urlsplit(url)

        print(f"Using URL {url} -> {split_url}")

        if direct:
            return get_direct_url(url) 

        for site in sites: 
            if(sanitise_base_url(split_url.netloc) in site['catch']):
                print(f"Getting {site['name']} URL...")

                direct_url = get_direct_url(url) 
                print(f"Direct URL {direct_url}")
                
                return direct_url
    except AttributeError:
        pass 
    except Exception as e:
        print(f"Error: Could not process URL {e}")

    return None

def get_direct_url(url): # Schema returned by this is not 
    with youtube_dl.YoutubeDL({'format': 'bestvideo/best', 'merge-output-format': 'mp4'}) as ydl:
        try:
            return ydl.extract_info(url, download=False)["url"] # Also provides rich metadata info 
        except Exception as e:
            print(f"Error: Could not get video URL. {e}")

def sanitise_base_url(base):
    return base.replace("www.", "")