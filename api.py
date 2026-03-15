import os
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = "https://indialotteryapi.com/wp-json/wingo/v1"
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Générer une période en temps réel
def generate_period(market: float) -> str:
    ist = pytz.timezone("Asia/Kolkata")
    ist_now = datetime.now(ist)

    date_str = ist_now.strftime("%Y%m%d")
    prefix = "1000"

    if market == 1:
        market_code = "1"
    elif market == 3:
        market_code = "2"
    elif market == 5:
        market_code = "3"
    else:
        market_code = "5"

    midnight = ist_now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_since_midnight = int((ist_now - midnight).total_seconds())

    base_count_5min = seconds_since_midnight // (5 * 60)

    if market == 5:
        counter = base_count_5min
    else:
        counter = int(base_count_5min * (5 / market))

    counter_str = str(counter % 10000).zfill(4)

    return f"{date_str}{prefix}{market_code}{counter_str}"


# Récupération prediction API
def get_prediction(market):
    try:
        r = requests.get(f"{BASE_URL}/predict", params={"market": market}, timeout=10)
        data = r.json()

        if "items" not in data or not data["items"]:
            return None

        return data["items"][0]

    except Exception as e:
        print("API ERROR:", e)
        return None


# Message prediction
def build_message(prediction, market):

    real_period = generate_period(float(market))

    return (
        f"🎰 Prediction for winGO {market} MIN 🎰\n\n"
        f"📅 Period: {real_period}\n"
        f"💸 Purchase: {prediction['bigSmall']}\n\n"
        f"🔮 Risky Predictions:\n"
        f"👉 Colour: {prediction['color']}\n"
        f"👉 Numbers: {prediction['digit']} or {(prediction['digit']+2) % 10}\n\n"
        f"💡 Strategy Tip:\nUse the 2x strategy for better chances.\n\n"
        f"📊 Fund Management:\nAlways play through fund management 5 level."
    )


# Publication automatique dans channel
async def post_prediction(context: ContextTypes.DEFAULT_TYPE):

    market = "1"

    prediction = get_prediction(market)

    if not prediction:
        return

    msg = build_message(prediction, market)

    await context.bot.send_message(chat_id=CHANNEL_ID, text=msg)


# Menu principal
async def show_menu(update_or_query, context):

    keyboard = [
        [InlineKeyboardButton("30s", callback_data="market_0.5")],
        [InlineKeyboardButton("1 min", callback_data="market_1")],
        [InlineKeyboardButton("3 min", callback_data="market_3")],
        [InlineKeyboardButton("5 min", callback_data="market_5")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text("Choose your market 🎰:", reply_markup=reply_markup)
    else:
        await update_or_query.edit_message_text("Choose your market 🎰:", reply_markup=reply_markup)


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Chat ID :", update.effective_chat.id)
    await show_menu(update, context)


# Boutons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data.startswith("market_"):

        market = query.data.split("_")[1]

        prediction = get_prediction(market)

        if not prediction:
            await query.edit_message_text("Error API ❌")
            return

        msg = build_message(prediction, market)

        keyboard = [
            [InlineKeyboardButton("🔄 New prediction", callback_data=f"market_{market}")], 
            [InlineKeyboardButton("⬅️ Back", callback_data="menu")]
        ]

        await query.edit_message_text(
            text=msg,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "menu":
        await show_menu(query, context)


# MAIN
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # job automatique
    app.job_queue.run_repeating(post_prediction, interval=300, first=10)

    print("Bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()
