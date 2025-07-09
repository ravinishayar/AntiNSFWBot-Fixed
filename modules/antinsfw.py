import os
import traceback
import datetime
from pymongo import MongoClient
from pyrogram import Client, filters, types as t
from modules.utils.misc import getFileId
from modules.utils.api import isNsfw

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["AntiNSFW"]  # Database name
logs_collection = db["nsfw_logs"]  # Collection name

print("👀 antinsfw.py loaded")

@Client.on_message(
    (filters.document | filters.photo | filters.sticker | filters.animation | filters.video)
    & ~filters.private,
    group=9,
)
async def NSFW(_: Client, message: t.Message):
    print("📩 NSFW Handler Triggered")
    if not message.from_user:
        return

    fileId = getFileId(message)
    if not fileId:
        print("⚠️ No FileID found.")
        return

    file = await _.download_media(fileId)
    print(f"📥 Downloaded media: {file}")

    unsafe = await isNsfw(file)
    print(f"🔍 NSFW Detection Result: {unsafe}")

    if unsafe is True:
        try:
            await message.delete()
            print(f"✅ Deleted NSFW content from {message.from_user.first_name}")

            logs_collection.insert_one({
                "user_id": message.from_user.id,
                "username": message.from_user.username,
                "chat_id": message.chat.id,
                "chat_title": message.chat.title,
                "message_id": message.id,
                "date": datetime.datetime.utcnow(),
                "file_id": fileId,
                "nsfw": True
            })
            print("📦 Logged NSFW content to MongoDB.")
        except Exception as e:
            print(f"❌ Failed to delete message: {e}")
            traceback.print_exc()
