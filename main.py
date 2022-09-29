#main.py

from upload_database import firebase_update

firebase_update()
print("Coin Data Successfully Uploaded")
print("Processing Data: ")
#process_data() #train and test? or maybe do train first and then test
#add a global value for how many coins we want and how many tweets we want so we can easily change it

# print("Enter what coin you want to check")
# coin_name = input()
# coin = coin_info.CoinInfo(coin_name)

# print(coin.price)
# print(coin.rank)
# print("Do you want to update the price and rank?")
# answer = input()
# while answer == "yes":
#     coin.set_retrieve_price()
#     coin.get_retrieve_rank()
#     print(coin.get_retrieve_price())
#     print(coin.get_retrieve_rank())
#     print("Do you want to update the price and rank?")
#     answer = input()


# market_cap, price_change_percentage_24h, market_cap_change_percentage_24h, price_change_percentage_30d_in_currency, price_change_percentage_7d_in_currency










