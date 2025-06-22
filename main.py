import requests
import time
from bs4 import BeautifulSoup
from telegram.ext import ApplicationBuilder
import asyncio

CHECK_INTERVAL = 10  # seconds
BOT_TOKEN = '8033362371:AAGieXQLZMvrqmmbp3H4dXISv_CdA3XSr58'
CHAT_ID = '1680102990'
URL = "https://hypervision.gg/checkout/?prod=1"

async def send_alert():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    await app.bot.send_message(
        chat_id=CHAT_ID,
        text="🚨 A Hypervision slot is now AVAILABLE!\n👉 https://hypervision.gg/checkout/?prod=1"
    )
    print("✅ Slot detected! Telegram alert sent.")

def check_slot_available():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)"
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return "No slots left" not in soup.text
    except Exception as e:
        print(f"❌ Error checking slot:", e)
        return False

print("🔁 Monitoring Hypervision for slot availability...")
while True:
    if check_slot_available():
        asyncio.run(send_alert())
        break
    else:
        print("❌ No slot yet. Checking again in", CHECK_INTERVAL, "seconds...")
    time.sleep(CHECK_INTERVAL)
