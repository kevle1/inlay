# Inlay Discord Bot

![image](https://i.imgur.com/STPnU64s.png)

A Discord bot to automatically send playable video embeds following a message from supported sites.

**Note:** Currently a proof of concept

## Tested Sites
- Twitter
- Reddit (no audio with direct link due to Reddit handling of videos)

## Requirements 
- Python 3.8+ 
- See requirements.txt
- [Discord Bot Token](https://discord.com/developers/applications)

## Todo
- Improve Error Handling
- Allow option for any URL supported by youtube-dl
- Add caching strategy
- Add Logging (print statements to be removed)
- Send message with the post metadata (Title, description, etc)