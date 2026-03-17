import sys
sys.stdout.reconfigure(encoding='utf-8')

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.ext import MessageHandler, filters
from config import BOT_TOKEN, CHANNEL_ID
from handlers.start_handler import start
from handlers.menu_handler import menu_handler
from handlers.callback_handler import callback_handler
from handlers.sticker_handler import get_sticker_id
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
from services.api_service import get_prediction
from services.prediction_service import build_message

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

async def auto_post(context: ContextTypes.DEFAULT_TYPE):
    try:
        prediction = await get_prediction("1")

        if not prediction:
            return

        msg = build_message(prediction, "1")

        if prediction["bigSmall"] == "Small":
            photo_path = "ads/small.jpg"
        else:
            photo_path = "ads/big.jpg"
        
        keyboard = [
            [InlineKeyboardButton("🔥 PLAY NOW", url="https://k3jalp2.com/#/register?invitationCode=44233100104")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        with open(photo_path, "rb") as photo:
            await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=photo,
                caption=msg,
                read_markup=reply_markup
            )

        await context.bot.send_sticker(chat_id=CHANNEL_ID,
                                       sticker="CAACAgUAAxkBAAIDi2m36V2DW5fQFOzsbGdOVhe_r1ocAAJSAwAC0qoBVU3NipS4NOxCOgQ"
                                       )
    except Exception as e:
        print(f"Autopost error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.Sticker.ALL, get_sticker_id))

    app.job_queue.run_repeating(auto_post, interval=300, first=10)
    print('gooooooooooo')

    app.run_polling()


if __name__ == "__main__":
    main()