# This file contains any site specific logic (e.g. formatting or url retrieval)

def twitter(info) -> str:
    return info["url"]
    
def reddit(info) -> str:
    for f in info["requested_formats"]:
        if f["ext"] == "mp4":
            return f["url"]