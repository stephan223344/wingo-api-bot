from telegram import Update
from telegram.ext import ContextTypes

async def get_sticker_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 🔒 sécurité
    if not update.message or not update.message.sticker:
        return

    file_id = update.message.sticker.file_id

    print(f"Sticker ID: {file_id}")

    await update.message.reply_text(
        f"✅ Sticker ID récupéré:\n{file_id}"
    )