from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from utils.user_store import get_users
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# 📊 Stats
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    users = len(get_users() or [])

    await update.callback_query.edit_message_text(
        f"📊 BOT STATS\n\nUsers: {users}"
    )


# 📢 Activer broadcast
async def admin_broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    context.user_data["broadcast"] = True

    await update.callback_query.edit_message_text(
        "📢 Send message to broadcast."
    )


# 📤 Envoyer broadcast
async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.user_data.get("broadcast"):
        return

    users = get_users() or []
    sent = 0

    keyboard = [
        [InlineKeyboardButton("🔥 PLAY NOW", url="https://k3jalp2.com/#/register?invitationCode=44233100104")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user,
                text=update.message.text,
                reply_markup=reply_markup
            )
            sent += 1
        except Exception as e:
            print(f"Error sending to {user}: {e}")

    context.user_data["broadcast"] = False

    await update.message.reply_text(
        f"✅ Broadcast sent to {sent} users"
    )