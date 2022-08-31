from firebase import firebase

firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)
result = firebase.get('/cryptoanalyzer-fc741/Student/-NApTCtmPKFjyxZb5VGm','Name')
print(result)