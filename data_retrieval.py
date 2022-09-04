# data_retrieval.py


def retrieve_price(data):
    price = data['current_price']
    return price


def retrieve_rank(data):
    rank = data['market_cap_rank']
    return rank

def retrieve_name(data):
    name = data['id']
    return name

# def extra_information(data):
#     data = retrieve_data(coin_name)
#     current_market_cap = data['marketcap']['current_marketcap_usd']
#     volume_turnover_24_hour = data['marketcap']['volume_turnover_last_24_hours_percent']
#     circulating_supply = data['supply']['circulating']