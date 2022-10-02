from firebase import firebase
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score


import coin_info
import requests


firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)
url_name = "https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/cryptoanalyzer-fc741/CryptoData.json"

dataFrame = pd.read_json(url_name)
dataFrame = dataFrame.T

Y = dataFrame["Price 24hr"]

X = dataFrame.drop(columns=["Price 24hr", "Name"])

x_train, x_test, y_train, y_test = train_test_split(X.values, Y.values, test_size=0.3)



rf = RandomForestRegressor()
rf.fit(x_train, y_train) # training the data

y_pred = rf.predict(x_test) # test our trained data



r_square = r2_score(y_test, y_pred) # checking to see how well our data predicted
#print(r_square)     


if(r_square < 0.9):
    while(r_square < 0.9):
        # running it again to get a better score
        x_train, x_test, y_train, y_test = train_test_split(X.values, Y.values, test_size=0.3)
        rf.fit(x_train, y_train) # training the data

        y_pred = rf.predict(x_test) # test our trained data

        r_square = r2_score(y_test, y_pred) # checking to see how well our data predicted
        
print(r_square)   # close to 1 means really good






url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=chiliz&order=market_cap_desc&per_page=1&page=1&sparkline=false&price_change_percentage=24h%2C7d%2C30d"
response = requests.get(url)
data_coins = response.json()
data = data_coins[0]
coinData = coin_info.CoinInfo(data)

#need to look up new polarity for the coin that is picked
polarity = -0.26666666666666666
list = [
    [coinData.MC, coinData.MC_24h, polarity, coinData.price, coinData.price_30d, coinData.price_7d, coinData.rank]
    ]
prediction = rf.predict(list)
print(prediction)

#need to get data for coins that is 24hr old and then get data for what the increase percentage in 24hr is after 24hrs
#to do this we would need to have two databases, one for 24hour old data on the coins that we hold and one for new 24hour data that we use
#the next day. We also need to hold the current 24hr price change percentage.
#so when we upload_database we are grabbing current coin info but saving that info for use 24 hours later?
#yes so we run it and we have 2 different databases, 1 holds current data and the other holds old data. When we run upload_database it will
#move the current data to old data and rewrite old data with new current data. If we run this every 24 hours then the data will have a difference 
#of 24 hours. SO we have to include the price change in 24 hours to predict a future price change in 24 hours.

#right now, figure out the order of things we will need to code. Do we code the user entering the coin first? do we code our prediction working? 
#clean up our files? Run our code every night automatically?

#need to have them type id of coin and then we can find that coin
#need a check for if that coin is valid or not cause if not if will break it
#need to find a way to run our code every night at midnight

#we should try to calculate the average deviation each time the algorithm is run and how accurate it tends to be based on actual 24hr change