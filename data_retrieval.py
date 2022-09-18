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

