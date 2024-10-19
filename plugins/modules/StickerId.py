import os, glob
from os import error
import logging
import time
import math
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bughunter0 = Client(
    "Sticker-Bot",
    bot_token=os.environ("BOT_TOKEN"),
    api_id=int(os.environ("API_ID")),
    api_hash=os.environ("API_HASH")
)

START_STRING = """Hi {}, I'm Sticker Bot.

I can provide all kinds of sticker options here."""

JOIN_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton('↗ Join Here ↗', url='https://t.me/team_netflix')]]
)

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")

@bughunter0.on_message(filters.command(["start_sticker"]))
async def start_sticker(bot, update):
    text = START_STRING.format(update.from_user.mention)
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=JOIN_BUTTON,
        quote=True
    )

@bughunter0.on_message(filters.command(["ping"]))
async def ping(bot, message):
    start_t = time.time()
    rm = await message.reply_text("Checking")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")

@bughunter0.on_message(filters.command(["getsticker"]))
async def getstickerasfile(bot, message):      
    try:
        tx = await message.reply_text("Downloading...")
        file_path = DOWNLOAD_LOCATION + f"{message.chat.id}.WEBM"
        await message.reply_to_message.download(file_path)   
        await tx.edit("Downloaded")
        await tx.edit("Uploading...")
        await message.reply_document(file_path, caption="©Team_Netflix")
        await tx.delete()   
        os.remove(file_path)
    except Exception as error:
        print(error)

@bughunter0.on_message(filters.command(["clearcache"]))
async def clearcache(bot, message):   
    txt = await message.reply_text("Checking Cache")
    await txt.edit("Clearing cache")
    dir = DOWNLOAD_LOCATION
    filelist = glob.glob(os.path.join(dir, "*"))
    i = 0
    for f in filelist:
        os.remove(f)
        i += 1
    await txt.edit(f"Cleared {i} files") 
    await txt.delete()

@bughunter0.on_message(filters.command(["stickerid"]))
async def stickerid(bot, message):   
    if message.reply_to_message.sticker:
        await message.reply(
            f"**Sticker ID is** \n `{message.reply_to_message.sticker.file_id}`\n\n"
            f"**Unique ID is** \n\n`{message.reply_to_message.sticker.file_unique_id}`",
            quote=True
        )
    else: 
        await message.reply("Oops! Not a sticker file.")

@bughunter0.on_message(filters.command(["findsticker"]))
async def findsticker(bot, message):  
    try:
        txt = await message.reply_text("Validating Sticker ID")
        stickerid = str(message.reply_to_message.text)
        chat_id = str(message.chat.id)
        await txt.delete()
        await bot.send_sticker(chat_id, stickerid)
    except Exception as error:
        await message.reply_text("Not a valid file ID")
