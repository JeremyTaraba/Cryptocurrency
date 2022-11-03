# data_retrieval.py


def retrieve_price(data):
    return data['current_price']

def retrieve_rank(data):
    return data['market_cap_rank']

def retrieve_name(data):
    return data['id']

def retrieve_MC(data):
    return data['market_cap']

def retrieve_price_24h(data):
    return data['price_change_percentage_24h']

def retrieve_MC_24h(data):
    return data['market_cap_change_percentage_24h']

def retrieve_price_30d(data):
    return data['price_change_percentage_30d_in_currency']

def retrieve_price_7d(data):
    return data['price_change_percentage_7d_in_currency']