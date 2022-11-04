#main.py

from upload_database import firebase_update, upload_2

# run this first regardless
firebase_update()   
print("Coin Data Successfully Uploaded")

# run this 24 hours later, this will keep the same coin order regardless of rankings, double coin amount
# upload_2()
# print("Second Coin Data Successfully Uploaded")

