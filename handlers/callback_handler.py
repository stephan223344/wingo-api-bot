from telegram import Update
from telegram.ext import ContextTypes

from handlers.admin_handler import admin_stats, admin_broadcast_start
from services.api_service import get_prediction
from services.prediction_service import build_message

STICKER_ID = "CAACAgUAAxkBAAIDi2m36V2DW5fQFOzsbGdOVhe_r1ocAAJSAwAC0qoBVU3NipS4NOxCOgQ"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    data = query.data

    try:
        # 🎯 MARKET
        if data.startswith("market_"):
            market = data.split("_")[1]

            prediction = await get_prediction(market)

            if not prediction:
                await query.edit_message_text("❌ API Error")
                return

            msg = build_message(prediction, market)

            # afficher prediction
            await query.edit_message_text(msg)

            # envoyer sticker (optionnel)
            if STICKER_ID:
                await context.bot.send_sticker(
                    chat_id=query.message.chat_id,
                    sticker=STICKER_ID
                )

        # 👑 ADMIN
        elif data == "admin_stats":
            await admin_stats(update, context)

        elif data == "admin_broadcast":
            await admin_broadcast_start(update, context)

    except Exception as e:
        print(f"Callback Error: {e}")
        await query.edit_message_text("⚠️ Une erreur est survenue")