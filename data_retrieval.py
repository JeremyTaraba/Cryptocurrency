# data_retrieval.py

import requests


def retrieve_data(coin_name):
    url_name = "https://data.messari.io/api/v1/assets/"+coin_name+"/metrics"
    response = requests.get(url_name)
    data = response.json()
    return data["data"]


def retrieve_price(coin_name):
    data = retrieve_data(coin_name)
    price = (data['market_data']['price_usd'])
    return price


def retrieve_rank(coin_name):
    data = retrieve_data(coin_name)
    rank = (data['marketcap']['rank'])
    return rank

def extra_information(coin_name):
    data = retrieve_data(coin_name)
    current_market_cap = data['marketcap']['current_marketcap_usd']
    volume_turnover_24_hour = data['marketcap']['volume_turnover_last_24_hours_percent']
    circulating_supply = data['supply']['circulating']