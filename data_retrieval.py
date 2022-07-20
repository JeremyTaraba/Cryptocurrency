# data_retrieval.py
import requests

def retrieve_data(coin_name):
  url_name = "https://data.messari.io/api/v1/assets/" + coin_name + "/metrics"
  response = requests.get(url_name)
  data = response.json()
  
  return data["data"]


def retrieve_price(coin_name):
  data = retrieve_data(coin_name)
  price = (data['market_data']['price_usd'])
  return price


def retrieve_additional_information(coin_name):
  data = retrieve_data(coin_name)
  data_high = f'${data["market_data"]["ohlcv_last_24_hour"]["high"]}'
  data_low = f'${data["market_data"]["ohlcv_last_24_hour"]["low"]}'
  print('\n' + coin_name, "is ranked number", data["marketcap"]["rank"], "in the world.")
  print("The highest price of", coin_name, "from the last 24 hours is", data_high)
  print("The lowest price of", coin_name, "from the last 24 hours is", data_low)