from firebase import firebase
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score


firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)
url_name = "https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/cryptoanalyzer-fc741/CryptoData.json"

dataFrame = pd.read_json(url_name)
dataFrame = dataFrame.T
#print(dataFrame)
Y = dataFrame["Price 24hr"]
#print(Y)
X = dataFrame.drop(columns=["Price 24hr", "Name"])
#print(X)
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

#print(y_train)

rf = RandomForestRegressor()
rf.fit(x_train, y_train) # training the data

y_pred = rf.predict(x_test) # test our trained data

# print(y_pred)
# print("y_test:")
# print(y_test)

r_square = r2_score(y_test, y_pred) # checking to see how well our data predicted
print(r_square)     # close to 1 means really good

# running it again to get a better score
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
rf.fit(x_train, y_train) # training the data

y_pred = rf.predict(x_test) # test our trained data

r_square = r2_score(y_test, y_pred) # checking to see how well our data predicted
print(r_square)   