# coin_info.py
import data_retrieval

class CoinInfo:
    def __init__(self, data):
        self.coin_name = data_retrieval.retrieve_name(data)
        self.price = data_retrieval.retrieve_price(data)
        self.rank = data_retrieval.retrieve_rank(data)

    def get_price(self):
        return self.price
    

    def get_rank(self):
        return self.rank

        