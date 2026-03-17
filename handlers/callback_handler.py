################Bouton

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.admin_handler import admin_stats, admin_broadcast_start
from services.api_service import get_prediction
from services.prediction_service import build_message
from utils.user_store import get_users

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("market_"):
        market = data.split("_")[1]

        prediction = await get_prediction(market)

        if not prediction:
            await query.edit_message_text("API Error ❌")
            return

        msg = build_message(prediction, market)

        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data=data)]
        ]

        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "admin_stats":
        await admin_stats(update, context)

    elif data == "admin_broadcast":
        await admin_broadcast_start(update, context)