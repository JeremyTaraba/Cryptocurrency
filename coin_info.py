# coin_info.py
import data_retrieval

class CoinInfo:
  def __init__(self, name):
    self.name = name
    self.price = 0
    self.data = data_retrieval.retrieve_data(name)


  def retrieve_price(self):
    self.price = data_retrieval.retrieve_price(self.name)
    return self.price

  
  def retrieve_important_information(self):
    data_retrieval.retrieve_additional_information(self.name)