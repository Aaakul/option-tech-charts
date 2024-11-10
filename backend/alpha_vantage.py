import os
import requests
from dotenv import load_dotenv


# Load api key from .env
load_dotenv ()
api_key = os.getenv("API_KEY")

symbol = "SPY"


url = f"https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={symbol}&apikey={api_key}"
# r = requests.get(url)
# data = r.json()

print(url)