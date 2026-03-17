##################Logique admin

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID
from utils.user_store import get_users


# 📊 Stats
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    users = len(get_users())

    await update.callback_query.edit_message_text(
        f"📊 BOT STATS\n\nUsers: {users}"
    )


# 📢 Activer broadcast
async def admin_broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    context.user_data["broadcast"] = True

    await update.callback_query.edit_message_text(
        "Send message to broadcast."
    )


# 📤 Envoyer broadcast
async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.user_data.get("broadcast"):
        return

    users = get_users()
    sent = 0

    for user in users:
        try:
            await context.bot.send_message(chat_id=user, text=update.message.text)
            sent += 1
        except:
            pass

    context.user_data["broadcast"] = False

    await update.message.reply_text(f"Broadcast sent to {sent} users")