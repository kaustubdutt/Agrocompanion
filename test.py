from firebase import firebase,Firebase



conn = firebase.FirebaseApplication("https://arduinodata-83659.firebaseio.com/")


print(conn.get('/Temperature',None))


