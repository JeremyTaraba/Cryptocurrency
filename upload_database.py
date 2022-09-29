
from gc import collect
from firebase import firebase
import coin_info
import requests
import settings

from twitterapi import calculate_polarity, getcointweets

firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)
url_name = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h%2C7d%2C30d"
response = requests.get(url_name)
data_coins = response.json()



def upload(data):
    firebase.post('cryptoanalyzer-fc741/CryptoData', data)


def collect_data(data): # per coin
    coinData = coin_info.CoinInfo(data)
    tweets = getcointweets(coinData.coin_name)
    polarity = calculate_polarity(tweets)
    coin = {
        'Name': coinData.coin_name,
        'Price': coinData.price,
        'Rank': coinData.rank,
        'Polarity': polarity,
        'Price 24hr': coinData.price_24h,
        'Price 30d' : coinData.price_30d,
        'Price 7d' : coinData.price_7d,
        'Market Cap' : coinData.MC,
        'Market Cap 24hr' : coinData.MC_24h,
    }
    return coin

def collect_and_upload(): 
    for i in range(settings.TOTAL_COINS):
        coin = collect_data(data_coins[i])
        upload(coin)
        
    

def delete_data():
    firebase.delete('cryptoanalyzer-fc741/','CryptoData')
    pass


def firebase_update():
    delete_data()
    collect_and_upload()

