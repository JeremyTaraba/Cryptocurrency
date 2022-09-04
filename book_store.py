from firebase import firebase

firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)

import json

# how to set data
# data = {
#     'Name': 'Book',
#     'Author': 'Someone',
#     'Genre': 'Fantasy',
#     'Price': 20
# }

# result = firebase.post('cryptoanalyzer-fc741/Books', data)
# print(result)


# how to update data
# firebase.put('cryptoanalyzer-fc741/Books/-NAqD9V-s6jYRnlzGReX','Price',30)




# how to get data
# data = firebase.get('cryptoanalyzer-fc741/Books/-NAqD9V-s6jYRnlzGReX','Author')
# print(data)



# how to delete data
# firebase.delete('cryptoanalyzer-fc741/Books/','-NAqD9V-s6jYRnlzGReX')

firebase.delete('cryptoanalyzer-fc741/','Books')

with open("book_info.json","r") as file:
    file_contents = json.load(file)

firebase.post('cryptoanalyzer-fc741/Books/', file_contents)