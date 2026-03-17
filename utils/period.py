from datetime import datetime
import pytz

def generate_period(market: float) -> str:
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    date_str = now.strftime("%Y%m%d")
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    seconds = int((now - midnight).total_seconds())
    base_counter = seconds // 30 - 657

    mapping = {
        0.5: base_counter,
        1: round(base_counter / 2),
        3: round(base_counter / 6),
        5: round(base_counter / 10),
    }

    market_code = {1: "1", 3: "2", 5: "3"}.get(market, "5")

    counter = mapping.get(market, base_counter)

    return f"{date_str}1000{market_code}{str(counter).zfill(4)}"