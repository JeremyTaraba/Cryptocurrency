#main.py
import schedule

from upload_database import firebase_update

# print("waiting for scheduler")
# schedule.every().day.at("16:47").do(firebase_update)


#firebase_update()   # check if 24 hours have passed, if yes then update database
print("Coin Data Successfully Uploaded")

print("Processing Data: ")



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










