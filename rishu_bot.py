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

# Bot details from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
CHANNEL_1_USERNAME = "Rishucoder"
CHANNEL_2_USERNAME = "Rishu_mood"
API_HASH = "42a60d9c657b106370c79bb0a8ac560c"
API_ID = "14050586"
TERABOX_API = "https://terabox-player.rishuapi.workers.dev/?url="
DUMP_CHANNEL = "-1002561334306"
ADMIN_ID = int(os.getenv("ADMIN_ID", "5738579437"))

# Flask app for monitoring
flask_app = Flask(__name__)
start_time = time.time()

# MongoDB setup
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[os.getenv("MONGO_DB_NAME", "Rishu-free-db")]
users_collection = db[os.getenv("MONGO_COLLECTION_NAME", "users")]

# Pyrogram bot client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@flask_app.route('/')
def home():
    uptime_minutes = (time.time() - start_time) / 60
    user_count = users_collection.count_documents({})
    return f"Bot uptime: {uptime_minutes:.2f} minutes\nUnique users: {user_count}"

async def is_user_in_channel(fclient, user_id, channel_username):
    try:
        await fclient.get_chat_member(channel_username, user_id)
        return True
    except UserNotParticipant:
        return False
    except Exception:
        return False

async def send_join_prompt(client, chat_id):
    join_button_1 = InlineKeyboardButton("♡ Join ♡", url=f"https://t.me/{CHANNEL_1_USERNAME}")
    join_button_2 = InlineKeyboardButton("♡ Join ♡", url=f"https://t.me/{CHANNEL_2_USERNAME}")
    markup = InlineKeyboardMarkup([[join_button_1], [join_button_2]])
    await client.send_message(
        chat_id,
        "♡ You need to join both channels to use this bot.. ♡",
        reply_markup=markup,
    )

@app.on_message(filters.command("start"))
async def start_message(client, message):
    user_id = message.from_user.id
    if users_collection.count_documents({'user_id': user_id}) == 0:
        users_collection.insert_one({'user_id': user_id})
        await client.send_message(
            chat_id=ADMIN_ID,
            text=f"💡 **New User Alert**:\n👤 **User:** {message.from_user.mention}\n🆔 **User ID:** `{user_id}`\n📊 **Total Users:** {users_collection.count_documents({})}"
        )

    image_urls = [ # truncated for brevity ]
    random_image = random.choice(image_urls)

    join_button_1 = InlineKeyboardButton("˹ υᴘᴅᴧᴛєs ˼", url="https://t.me/Ur_rishu_143")
    join_button_2 = InlineKeyboardButton("˹ ᴧʟʟ ʙσᴛ's ˼", url="https://t.me/vip_robotz")
    support_button = InlineKeyboardButton('˹ sυᴘᴘσʀᴛ ˼', url='https://t.me/Ur_support07')
    api_button = InlineKeyboardButton('˹ ᴧʟʟ ᴧᴘɪ ˼', url='https://t.me/RishuApi')
    markup = InlineKeyboardMarkup([[join_button_1, join_button_2], [support_button, api_button]])

    await client.send_photo(
        chat_id=message.chat.id,
        photo=random_image,
        caption=f"""**┌────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼──────•
┆◍ ʜᴇʏ {message.from_user.mention} !
└──────────────────────•
» ✦ ϻσsᴛ ᴘσᴡєꝛғυʟʟ ᴛєꝛᴧʙσx ʙσᴛ  
» ✦ ʙєsᴛ ғєᴧᴛυꝛє ʙσᴛ ση ᴛєʟєɢꝛᴧϻ 
» ✦ ʙєsᴛ ᴘʟᴧʏєꝛ ʙσᴛ
» ✦ ғᴧsᴛ ᴅσᴡηʟσᴧᴅ sυᴘᴘσꝛᴛєᴅ
» ✦ ησ ʟᴧɢ, ғᴧsᴛ ᴧηᴅ sєᴄυꝛє 
» ✦ ᴘꝛєϻɪυϻ ғєᴧᴛυꝛєs
•──────────────────────•
❖ 𝐏ᴏᴡᴇʀᴇᴅ ʙʏ  »»  [˹ʀɪsʜυ ʙσᴛ˼ ](t.me/ur_rishu_143) 
•──────────────────────•**""",
        reply_markup=markup
    )

@app.on_message(filters.command("Rishu"))
async def status_message(client, message):
    user_count = users_collection.count_documents({})
    uptime_minutes = (time.time() - start_time) / 60
    await message.reply_text(f"💫 Bot uptime: {uptime_minutes:.2f} minutes\n👥 Total unique users: {user_count}")

@app.on_message(filters.command("help"))
async def status_message(client, message):
    text = (
        "** ⍟─── ϻʏ ʜєʟᴘ ───⍟**\n\n"
        "**───────────────────────**\n"
        "**❖ ɪ ᴧϻ ϻσsᴛ ᴘσʷєʀғυʟʟ ᴛєꝛᴧʙσx ʙσᴛ**\n\n"
        "**● ᴊυsᴛ sєηᴅ ϻє ʏσυꝛ ᴛєꝛᴧʙσx ʟɪηᴋ ᴧηᴅ sєє ϻᴧɢɪᴄ **\n"
        "**───────────────────────**\n"
        "**❖ υᴘᴅᴧᴛєs ➥ [ʀɪsʜυ](https://t.me/Ur_rishu_143)**\n"
        "**❖ sυᴘᴘσʀᴛ ➥ [ʀɪsʜυ sυᴘᴘσʀᴛ ](https://t.me/Vip_robotz)**\n"
        "**❖ σᴡηєʀ ➥ [ʀɪsʜυ](https://t.me/Rishu1286)**\n"
        "**───────────────────────**"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("˹ υᴘᴅᴧᴛєs ˼", url="https://t.me/Ur_rishu_143")],
        [InlineKeyboardButton("˹ sυᴘᴘσʀᴛ ˼", url="https://t.me/Vip_robotz"),
         InlineKeyboardButton(" ˹ ʀɪsʜυ ˼", url="https://t.me/Rishu1286")]
    ])
    await message.reply_text(text, reply_markup=buttons, disable_web_page_preview=True)

