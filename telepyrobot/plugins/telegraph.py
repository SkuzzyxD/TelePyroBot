import os
import time
from datetime import datetime
from telegraph import upload_file
from pyrogram import Client, filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Paste media to telegraph!

`{COMMAND_HAND_LER}telegraph`: As a reply to a media to paste it to Telegraph.
"""


@Client.on_message(filters.command("telegraph", COMMAND_HAND_LER) & filters.me)
async def telegraph(c: Client, m: Message):
    replied = m.reply_to_message
    start_t = datetime.now()
    await m.edit("`Trying to paste to telegraph...`", parse_mode="md")
    if not replied:
        await m.edit("reply to a supported media file")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (
            replied.video
            and replied.video.file_name.endswith(".mp4")
            and replied.video.file_size <= 5242880
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4")
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await m.edit("**Not supported!**", parse_mode="md")
        return
    download_location = await client.download_media(
        message=m.reply_to_message, file_name="telepyrobot/downloads/"
    )
    await m.edit("`Pasting to telegraph...`", parse_mode="md")
    try:
        response = upload_file(download_location)
    except Exception as document:
        await m.edit(document)
    else:
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        await m.edit(
            f"**Document Passed to** [Telegra.ph](https://telegra.ph{response[0]}) **in __{ms}__ seconds**",
            parse_mode="md",
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)
