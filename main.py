import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)
from config import BOT_TOKEN, CHANNEL_ID
from handlers.start_handler import start
from handlers.menu_handler import menu_handler
from handlers.callback_handler import callback_handler
from handlers.sticker_handler import get_sticker_id
from services.api_service import get_prediction
from services.prediction_service import build_message

# ─── Flask keep-alive server ──────────────────────────────────────────────────
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "✅ Wingo Bot is running!", 200

@flask_app.route("/health")
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# ─── Auto-post job ────────────────────────────────────────────────────────────
async def auto_post(context: ContextTypes.DEFAULT_TYPE):
    try:
        prediction = await get_prediction("1")
        if not prediction:
            return

        msg = build_message(prediction, "1")

        photo_path = "ads/small.jpg" if prediction["bigSmall"] == "Small" else "ads/big.jpg"

        keyboard = [[InlineKeyboardButton(
            "🔥 PLAY NOW",
            url="https://www.jaiclub.me/#/"  ###"https://k3jalp2.com/#/register?invitationCode=44233100104"
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        for channel in CHANNEL_ID:
            try:
                with open(photo_path, "rb") as photo:
                    await context.bot.send_photo(
                        chat_id=channel.strip(),
                        photo=photo,
                        caption=msg,
                        reply_markup=reply_markup
                    )

                await context.bot.send_sticker(
                    chat_id=channel.strip(),
                    sticker="CAACAgUAAxkBAAIDi2m36V2DW5fQFOzsbGdOVhe_r1ocAAJSAwAC0qoBVU3NipS4NOxCOgQ"
                )
                print(f"Message sent to {channel}")
            except Exception as e:
                print(f"Error sending to {channel} : {e}")
    except Exception as e:
        print(f"Autopost error: {e}")

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    # Démarrer Flask dans un thread séparé (keep-alive pour Render)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.Sticker.ALL, get_sticker_id))

    app.job_queue.run_repeating(auto_post, interval=10000, first=10)

    print("✅ Bot started (polling + Flask keep-alive)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()