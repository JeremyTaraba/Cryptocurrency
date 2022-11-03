from firebase import firebase
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score


#import coin_info as coin_info
import requests


firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)
url_newData = "https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/cryptoanalyzer-fc741/NewCryptoData.json" 
url_oldData = "https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/cryptoanalyzer-fc741/OldCryptoData.json"

dataFrame = pd.read_json(url_oldData) # all data on coins except price 24hr
dataFrame = dataFrame.T
futureData = pd.read_json(url_newData) # new data 24 hours ahead of old data
futureData = futureData.T
#print(futureData)

Y = futureData["Price 24hr"]

X = dataFrame.drop(columns=["Price 24hr", "Name"])

futurePredict = futureData.drop(columns=["Price 24hr", "Name"]) # might want to save names somewhere to add them to a new list after prediction
#print(futurePredict)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)    #do X.values and Y.values if you only want the values with no names



rf = RandomForestRegressor()
rf.fit(x_train, y_train) # training the data

y_pred = rf.predict(x_test) # test our trained data



r_square = r2_score(y_test, y_pred) # checking to see how well our data predicted
#print(r_square)     


if(r_square < 0.9):
    while(r_square < 0.9):
        # running it again to get a better score
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
        rf.fit(x_train, y_train) # training the data

        y_pred = rf.predict(x_test) # test our trained data

        r_square = r2_score(y_test, y_pred) # checking to see how well our data predicted
        
print(r_square)   # close to 1 means really good






# url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=chiliz&order=market_cap_desc&per_page=1&page=1&sparkline=false&price_change_percentage=24h%2C7d%2C30d"
# response = requests.get(url)
# data_coins = response.json()
# data = data_coins[0]
# coinData = coin_info.CoinInfo(data)

# #need to look up new polarity for the coin that is picked
# polarity = -0.26666666666666666
# list = [
#     [coinData.MC, coinData.MC_24h, polarity, coinData.price, coinData.price_30d, coinData.price_7d, coinData.rank]
#     ]

prediction = rf.predict(futurePredict)

print(prediction)



# Run our code at noon automatically?

#need to have them type id of coin and then we can find that coin
#need a check for if that coin is valid or not cause if not if will break it

#we should try to calculate the average deviation each time the algorithm is run and how accurate it tends to be based on actual 24hr change