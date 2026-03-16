import os
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

BASE_URL = "https://indialotteryapi.com/wp-json/wingo/v1"

USERS_FILE = "users.txt"

broadcast_mode = False


# ---------------- USERS ---------------- #

def save_user(user_id):

    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()

    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")


def get_users():

    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r") as f:
        return f.read().splitlines()


# ---------------- PERIOD ---------------- #


def generate_period(market: float):

    ist = pytz.timezone("Asia/Kolkata")
    ist_now = datetime.now(ist)

    date_str = ist_now.strftime("%Y%m%d")

    prefix = "1000"

    if market == 1:
        market_code = "1"
        interval = 60
    elif market == 3:
        market_code = "2"
        interval = 180
    elif market == 5:
        market_code = "3"
        interval = 300
    else:
        market_code = "5"
        interval = 30

    midnight = ist_now.replace(hour=0, minute=0, second=0, microsecond=0)

    seconds_since_midnight = int((ist_now - midnight).total_seconds())

    counter = (seconds_since_midnight // interval) + 1

    counter = counter - 326

    counter_str = str(counter % 10000).zfill(4)

    return f"{date_str}{prefix}{market_code}{counter_str}"


# ---------------- API ---------------- #

def get_prediction(market):

    try:

        r = requests.get(
            f"{BASE_URL}/predict",
            params={"market": market},
            timeout=10
        )

        data = r.json()

        if "items" not in data:
            return None

        return data["items"][0]

    except:
        return None


def build_message(prediction, market):

    period = generate_period(float(market))

    return (

        f"🎰 Prediction for winGO {market} MIN 🎰\n\n"

        f"📅 Period: {period}\n"

        f"💸 Purchase: {prediction['bigSmall']}\n\n"

        f"🔮 Risky Predictions:\n"

        f"👉 Colour: {prediction['color']}\n"

        f"👉 Numbers: {prediction['digit']} or {(prediction['digit']+2)%10}\n\n"

        f"💡 Strategy Tip:\nUse 2x strategy\n\n"

        f"📊 Fund Management:\n5 level management"
    )


# ---------------- AUTO POST ---------------- #

async def post_prediction(context: ContextTypes.DEFAULT_TYPE):

    prediction = get_prediction("1")

    if not prediction:
        return

    msg = build_message(prediction, "1")

    await context.bot.send_message(chat_id=CHANNEL_ID, text=msg)


# ---------------- MENUS ---------------- #

def main_menu_keyboard(user_id):

    keyboard = [

        ["🎰 Prediction"],

        ["🔗 Register"],

        ["📢 Channel"]

    ]

    if user_id == ADMIN_ID:
        keyboard.append(["🛠 Admin"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


async def show_market_menu(update):

    keyboard = [

        [InlineKeyboardButton("30 Seconds", callback_data="market_0.5")],

        [InlineKeyboardButton("1 Minute", callback_data="market_1")],

        [InlineKeyboardButton("3 Minutes", callback_data="market_3")],

        [InlineKeyboardButton("5 Minutes", callback_data="market_5")]

    ]

    await update.message.reply_text(
        "Choose Market 🎰",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_admin_menu(update):

    keyboard = [

        [InlineKeyboardButton("📊 Bot Stats", callback_data="admin_stats")],

        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")]

    ]

    await update.message.reply_text(
        "Admin Panel 🛠",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- START ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    save_user(user_id)

    await update.message.reply_text(
        "🚀 Welcome to Wingo Predict Bot PRO
        🎮 The Best Betting Platforms ! 🔥
        Join the community 👉 @Jalwa_Game_Channel
        Tutorials, Gifts, Subscribe to Me! 🥰🎁 💶
        
        Please select an option below :",
        reply_markup=main_menu_keyboard(user_id)
    )


# ---------------- MENU HANDLER ---------------- #

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global broadcast_mode

    text = update.message.text

    user_id = update.effective_user.id

    if text == "🎰 Prediction":

        await show_market_menu(update)

    elif text == "🔗 Register":

        await update.message.reply_text(
            "Register here:\nhttps://k3jalp2.com/#/register?invitationCode=44233100104"
        )

    elif text == "📢 Channel":

        await update.message.reply_text(
            "Join channel:\nhttps://t.me/gowintest"
        )

    elif text == "🛠 Admin":

        if user_id != ADMIN_ID:
            return

        await show_admin_menu(update)

    elif broadcast_mode and user_id == ADMIN_ID:

        users = get_users()

        sent = 0

        for user in users:

            try:

                await context.bot.send_message(chat_id=user, text=text)

                sent += 1

            except:
                pass

        broadcast_mode = False

        await update.message.reply_text(f"Broadcast sent to {sent} users")


# ---------------- CALLBACKS ---------------- #

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global broadcast_mode

    query = update.callback_query

    await query.answer()

    data = query.data

    if data.startswith("market_"):

        market = data.split("_")[1]

        prediction = get_prediction(market)

        if not prediction:

            await query.edit_message_text("API Error ❌")

            return

        msg = build_message(prediction, market)

        keyboard = [

            [InlineKeyboardButton("🔄 New Prediction", callback_data=data)]

        ]

        await query.edit_message_text(
            msg,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "admin_stats":

        users = len(get_users())

        await query.edit_message_text(
            f"📊 BOT STATS\n\nUsers: {users}"
        )

    elif data == "admin_broadcast":

        broadcast_mode = True

        await query.edit_message_text(
            "Send message to broadcast."
        )


# ---------------- MAIN ---------------- #

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    app.add_handler(CallbackQueryHandler(button_handler))

    app.job_queue.run_repeating(
        post_prediction,
        interval=300,
        first=10
    )

    print("Bot started")

    app.run_polling()


if __name__ == "__main__":
    main()
