import requests

url_name = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
response = requests.get(url_name)
data = response.json()
print(data[0]["id"]) 