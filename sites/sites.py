# This file contains any site specific logic (e.g. formatting or url retrieval)
import re
import json 

accepted_formats = ["mp4", "webm"] # Discord embeddable 
reddit_url_patterns = [r"https://.*720.mp4", r"https://.*480.mp4", r"https://.*360.mp4", r"https://.*240.mp4"]

def twitter(info) -> str:
    desc = ""

    # try:
    #     title = info["title"].replace(f"{info['uploader']} - ", "")
    #     desc = f">>> **Twitter**\n`{info['uploader']} - @{info['uploader_id']}` - `Likes: {info['like_count']}`\n{title}\n\n"
    # except KeyError:
    #     pass
        
    return desc + info["url"]
    
def reddit(info) -> str:
    patterns = "(?:%s)" % "|".join(reddit_url_patterns)

    for f in reversed(info["formats"]):
        url = f["url"]
        if re.match(patterns, url):
            return url

    return general(info) # Fallback

def general(info):
    try:
        return search_format(info["requested_formats"])
    except KeyError:
        return search_format(info["formats"])

def search_format(formats):
    for f in formats:
        if f["ext"] in accepted_formats:
            return f["url"]