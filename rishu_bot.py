import re
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from pyrogram.enums import ChatAction
from pyrogram.errors import UserNotParticipant
import requests
import time
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread
import pymongo
from typing import Optional
import random

# Load env vars
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_HASH = os.environ.get("API_HASH")
API_ID = int(os.environ.get("API_ID"))
MONGO_URI = os.environ.get("MONGO_URI")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

# Constants
CHANNEL_1_USERNAME = "bot_backup"
CHANNEL_2_USERNAME = "terabox_bots7"
TERABOX_API = "https://terabox-player.rishuapi.workers.dev/?url="
DUMP_CHANNEL = "-1002788628376"

# Flask app
flask_app = Flask(__name__)
start_time = time.time()

# MongoDB
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["teraboxbot"]
users_collection = db.get_collection("users")

# Pyrogram
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@flask_app.route('/')
def home():
    uptime_minutes = (time.time() - start_time) / 60
    user_count = users_collection.count_documents({})
    return f"Bot uptime: {uptime_minutes:.2f} minutes\nUnique users: {user_count}"

async def is_user_in_channel(client, user_id, channel_username):
    try:
        await client.get_chat_member(channel_username, user_id)
        return True
    except UserNotParticipant:
        return False
    except:
        return False

async def send_join_prompt(client, chat_id):
    buttons = [
        [InlineKeyboardButton("♡ Join ♡", url=f"https://t.me/{CHANNEL_1_USERNAME}")],
        [InlineKeyboardButton("♡ Join ♡", url=f"https://t.me/{CHANNEL_2_USERNAME}")]
    ]
    await client.send_message(chat_id, "♡ You need to join both channels to use this bot.. ♡", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_message(filters.command("start"))
async def start_message(client, message):
    user_id = message.from_user.id
    if users_collection.count_documents({'user_id': user_id}) == 0:
        users_collection.insert_one({'user_id': user_id})
        await client.send_message(chat_id=ADMIN_ID, text=(
            f"💡 New User Alert:\n\n"
            f"👤 User: {message.from_user.mention}\n"
            f"🆔 User ID: {user_id}\n"
            f"📊 Total Users: {users_collection.count_documents({})}"
        ))

    image_urls = [
        "https://graph.org/file/db277a7810a3f65d92f22.jpg",
        "https://graph.org/file/a00f89c5aa75735896e0f.jpg",
        "https://graph.org/file/f86b71018196c5cfe7344.jpg",
        "https://graph.org/file/a3db9af88f25bb1b99325.jpg",
        "https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
        "https://graph.org/file/84de4b440300297a8ecb3.jpg",
        "https://graph.org/file/84e84ff778b045879d24f.jpg",
        "https://graph.org/file/a4a8f0e5c0e6b18249ffc.jpg",
        "https://graph.org/file/ed92cada78099c9c3a4f7.jpg",
        "https://graph.org/file/d6360613d0fa7a9d2f90b.jpg",
        "https://graph.org/file/37248e7bdff70c662a702.jpg",
        "https://graph.org/file/0bfe29d15e918917d1305.jpg",
        "https://graph.org/file/16b1a2828cc507f8048bd.jpg",
        "https://graph.org/file/e6b01f23f2871e128dad8.jpg",
        "https://graph.org/file/cacbdddee77784d9ed2b7.jpg",
        "https://graph.org/file/ddc5d6ec1c33276507b19.jpg",
        "https://graph.org/file/39d7277189360d2c85b62.jpg",
        "https://graph.org/file/5846b9214eaf12c3ed100.jpg",
        "https://graph.org/file/ad4f9beb4d526e6615e18.jpg",
        "https://graph.org/file/3514efaabe774e4f181f2.jpg"
    ]
    photo_url = random.choice(image_urls)

    buttons = [
        [InlineKeyboardButton(" DEVELOPER ", url="https://t.me/UNBORNVILLIAN"),
         InlineKeyboardButton("SUPPORT", url="https://t.me/BOT_BACKUP")],
        [InlineKeyboardButton("TERMS", url="https://t.me/BOT_BACKUP/7"),
         InlineKeyboardButton("CHANNEL", url="https://t.me/BOTMINE_TECH")]
    ]

    caption = f"""**✨ 𝐇𝐞𝐲 {message.from_user.mention}, 𝚆𝙴𝙻𝙲𝙾𝙼𝙴 ✨  
────────────────────  
🔗 𝐒𝐞𝐧𝐝 𝐚𝐧𝐲 𝐓𝐞𝐫𝐚𝐁𝐨𝐱 𝐥𝐢𝐧𝐤...

✅ 𝐈'𝐥𝐥 𝐮𝐧𝐥𝐨𝐜𝐤 𝐢𝐭 & 𝐠𝐢𝐯𝐞 𝐲𝐨𝐮:
📥 𝐅𝐀𝐒𝐓 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤  
▶️ 𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐕𝐢𝐝𝐞𝐨 𝐏𝐥𝐚𝐲𝐞𝐫

💫 𝐍𝐨 𝐥𝐢𝐦𝐢𝐭𝐬. 𝐍𝐨 𝐚𝐝𝐬. 𝐍𝐨 𝐰𝐚𝐢𝐭𝐢𝐧𝐠.  
────────────────────  
💖 𝐄𝐧𝐣𝐨𝐲 𝐭𝐡𝐞 𝐦𝐨𝐬𝐭 𝐩𝐨𝐰𝐞𝐫𝐟𝐮𝐥 𝐓𝐞𝐫𝐚𝐁𝐨𝐱 𝐁𝐨𝐭!**"""
    await client.send_photo(chat_id=message.chat.id, photo=photo_url, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_message(filters.command("help"))
async def help_message(client, message):
    text = """ ⍟─── 𝕄𝕐 ℍ𝔼𝕃ℙ ───⍟

❖ Just send me your TeraBox link.
❖ I will fetch the video link and give you fast download options.
❖ Best bot with secure & fast processing.
❖ NEED HELP? CONTACT DEVELOPER 
"""
    buttons = [[
        InlineKeyboardButton("Updates", url="https://t.me/bot_backup"),
        InlineKeyboardButton("Support", url="https://t.me/bot_backup_support")
    ]]
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

@app.on_message(filters.command("stats"))
async def status_message(client, message):
    user_count = users_collection.count_documents({})
    uptime_minutes = (time.time() - start_time) / 60
    await message.reply_text(f"🌟 Bot uptime: {uptime_minutes:.2f} min\n👥 Users: {user_count}")

@app.on_message(filters.text & ~filters.command(["start", "stats", "help"]))
async def get_video_links(client, message):
    user_id = message.from_user.id
    if not await is_user_in_channel(client, user_id, CHANNEL_1_USERNAME):
        await send_join_prompt(client, message.chat.id)
        return
    if not await is_user_in_channel(client, user_id, CHANNEL_2_USERNAME):
        await send_join_prompt(client, message.chat.id)
        return
    await process_video_request(client, message)

def extract_terabox_id(url: str) -> Optional[str]:
    match = re.search(r'/s/([a-zA-Z0-9]+)', url)
    return match.group(1) if match else None

def fetch_video_details(video_url: str) -> Optional[str]:
    try:
        r = requests.get(video_url, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            tag = soup.find("meta", property="og:image")
            return tag["content"] if tag else None
    except:
        return None

async def process_video_request(client, message):
    video_url = message.text.strip()
    
    if "terabox.com" not in video_url:
        await message.reply_text("❌ Invalid TeraBox link.")
        return

    await message.reply_chat_action(ChatAction.TYPING)
    m = await message.reply_text("Processing your video... Please wait 🥵.")

    try:
        api_url = f"https://teraboxdown.rishuapi.workers.dev/?url={video_url}"
        r = requests.get(api_url, timeout=15)
        response = r.json() if r.status_code == 200 else {}

        file_name = response.get("file_name", "Unknown")
        file_size = response.get("size", "Unknown")
        download_url = response.get("link")
        thumbnail = response.get("thumbnail") or fetch_video_details(video_url) or "https://envs.sh/L75.jpg"

        main_player_url = f"{TERABOX_API}{video_url}"
        web_app_1 = WebAppInfo(url=main_player_url)

        t_id = extract_terabox_id(video_url)
        web_app_2 = WebAppInfo(url=f"https://icy-brook12.arjunavai273.workers.dev/?id={t_id}") if t_id else None

        buttons = []
        if web_app_2:
            buttons.append([InlineKeyboardButton("Play Video", web_app=web_app_2)])
        buttons.append([InlineKeyboardButton("Play Video 2", web_app=web_app_1)])

        caption = (
            f"**User: {message.from_user.mention}\n"
            f"File: `{file_name}`\n"
            f"Size: `{file_size}`\n"
            f"[Download Link]({download_url})**"
        )

        await m.delete()
        await client.send_photo(chat_id=message.chat.id, photo=thumbnail, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))

        dump_caption = (
            f"From {message.from_user.mention}:\n"
            f"File: `{file_name}`\n"
            f"Size: `{file_size}`\n"
            f"[Play 1]({main_player_url}) | [Play 2]({web_app_2.url if web_app_2 else 'N/A'})\n"
            f"[Download]({download_url})"
        )
        await client.send_photo(chat_id=DUMP_CHANNEL, photo=thumbnail, caption=dump_caption)

    except Exception as e:
        await m.delete()
        await message.reply_text(f"Error: {str(e)}")

# Run Flask in a thread
def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask, daemon=True).start()

# Start bot
app.run()
