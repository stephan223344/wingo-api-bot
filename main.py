import sys
sys.stdout.reconfigure(encoding='utf-8')

from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import BOT_TOKEN, CHANNEL_ID
from handlers.start_handler import start
from handlers.menu_handler import menu_handler
from handlers.callback_handler import callback_handler

from services.api_service import get_prediction
from services.prediction_service import build_message

async def auto_post(context):
    prediction = await get_prediction("1")

    if not prediction:
        return

    msg = build_message(prediction, "1")

    await context.bot.send_message(chat_id=CHANNEL_ID, text=msg)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))

    app.job_queue.run_repeating(auto_post, interval=300, first=10)

    print("Bot started clean version")
    app.run_polling()


if __name__ == "__main__":
    main()