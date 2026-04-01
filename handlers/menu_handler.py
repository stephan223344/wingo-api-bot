from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menus import market_menu, admin_menu
from config import ADMIN_ID
from handlers.admin_handler import handle_broadcast
from utils.user_store import save_user


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # sécurité
    if not update.message:
        return

    text = update.message.text
    user_id = update.effective_user.id

    # 🎯 gestion broadcast (priorité)
    if context.user_data.get("broadcast"):
        await handle_broadcast(update, context)
        return

    # 🎰 Prediction
    if text == "🎰 Prediction":
        await update.message.reply_text(
            "Choose Market 🎰",
            reply_markup=market_menu()
        )

    # 🔗 Register
    elif text == "🔗 Register Link":
        await update.message.reply_text(
            "🔗 Register Link:\nhttps://www.jaiclub.me/#/register"
        )

    # 📢 Channel
    elif text == "📢 Prediction Channel":
        await update.message.reply_text(
            "✅ Fast Predictions:\nhttps://t.me/jaiclub_official_channel"
        )

    # 🛠 Admin
    elif text == "🛠 Admin" and user_id == ADMIN_ID:
        await update.message.reply_text(
            "Admin Panel",
            reply_markup=admin_menu()
        )

    user_id = update.effective_user.id
    save_user(user_id)   