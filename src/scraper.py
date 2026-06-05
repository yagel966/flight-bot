import time
import requests

from config import TRAVELPAYOUTS_TOKEN
from database import get_active_routes, save_price, get_last_price, save_alert
from notifier import send_alert


def get_price(origin, destination):
    url = "https://api.travelpayouts.com/v1/prices/cheap"
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
        result_data = data["data"]

        prices = result_data.get(destination)

        if not prices:
            first_city_key = next(iter(result_data))
            print(
                    f"No exact airport match for {destination}, using city key {first_city_key}",
                    flush=True
                    )
            prices = result_data[first_city_key]
        if prices:
            first_option = list(prices.values())[0]
            return first_option.get("price")


def run():
    print("Starting flight price check...", flush=True)

    routes = get_active_routes()
    print(f"Found {len(routes)} active routes", flush=True)

    for route in routes:
        route_id, origin, destination, target_price = route

        print(f"Checking route {origin} -> {destination}", flush=True)

        current_price = get_price(origin, destination)

        if current_price is None:
            print(f"No price found for {origin} -> {destination}", flush=True)
            continue

        print(f"Price found for {origin} -> {destination}: {current_price} ILS", flush=True)

        last_price = get_last_price(route_id)

        save_price(route_id, current_price)
        print(f"Saved price for route_id={route_id}", flush=True)

        price_dropped = last_price and current_price < last_price

        if price_dropped:
            print(f"Price dropped: {last_price} -> {current_price}", flush=True)
            send_alert(origin, destination, current_price, last_price)
            save_alert(route_id, current_price)

        elif not last_price and target_price and current_price <= target_price:
            print(
                f"First price is under target price: {current_price} <= {target_price}",
                flush=True
            )
            send_alert(origin, destination, current_price, last_price)
            save_alert(route_id, current_price)
    params = {
        "origin": origin,
        "destination": destination,
        "currency": "ils",
        "token": TRAVELPAYOUTS_TOKEN
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("success") and data.get("data"):
        result_data = data["data"]

        price = result_data.get(destination)

        if not prices:
            first_city_key = next(iter(result_data))
            print(
                    f"No exact airport match for {destination}, using city key {first_city_key}",
                    flush=True
                    )
            prices = result_data[first_city_key]
        if prices:
            first_option = list(prices.values())[0]
            return first_option.get("price")


def run():
    print("Starting flight price check...", flush=True)

    routes = get_active_routes()
    print(f"Found {len(routes)} active routes", flush=True)

    for route in routes:
        route_id, origin, destination, target_price = route

        print(f"Checking route {origin} -> {destination}", flush=True)

        current_price = get_price(origin, destination)

        if current_price is None:
            print(f"No price found for {origin} -> {destination}", flush=True)
            continue

        print(f"Price found for {origin} -> {destination}: {current_price} ILS", flush=True)

        last_price = get_last_price(route_id)

        save_price(route_id, current_price)
        print(f"Saved price for route_id={route_id}", flush=True)

        price_dropped = last_price and current_price < last_price

        if price_dropped:
            print(f"Price dropped: {last_price} -> {current_price}", flush=True)
            send_alert(origin, destination, current_price, last_price)
            save_alert(route_id, current_price)

        elif not last_price and target_price and current_price <= target_price:
            print(
                f"First price is under target price: {current_price} <= {target_price}",
                flush=True
            )
            send_alert(origin, destination, current_price, last_price)
            save_alert(route_id, current_price)

    print("Flight price check completed", flush=True)


if __name__ == "__main__":
    while True:
        run()
        time.sleep(3600)
