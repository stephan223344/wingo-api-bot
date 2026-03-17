from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menus import main_menu
from utils.user_store import save_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    await update.message.reply_text(
        "🚀 Welcome to Wingo Predict Bot PRO 🎮 The Best Betting Platforms ! 🔥 Join the community 👉 @Jalwa_Game_Channel Tutorials, Gifts, Subscribe to Me! 🥰🎁 💶 Please select an option below :",
        reply_markup=main_menu(user_id)
    )