#main.py

import coin_info
import json
from firebase import firebase

firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)
data = {
    'Name': 'Jeremy',
    'Email': 'jeremy@gmail',
    'phone': 911,
}

# creates a random name for it, doesn't matter for us because we will be iterating through all the data
result = firebase.post('/cryptoanalyzer-fc741/Student', data)
print(result)

with open("book_info.json", "r") as f:
	file_contents = json.load(f)
firebase.post('/cryptoanalyzer-fc741/Books',file_contents)


# import firebase_admin
# from firebase_admin import db

# ref = db.reference("/")

# from firebase_admin import credentials

#cred = credentials.Certificate("cryptoanalyzer-fc741-firebase-adminsdk-i2f2w-04e511a468.json")
#firebase_admin.initialize_app(cred)







print("Enter what coin you want to check")
coin_name = input()
coin = coin_info.CoinInfo(coin_name)

print(coin.price)
print(coin.rank)
print("Do you want to update the price and rank?")
answer = input()
while answer == "yes":
    coin.set_retrieve_price()
    coin.get_retrieve_rank()
    print(coin.get_retrieve_price())
    print(coin.get_retrieve_rank())
    print("Do you want to update the price and rank?")
    answer = input()


# Market Cap, 24 Hour data, 
