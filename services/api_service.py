import httpx
from config import BASE_URL

async def get_prediction(market: str):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{BASE_URL}/predict",
                params={"market": market},
                timeout=10
            )
            r.raise_for_status()
            data = r.json()

            return data.get("items", [None])[0]

    except Exception as e:
        print(f"API error: {e}")
        return None