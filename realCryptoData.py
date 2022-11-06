from firebase import firebase
import requests
from Update_Database import settings
import matplotlib.pyplot as plt
import numpy as np
from Process_Data import process_database


url_name = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page="+str(settings.TOTAL_COINS*2)+"&page=1&sparkline=false&price_change_percentage=24h%2C7d%2C30d"
firebaseUrl = "https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/cryptoanalyzer-fc741/NewCryptoData.json"
oldFirebaseData = requests.get(firebaseUrl).json()
response = requests.get(url_name)
data_coins = response.json()

realHourData = []
coinNames = []


for i in oldFirebaseData.keys():
        for j in range(settings.TOTAL_COINS*2):
            id = data_coins[j]['id']
            name = oldFirebaseData[i]['Name']
            if(name == id):
                coinNames.append(name)
                realHourData.append(data_coins[j]['price_change_percentage_24h'])
                break




# determine percentage accuracy
# subtract the observed value from the true value, divide by the true value, multiply by 100, then subtract this result from 100

prediction = process_database.processData()
percentageResults = []

for i in range(len(prediction)):
    difference =  realHourData[i] - prediction[i]
    difference = difference / realHourData[i]
    difference = difference * 100
    percentageResults.append(100 - difference)
    print(100-difference)

sum = 0
for i in percentageResults:
    sum += i


print(sum / settings.TOTAL_COINS)



height = realHourData
bars = coinNames
y_pos = np.arange(len(bars))
colorList = []
for i in realHourData:
    if i < 0:
        colorList.append("red")
    elif i > 0:
        colorList.append("green")
    else:
        colorList.append("black")


# Create bars
plt.bar(y_pos, height, color = colorList)

# Create names on the x-axis
plt.xticks(y_pos, bars, rotation=90)

plt.ylabel("24 Hour Change")
plt.title("Current 24 Hour Price Change %")

# Show graphic
plt.show()
