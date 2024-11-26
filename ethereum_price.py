# File: ethereum_price.py
import requests
from datetime import datetime, timedelta


def get_ethereum_price_message():
    """
    Fetches the current and yesterday's Ethereum prices and generates a message.
    Also retrieves the lowest and highest prices in the last 2.5 months.
    :return: A string message with the Ethereum price and percentage change.
    """

    def get_ethereum_price_now():
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "ethereum",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["ethereum"]["usd"]

    def get_ethereum_price_on_date(date):
        url = f"https://api.coingecko.com/api/v3/coins/ethereum/history"
        params = {"date": date}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        market_data = data.get("market_data", {})
        return market_data.get("current_price", {}).get("usd", None)

    def get_ethereum_price_range():
        # Calculate the date 2.5 months ago (approx. 75 days)
        start_date = datetime.now() - timedelta(days=75)
        url = f"https://api.coingecko.com/api/v3/coins/ethereum/market_chart"
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
        price_now = get_ethereum_price_now()

        # Yesterday's price
        yesterday_date = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday_date.strftime("%d-%m-%Y")
        yesterday_formatted = yesterday_date.strftime("%b %d, %Y")
        price_yesterday = get_ethereum_price_on_date(yesterday_str)

        # Price range
        lowest_price, highest_price = get_ethereum_price_range()

        if price_yesterday:
            # Percentage change
            change = ((price_now - price_yesterday) / price_yesterday) * 100
            emoji = "🚀" if change > 0 else "📉"
            message = (
                f"Ethereum price is now at ${price_now:.2f}. "
                f"({change:+.2f}% {emoji}) compared to yesterday ({yesterday_formatted}).\n"
                f"Lowest in last 2.5 months: ${lowest_price:.2f}, "
                f"Highest in last 2.5 months: ${highest_price:.2f}."
            )
        else:
            message = "Ethereum price data for yesterday is unavailable."

        return message
    except requests.exceptions.RequestException as e:
        return f"Error retrieving data: {e}", None, None
