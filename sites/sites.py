# This file contains any site specific logic (e.g. formatting or url retrieval)

accepted_formats = ["mp4"]

def twitter(info) -> str:
    return info["url"]
    
def reddit(info) -> str:
    return base(info)

def base(info):
    for f in info["requested_formats"]:
        if f["ext"] in accepted_formats:
            return f["url"]