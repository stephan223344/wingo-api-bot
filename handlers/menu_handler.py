#########Navigation

from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menus import market_menu, admin_menu
from config import ADMIN_ID
from utils.user_store import get_users
from handlers.admin_handler import handle_broadcast

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "🎰 Prediction":
        await update.message.reply_text("Choose Market 🎰", reply_markup=market_menu())

    elif text == "🔗 Register":
        await update.message.reply_text("https://k3jalp2.com/#/register?invitationCode=44233100104")

    elif text == "📢 Channel":
        await update.message.reply_text("https://t.me/gowintest")

    elif text == "🛠 Admin" and user_id == ADMIN_ID:
        await update.message.reply_text("Admin Panel", reply_markup=admin_menu())

    elif context.user_data.get("broadcast"):
        await handle_broadcast(update, context)

        for user in get_users:
            try:
                await context.bot.send_message(chat_id=user, text=text)
                sent += 1
            except:
                pass

        context.user_data["broadcast"] = False
        await update.message.reply_text(f"Sent to {sent} users")