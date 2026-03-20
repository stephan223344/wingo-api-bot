import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

from config import BOT_TOKEN, CHANNEL_ID
from handlers.start_handler import start
from handlers.menu_handler import menu_handler
from handlers.callback_handler import callback_handler
from handlers.sticker_handler import get_sticker_id
from services.api_service import get_prediction
from services.prediction_service import build_message
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

# Handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
application.add_handler(CallbackQueryHandler(callback_handler))
application.add_handler(MessageHandler(filters.Sticker.ALL, get_sticker_id))

# Auto-post job
async def auto_post(context: ContextTypes.DEFAULT_TYPE):
    try:
        prediction = await get_prediction("1")
        if not prediction:
            return

        msg = build_message(prediction, "1")
        photo_path = "ads/small.jpg" if prediction["bigSmall"] == "Small" else "ads/big.jpg"

        keyboard = [[InlineKeyboardButton("🔥 PLAY NOW", url="https://k3jalp2.com/#/register?invitationCode=44233100104")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        with open(photo_path, "rb") as photo:
            await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=photo,
                caption=msg,
                reply_markup=reply_markup
            )

        await context.bot.send_sticker(
            chat_id=CHANNEL_ID,
            sticker="CAACAgUAAxkBAAIDi2m36V2DW5fQFOzsbGdOVhe_r1ocAAJSAwAC0qoBVU3NipS4NOxCOgQ"
        )
    except Exception as e:
        print(f"Autopost error: {e}")

application.job_queue.run_repeating(auto_post, interval=300, first=10)

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

# Vercel lance automatiquement app comme point d’entrée
