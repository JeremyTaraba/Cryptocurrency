# coin_info.py
import data_retrieval

class CoinInfo:
    def __init__(self, name):
        self.coin_name = name
        self.price = data_retrieval.retrieve_price(name)
        self.rank = data_retrieval.retrieve_rank(name)

    def get_retrieve_price(self):
        return self.price
    
    def set_retrieve_price(self):
        self.price = data_retrieval.retrieve_price(self.coin_name)
    
    def get_retrieve_rank(self):
        return self.rank

    def set_retrieve_rank(self):
        self.rank = data_retrieval.retrieve_rank(self.coin_name)
        