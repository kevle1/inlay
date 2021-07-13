# This file contains any site specific logic (e.g. formatting or url retrieval)
import re

accepted_formats = ["mp4", "webm"]

def twitter(info) -> str:
    return info["url"]
    
def reddit(info) -> str:
    for f in info["formats"]:
        url = f["url"]
        if re.match(r"https://.*720.mp4", url):
            return url
    
    return general(info)

def general(info):
    try:
        return search_format(info["requested_formats"])
    except KeyError:
        return search_format(info["formats"])

def search_format(formats):
    for f in formats:
        if f["ext"] in accepted_formats:
            return f["url"]