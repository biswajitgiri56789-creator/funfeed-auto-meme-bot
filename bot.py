import os
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@FunFeed1"

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found")
        return

    bot = Bot(token=BOT_TOKEN)

    url = "https://meme-api.com/gimme"
    r = requests.get(url, timeout=20).json()

    photo_url = r["url"]
    title = r["title"]

    caption = f"😂 {title}\n\n🔥 @FunFeed1"

    try:
        bot.send_photo(
            chat_id=CHANNEL_USERNAME,
            photo=photo_url,
            caption=caption
        )
        print("✅ Meme posted successfully to Telegram")
    except Exception as e:
        print("❌ Telegram error:", e)

if __name__ == "__main__":
    main()
