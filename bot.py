import os
import json
import random
import asyncio
import requests
from telethon import TelegramClient
from config import *
from PIL import Image
import openai

# -------------------------------
# Telegram client setup
# -------------------------------
api_id = 123456  # Get from https://my.telegram.org
api_hash = "YOUR_API_HASH"
client = TelegramClient('funfeed_session', api_id, api_hash)

# -------------------------------
# OpenAI setup
# -------------------------------
openai.api_key = OPENAI_API_KEY

# -------------------------------
# Posted memes tracker
# -------------------------------
if not os.path.exists('posted_memes.json'):
    with open('posted_memes.json', 'w') as f:
        json.dump([], f)

with open('posted_memes.json', 'r') as f:
    posted_memes = json.load(f)

# -------------------------------
# AI Meme Generator
# -------------------------------
async def generate_ai_meme():
    try:
        prompt = "Create a funny, viral, relatable meme about daily life or internet culture. Include a short caption."
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        img_url = response['data'][0]['url']
        img_data = requests.get(img_url).content
        meme_path = f"ai_meme_{random.randint(1000,9999)}.png"
        with open(meme_path, 'wb') as f:
            f.write(img_data)
        return meme_path
    except Exception as e:
        print("AI meme generation error:", e)
        return None

# -------------------------------
# Post meme to Telegram
# -------------------------------
async def post_meme():
    meme_path = await generate_ai_meme()
    if meme_path and meme_path not in posted_memes:
        await client.send_file(CHANNEL_ID, meme_path, caption=CAPTION_TEMPLATE)
        posted_memes.append(meme_path)
        with open('posted_memes.json', 'w') as f:
            json.dump(posted_memes, f)
        print(f"Posted meme: {meme_path}")
        os.remove(meme_path)  # Clean up
    else:
        print("No new meme to post.")

# -------------------------------
# Main loop
# -------------------------------
async def main():
    await client.start(bot_token=BOT_TOKEN)
    while True:
        await post_meme()
        await asyncio.sleep(POST_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()
