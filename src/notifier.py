import requests
from datetime import datetime, timedelta
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_alert(origin, destination, current_price, last_price):
    date = (datetime.now() + timedelta(days=30)).strftime("%y%m%d")
    link = f"https://www.skyscanner.co.il/transport/flights/{origin}/{destination}/{date}/"

    if last_price:
        difference = last_price - current_price
        message = (
            f"התראת מחיר טיסה\n\n"
            f"מסלול: {origin} -> {destination}\n"
            f"מחיר עכשיו: ${current_price}\n"
            f"מחיר קודם: ${last_price}\n"
            f"ירידה של: ${difference}\n\n"
            f"לרכישה: {link}"
        )
    else:
        message = (
            f"מחיר טיסה חדש\n\n"
            f"מסלול: {origin} -> {destination}\n"
            f"מחיר: ${current_price}\n\n"
            f"לרכישה: {link}"
        )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.ok
