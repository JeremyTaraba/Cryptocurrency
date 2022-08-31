from firebase import firebase

firebase = firebase.FirebaseApplication("https://cryptoanalyzer-fc741-default-rtdb.firebaseio.com/", None)

firebase.put('/cryptoanalyzer-fc741/Student/ABC123','Name','Bob')

# if you want to delete data
# firebase.delete('/cryptoanalyzer-fc741/Student/', 'ABC123')