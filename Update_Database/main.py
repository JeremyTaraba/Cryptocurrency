#main.py

from upload_database import firebase_update, second_update

# run this first regardless
# firebase_update()   
# print("Coin Data Successfully Uploaded")

# run this 24 hours later, this will keep the same coin order regardless of rankings, double coin amount
second_update()
print("Second Coin Data Successfully Uploaded")

