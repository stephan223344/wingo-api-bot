from datetime import datetime
import pytz

# 🔥 OFFSET UNIQUE basé sur le 30s (à ajuster une seule fois)
OFFSET = 657

def generate_period(market: float):
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    date_str = now.strftime("%Y%m%d")
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    seconds = int((now - midnight).total_seconds())

    # ✅ compteur de base (30s uniquement)
    base_counter = (seconds // 30) - OFFSET

    cycle_seconds = int(market * 60)
    elapsed_in_cycle = seconds % cycle_seconds

    time_remaining = cycle_seconds - elapsed_in_cycle

    if time_remaining == cycle_seconds:
        time_remaining = 0
        base_counter += 1

    # ✅ division APRÈS offset (logique correcte)
    if market == 0.5:      # 30s
        counter = base_counter
    elif market == 1:      # 1 min
        counter = base_counter // 2
    elif market == 3:      # 3 min
        counter = (base_counter + 5) // 6
    elif market == 5:      # 5 min
        counter = (base_counter + 9) // 10
    else:
        counter = base_counter

    # ✅ mapping correct
    market_code = {
        0.5: "5",
        1: "1",
        3: "2",
        5: "3"
    }.get(market, "5")

    # format compteur
    counter_str = str(counter).zfill(4)

    return f"{date_str}1000{market_code}{counter_str}"