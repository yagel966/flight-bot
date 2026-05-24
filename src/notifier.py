import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_alert(origin, destination, current_price, last_price):
    if last_price:
        difference = last_price - current_price
        message = (
            f"התראת מחיר טיסה\n\n"
            f"מסלול: {origin} <- {destination}\n"
            f"מחיר עכשיו: {current_price} שקל\n"
            f"מחיר קודם: {last_price} שקל\n"
            f"ירידה של: {difference} שקל\n\n"
            f"לרכישה: https://www.skyscanner.co.il"
        )
    else:
        message = (
            f"מחיר טיסה חדש\n\n"
            f"מסלול: {origin} <- {destination}\n"
            f"מחיר: {current_price} שקל\n\n"
            f"לרכישה: https://www.skyscanner.co.il"
        )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.ok
