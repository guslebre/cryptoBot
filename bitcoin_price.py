# File: bitcoin_price.py
import requests
from datetime import datetime, timedelta


def get_bitcoin_price_message():
    """
    Fetches the current and yesterday's Bitcoin prices and generates a message.
    Also retrieves the lowest and highest prices in the last 2.5 months along with their dates.
    :return: A string message with the Bitcoin price and percentage change.
    """

    def get_bitcoin_price_now():
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["bitcoin"]["usd"]

    def get_bitcoin_price_on_date(date):
        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/history"
        params = {"date": date}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        market_data = data.get("market_data", {})
        return market_data.get("current_price", {}).get("usd", None)

    def get_bitcoin_price_range():
        # Calculate the date 2.5 months ago (approx. 75 days)
        start_date = datetime.now() - timedelta(days=75)
        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {
            "vs_currency": "usd",
            "days": "90"  # Last 90 days
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract prices and timestamps
        prices = data["prices"]
        price_values = [point[1] for point in prices]
        timestamps = [datetime.utcfromtimestamp(point[0] / 1000).strftime('%b %d, %Y') for point in prices]

        # Find lowest and highest prices with their dates
        lowest_price = min(price_values)
        highest_price = max(price_values)
        lowest_price_date = timestamps[price_values.index(lowest_price)]
        highest_price_date = timestamps[price_values.index(highest_price)]

        return lowest_price, lowest_price_date, highest_price, highest_price_date

    try:
        # Current price
        price_now = get_bitcoin_price_now()

        # Yesterday's price
        yesterday_date = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday_date.strftime("%d-%m-%Y")
        yesterday_formatted = yesterday_date.strftime("%b %d, %Y")
        price_yesterday = get_bitcoin_price_on_date(yesterday_str)

        # Price range
        lowest_price, lowest_price_date, highest_price, highest_price_date = get_bitcoin_price_range()

        if price_yesterday:
            # Percentage change
            change = ((price_now - price_yesterday) / price_yesterday) * 100
            emoji = "🚀" if change > 0 else "📉"
            message = (
                f"Bitcoin price is now at ${price_now:.2f}. "
                f"({change:+.2f}% {emoji}) compared to yesterday ({yesterday_formatted}).\n"
                f"Lowest in last 3 months: ${lowest_price:.2f} on {lowest_price_date}, "
                f"Highest in last 3 months: ${highest_price:.2f} on {highest_price_date}."
            )
        else:
            print("errorrrrr")
            raise Exception("no price yesterday")

        return message, lowest_price, highest_price, price_now, change, emoji
    except requests.exceptions.RequestException as e:
        # Ensure six values are returned even in error cases
        return f"Error retrieving data: {e}", None, None, None, None, None
