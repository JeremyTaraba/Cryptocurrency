#main.py
import coin_info

chosen = False
while(not chosen):
    chosen = True
    print("0 - Bitcoin\n1 - Ethereum\n2 - Litecoin\n3 - Dogecoin")

    coin_choice = int(input("Please choose a coin: "))

    if coin_choice == 0:
        coin_info = coin_info.CoinInfo("bitcoin")
    elif coin_choice == 1:
        coin_info = coin_info.CoinInfo("ethereum")
    elif coin_choice == 2:
        coin_info = coin_info.CoinInfo("litecoin")
    elif coin_choice == 3:
        coin_info = coin_info.CoinInfo("dogecoin")
    else:
        print("Not a current choice. Choose again\n")
        chosen = False
  
print("\nCoin choice successfully made!\n")

print("0 - View Price\n1 - View Additional Information (Rank, Highest Price from the Last 24 Hours, Lowest Price from the Last 24 Hours)")

action_choice = int(input("Please choose an action: "))

if action_choice == 0:
  price_string = f"${coin_info.retrieve_price()}"
  print("Current Price for", coin_info.name, "is:", price_string)
elif action_choice == 1:
  coin_info.retrieve_important_information()