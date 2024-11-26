# File: dogecoin_price.py
import requests
from datetime import datetime, timedelta


def get_dogecoin_price_message():
    """
    Fetches the current and yesterday's Dogecoin prices and generates a message.
    Also retrieves the lowest and highest prices in the last 2.5 months.
    :return: A string message with the Dogecoin price and percentage change.
    """

    def get_dogecoin_price_now():
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "dogecoin",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["dogecoin"]["usd"]

    def get_dogecoin_price_on_date(date):
        url = f"https://api.coingecko.com/api/v3/coins/dogecoin/history"
        params = {"date": date}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        market_data = data.get("market_data", {})
        return market_data.get("current_price", {}).get("usd", None)

    def get_dogecoin_price_range():
        # Calculate the date 2.5 months ago (approx. 75 days)
        start_date = datetime.now() - timedelta(days=75)
        url = f"https://api.coingecko.com/api/v3/coins/dogecoin/market_chart"
        params = {
            "vs_currency": "usd",
            "days": "75"  # Last 75 days
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract prices
        prices = [point[1] for point in data["prices"]]
        lowest_price = min(prices)
        highest_price = max(prices)

        return lowest_price, highest_price

    try:
        # Current price
        price_now = get_dogecoin_price_now()

        # Yesterday's price
        yesterday_date = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday_date.strftime("%d-%m-%Y")
        yesterday_formatted = yesterday_date.strftime("%b %d, %Y")
        price_yesterday = get_dogecoin_price_on_date(yesterday_str)

        # Price range
        lowest_price, highest_price = get_dogecoin_price_range()

        if price_yesterday:
            # Percentage change
            change = ((price_now - price_yesterday) / price_yesterday) * 100
            emoji = "🚀" if change > 0 else "📉"
            message = (
                f"Dogecoin price is now at ${price_now:.4f}. "
                f"({change:+.2f}% {emoji}) compared to yesterday ({yesterday_formatted}).\n"
                f"Lowest in last 2.5 months: ${lowest_price:.4f}, "
                f"Highest in last 2.5 months: ${highest_price:.4f}."
            )
        else:
            message = "Dogecoin price data for yesterday is unavailable."

        return message
    except requests.exceptions.RequestException as e:
        return f"Error retrieving data: {e}", None, None
