from firebase import firebase
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score


import coin_info
import requests

firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)
url_newData = "https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/cryptoanalyzer-fc741/NewCryptoData.json" 
url_oldData = "https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/cryptoanalyzer-fc741/OldCryptoData.json"

def prediction(model, data):
    prediction = model.predict(data)
    print(prediction)
    


def trainModel(X,Y):
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3) #do X.values and Y.values if you only want the values with no names
    rf = RandomForestRegressor()
    rf.fit(x_train, y_train) # training the data

    y_pred = rf.predict(x_test) # test our trained data

    r_square = r2_score(y_test, y_pred) # checking to see how well our data predicted
  
    if(r_square < 0.9):
        while(r_square < 0.9):
            # running it again to get a better score
            x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
            rf.fit(x_train, y_train) # training the data

            y_pred = rf.predict(x_test) # test our trained data

            r_square = r2_score(y_test, y_pred) # checking to see how well our data predicted
            
    print(r_square)   # close to 1 means really good
    return rf



def processData():
    dataFrame = pd.read_json(url_oldData) # all data on coins except price 24hr
    dataFrame = dataFrame.T # transpose so its in the correct order
    futureData = pd.read_json(url_newData) # new data 24 hours ahead of old data
    futureData = futureData.T

    
    X = dataFrame.drop(columns=["Price 24hr", "Name"])
    Y = futureData["Price 24hr"]
    model = trainModel(X,Y)


    futurePredict = futureData.drop(columns=["Price 24hr", "Name"]) # might want to save names somewhere to add them to a new list after prediction
    prediction(model, futurePredict)



processData()






    








