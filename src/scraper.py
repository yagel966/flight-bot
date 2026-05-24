import requests
from config import TRAVELPAYOUTS_TOKEN
from database import get_active_routes, save_price, get_last_price, save_alert
from notifier import send_alert 


def get_price(origin, destination):
    url = "https://api.travelpayouts.com/v1/prices/cheap"
    params = {
            "origin": origin,
            "destination": destination,
            "currency": "ils",
            "token": TRAVELPAYOUTS_TOKEN
            }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("success") and data.get("data"):
        prices = data["data"].get(destination, {})
        if prices:
            first_option = list(prices.values())[0]
            return first_option.get("price")
    return None


def run():
    routes = get_active_routes()

    for route in routes:
        route_id, origin, destination, target_price = route

        current_price = get_price(origin, destination)
        if current_price is None:
            print(f"לא נמצא מחיר עבור {origin} -> {destination}")
            continue

        save_price(route_id, current_price)

        last_price = get_last_price(route_id)

        price_dropped = last_price and current_price < last_price
        below_target = target_price and current_price <= target_price

        if price_dropped or below_target:
            send_alert(origin, destination, current_price, last_price)
            save_alert(route_id, current_price)

if __name__ == "__main__":
    run()
