import os
import json
import random
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@FunFeed1"

MEME_APIS = [
    "https://meme-api.com/gimme",
    "https://meme-api.com/gimme/ProgrammerHumor",
    "https://meme-api.com/gimme/memes"
]

def get_meme():
    url = random.choice(MEME_APIS)
    data = requests.get(url, timeout=20).json()
    return data["url"], data["title"]

def main():
    bot = Bot(token=BOT_TOKEN)

    meme_url, title = get_meme()

    caption = f"😂 {title}\n\n🔥 @FunFeed1"

    bot.send_photo(
        chat_id=CHANNEL_USERNAME,
        photo=meme_url,
        caption=caption
    )

    print("✅ Meme posted successfully")

if __name__ == "__main__":
    main()
