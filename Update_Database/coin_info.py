# coin_info.py
import data_retrieval

class CoinInfo:
    def __init__(self, data):
        self.coin_name = data_retrieval.retrieve_name(data)
        self.price = data_retrieval.retrieve_price(data)
        self.rank = data_retrieval.retrieve_rank(data)
        self.MC = data_retrieval.retrieve_MC(data)
        self.price_24h = data_retrieval.retrieve_price_24h(data)
        self.MC_24h = data_retrieval.retrieve_MC_24h(data)
        self.price_30d = data_retrieval.retrieve_price_30d(data)
        self.price_7d = data_retrieval.retrieve_price_7d(data)

    # def get_price(self):
    #     return self.price
    

    # def get_rank(self):
    #     return self.rank

        