
from gc import collect
from firebase import firebase
import coin_info as coin_info
import requests
import settings

from twitterapi import calculate_polarity, getcointweets

firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)
url_name = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page="+str(settings.TOTAL_COINS*2)+"&page=1&sparkline=false&price_change_percentage=24h%2C7d%2C30d"
firebaseUrl = "https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/cryptoanalyzer-fc741/NewCryptoData.json"
response = requests.get(url_name)
data_coins = response.json()
oldFirebaseData = requests.get(firebaseUrl).json()


def upload(data):
    firebase.post('cryptoanalyzer-fc741/NewCryptoData', data)


def collect_data(data): # per coin
    coinData = coin_info.CoinInfo(data)
    tweets = getcointweets(coinData.coin_name)
    polarity = calculate_polarity(tweets)
    coin = {
        'Name': coinData.coin_name,
        'Price': round(coinData.price,5),
        'Rank': coinData.rank,
        'Polarity': round(polarity,5),
        'Price 24hr': round(coinData.price_24h,5),
        #'Price 30d' : round(coinData.price_30d,5), # was giving error because 1 coin didn't have 30 day price change
        'Price 7d' : round(coinData.price_7d,5),
        'Market Cap' : coinData.MC,
        'Market Cap 24hr' : round(coinData.MC_24h,5)
    }
    return coin

def collect_and_upload(): # add new 24 hour data
    for i in range(settings.TOTAL_COINS):
        coin = collect_data(data_coins[i])
        upload(coin)
        
def upload_2():
    for i in oldFirebaseData.keys():
        for j in range(settings.TOTAL_COINS*2):
            id = data_coins[j]['id']
            name = oldFirebaseData[i]['Name']
            if(name == id):
                coin = collect_data(data_coins[j])
                upload(coin)
                break

def delete_data():  # delete 24 hour old data
    firebase.delete('cryptoanalyzer-fc741/','OldCryptoData')
    

def move_data():
    for i in oldFirebaseData.keys():
        oldData = oldFirebaseData[i]
        firebase.post('cryptoanalyzer-fc741/OldCryptoData', oldData)
    firebase.delete('cryptoanalyzer-fc741/','NewCryptoData')
 


def firebase_update(): # delete old data, move data to other folder
    delete_data()
    move_data()
    collect_and_upload()

# make sure to increase the amount of coins in settings when doing this option
def second_update(): # used for if the order of coin rankings has changed, will keep coins in order in database regardless of ranking
    delete_data()
    move_data()
    upload_2() # slower than the collect_and_upload because we have to go through a nested loop

