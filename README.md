# Inlay Discord Bot

![image](https://i.imgur.com/STPnU64s.png)

A Discord bot to automatically send playable video embeds following a message from supported sites.

[Demo](https://i.imgur.com/5IVdKO3.mp4)

**Note:** Currently a proof of concept

## Tested Sites
- Twitter
- Reddit - [No Audio](https://github.com/kevinle-1/inlay/issues/3)

## Installation & Usage

1. `pip install -r requirements.txt`
2. Create conf.yaml with your Discord Bot Token (see conf.sample.yaml)
3. `python bot.py`
4. Invite with the URL `https://discord.com/oauth2/authorize?client_id=YOUR_APPLICATION_ID&scope=applications.commands+bot`
5. Use by typing `/inlay` or sending a valid URL trigger

## Requirements 
- Python 3.8+ 
- See requirements.txt
- [Discord Bot Token](https://discord.com/developers/applications)