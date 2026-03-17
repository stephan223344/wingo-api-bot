from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN_ID

def main_menu(user_id: int):
    keyboard = [
        ["🎰 Prediction"],
        ["🔗 Register Link"],
        ["📢 Prediction Channel"]
    ]

    if user_id == ADMIN_ID:
        keyboard.append(["🛠 Admin"])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def market_menu():
    keyboard = [
        [InlineKeyboardButton("1 Minute", callback_data="market_1")],
        [InlineKeyboardButton("3 Minutes", callback_data="market_3")],
        [InlineKeyboardButton("5 Minutes", callback_data="market_5")],
    ]
    return InlineKeyboardMarkup(keyboard)


def admin_menu():
    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data="admin_stats")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")]
    ]
    return InlineKeyboardMarkup(keyboard)