@app.on_message(filters.text & ~filters.command(["start", "status"]))
async def get_video_links(client, message):
    user_id = message.from_user.id
    if not await is_user_in_channel(client, user_id, CHANNEL_1_USERNAME):
        await send_join_prompt(client, message.chat.id)
        return
    if not await is_user_in_channel(client, user_id, CHANNEL_2_USERNAME):
        await send_join_prompt(client, message.chat.id)
        return
    await process_video_request(client, message)

def fetch_video_details(video_url: str) -> Optional[str]:
    try:
        response = requests.get(video_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.find("meta", property="og:image")["content"] if soup.find("meta", property="og:image") else None
    except requests.exceptions.RequestException:
        return None

def extract_terabox_id(url: str) -> Optional[str]:
    match = re.search(r'/s/([a-zA-Z0-9]+)', url)
    return match.group(1) if match else None

async def process_video_request(client, message):
    video_url = message.text.strip()
    await message.reply_chat_action(ChatAction.TYPING)
    processing_msg = await message.reply_text("**🔄 Processing your video \n\n 🤩Please wait 30 to 40 second....🫰🏻**")
    try:
        api_url = f"https://teraboxdown.rishuapi.workers.dev/?url={video_url}"
        response = requests.get(api_url).json()
        file_name = response.get("file_name", "Unknown")
        file_size = response.get("size", "Unknown")
        download_url = response.get("link")
        thumbnail = response.get("thumbnail") or fetch_video_details(video_url) or "https://envs.sh/L75.jpg"
        main_player_url = f"{TERABOX_API}{video_url}"
        web_app_1 = WebAppInfo(url=main_player_url)
        terabox_id = extract_terabox_id(video_url)
        web_app_2 = WebAppInfo(url=f"https://icy-brook12.arjunavai273.workers.dev/?id={terabox_id}") if terabox_id else None
        buttons = [[InlineKeyboardButton(" PLAY VIDEO ", web_app=web_app_2)]]
        if web_app_2:
            buttons.append([InlineKeyboardButton(" PLAY VIDEO 2 ", web_app=web_app_1)])
        markup = InlineKeyboardMarkup(buttons)
        caption = (
            f"**Dear: 🤩 {message.from_user.mention}\n\n"
            f"📦 File Name: `{file_name}`\n\n"
            f"📁 Size: `{file_size}`\n"
            f"💡 Download Here [Link]({download_url})**\n\n"
            f"**💾Here's your video:**"
        )
        await processing_msg.delete()
        await client.send_photo(chat_id=message.chat.id, photo=thumbnail, caption=caption, reply_markup=markup, has_spoiler=True)
        dump_caption = (
            f"From {message.from_user.mention}:\n"
            f"File: `{file_name}`\n"
            f"Size: `{file_size}`\n"
            f"Play video: [Player](https://icy-brook12.arjunavai273.workers.dev/?id={terabox_id})\n"
            f"Play video 2: [Player 2]({main_player_url})\n"
            f"Download Video: [Download Link]({download_url})"
        )
        await client.send_photo(chat_id=DUMP_CHANNEL, photo=thumbnail, caption=dump_caption)
    except requests.exceptions.RequestException as e:
        await message.reply_text(f"Error connecting to the API: {str(e)}")

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

flask_thread = Thread(target=run_flask)
flask_thread.start()

app.run()
