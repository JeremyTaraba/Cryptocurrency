
from gc import collect
from firebase import firebase
import coin_info
import requests

firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)
url_name = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h%2C7d%2C30d"
response = requests.get(url_name)
data_coins = response.json()



def upload(data):
    firebase.post('cryptoanalyzer-fc741/CryptoData', data)


def collect_data(data): # per coin
    coinData = coin_info.CoinInfo(data)
    coin = {
        'Name': coinData.coin_name,
        'Price': coinData.get_price(),
        'Rank': coinData.get_rank()
    }
    return coin

def collect_and_upload(): 
    for i in range(5):
        coin = collect_data(data_coins[i])
        upload(coin)

def delete_data():
    firebase.delete('cryptoanalyzer-fc741/','CryptoData')
    pass


def firebase_update():
    delete_data()
    collect_and_upload()

firebase_update()
