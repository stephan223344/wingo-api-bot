from utils.period import generate_period

def build_message(prediction: dict, market: str) -> str:
    period = generate_period(float(market))
    digit = prediction["digit"]

    return f"""
🎰 Prediction for winGO {market} MIN 🎰

📅 Period: {period}
💸 Purchase: {prediction['bigSmall']}

🔮 Risky Predictions:
👉 Color: {prediction['color']}
👉 Numbers: {digit} or {(digit + 2) % 10}

💡 Strategy Tip:
Use 2x strategy

📊 Fund Management:
5 level management
"""
