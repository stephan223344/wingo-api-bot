import requests
from datetime import datetime, timedelta
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8404084903:AAF96AkaMJgePNfYro0zEFmSHvWbsbCocGo"
BASE_URL = "https://indialotteryapi.com/wp-json/wingo/v1"


# Générer une période en temps réel (comme ton code Node.js)
def generate_period(market: float) -> str:
    ist = pytz.timezone("Asia/Kolkata")
    ist_now = datetime.now(ist)

    # Date AAAAMMJJ
    date_str = ist_now.strftime("%Y%m%d")

    prefix = "1000"

    # Code marché
    if market == 1:
        market_code = "1"
    elif market == 3:
        market_code = "2"
    elif market == 5:
        market_code = "3"
    else:
        market_code = "5"  # par défaut 30s

    # Calcul du nombre de périodes de 5 minutes écoulées depuis minuit
    midnight = ist_now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_since_midnight = int((ist_now - midnight).total_seconds())
    base_count_5min = seconds_since_midnight // (5 * 60)

    # Adapter selon le marché choisi
    if market == 5:
        counter = base_count_5min
    else:
        counter = round(base_count_5min * (5 / market))

    counter_str = str(counter % 10000).zfill(4)

    return f"{date_str}{prefix}{market_code}{counter_str}"

#menu principale
async def show_menu(query_or_update, context):
    keybord = [
        [InlineKeyboardButton("30s", callback_data="market_0.5")],
        [InlineKeyboardButton("1 min", callback_data="market_1")],
        [InlineKeyboardButton("3 min", callback_data="market_3")],
        [InlineKeyboardButton("5 min", callback_data="market_5")]
    ]
    reply_markup = InlineKeyboardMarkup(keybord)

    #si c'est une message classique
    if isinstance(query_or_update, Update):
        await query_or_update.message.reply_text("Choisis ton marche 🎰:", reply_markup=reply_markup)
    else:
        # Si c'est un callback (Retour au menu)
        await query_or_update.edit_message_text("Choisis ton marche 🎰", reply_markup=reply_markup)

# Commande /start avec bouton
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_menu(update, context)

# Callback quand on clique sur le bouton
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("market_"):
        market_str = query.data.split("_")[1]   # "0.5", "1", "3", "5"
        r = requests.get(f"{BASE_URL}/predict", params={"market": market_str})
        data = r.json()

        if "items" not in data or not data["items"]:
            await query.edit_message_text(text=f"Erreur API: {data}")
            return

        prediction = data["items"][0]
        real_period = generate_period(float(market_str))

        
        msg = (
            f"🎰 Prediction for winGO {market_str} MIN 🎰\n\n"
            f"📅 Period: {real_period}\n"
            f"💸 Purchase: {prediction['bigSmall']}\n\n"
            f"🔮 Risky Predictions:\n"
            f"👉🏻 Colour: {prediction['color']}\n"
            f"👉🏻 Numbers: {prediction['digit']} or {(prediction['digit']+2) % 10}\n \n"
            f"💡 Strategy Tip: \n Use the 2x strategy for better chances of profit and winning.\n"     
            f"📊 Fund Management: \n Always play through fund management 5 level.\n"

        )

        keyboard = [
            [InlineKeyboardButton("🔄 Nouvelle prédiction", callback_data=f"market_{market_str}")],
            [InlineKeyboardButton("⬅️ Retour au menu", callback_data="menu")]
            
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text=msg, reply_markup=reply_markup)

    elif query.data == "menu":
        await show_menu(query, context)
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot en cours d'execution...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
