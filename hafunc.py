# Hav fuction calls
from firebase import Firebase
import json

config =  {
    "apiKey": "AIzaSyBeTncdD2iqPHZId1LQEBGGlgxRtjPdu3U",
    "authDomain": "flutteriot-f26a9.firebaseapp.com",
    "databaseURL": "https://flutteriot-f26a9.firebaseio.com",
    "projectId": "flutteriot-f26a9",
    "storageBucket": "flutteriot-f26a9.appspot.com",
    "messagingSenderId": "234797577258",
    "appId": "1:234797577258:web:f9180bd58a8ccafff7bf53",
    "measurementId": "G-3783X43YC5"
  }

fire = Firebase(config)
db=fire.database()
auth = fire.auth()

def changestatusfunc(x):
    db.child("sai").child("led").child(x["currentdevice"]).set({"switch": x["currentstatus"]})
    return "done"


def getdevicedatafunc(x):
    x = dict(x)
    currdev = x["currentdevice"]
    r = dict(db.child("sai").child("led").child(currdev).get().val())
    d = {"currentdevice": x["currentdevice"], "currentstatus": r["switch"]}
    d = json.dumps(d)
    return d