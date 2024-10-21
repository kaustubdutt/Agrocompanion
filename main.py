from flask import Flask,request,redirect,url_for,render_template
from flask_mail import Mail, Message
import os, random, string
import threading
from hafunc import changestatusfunc,getdevicedatafunc
from rashifunc import inp
from geopy.geocoders import Nominatim
from meteocalc import dew_point
from firebase import firebase,Firebase
#Kaustub database
conn = firebase.FirebaseApplication("https://iotprojectmini.firebaseio.com/")
manoconn = firebase.FirebaseApplication("https://arduinodata-83659.firebaseio.com/")
#Havish Database
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






app = Flask(__name__)

'''app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kaustubdutt@gmail.com'
app.config['MAIL_PASSWORD'] = '098321Raikiri'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
#t1=threading.Thread(target=mailing())

def mailling():
    msg = Message('IOT Alert', sender='kaustubdutt@gmail.com', recipients=['kaustubzgame@gmail.com'])
    x = "35"
    msg.body = "Dear Customer, \n   Your Temperature is exceed than optimal.\n  It's value is  %s .Please Take necesary precautions to avoid further damage" % x
    mail.send(msg)


def estimate(d,f,p,t):
    v = 10000
    t = int(t)
    r = v - t
    est = r / (int(f)+1)
    est = est / 60
    return est'''



@app.route("/devicestatus",methods=["POST","GET"])
def devicestatus():
    if request.method == "POST":
        status = request.form["status"]
        conn.put("/","devicestatus",status)
        return render_template("devicestatus.html")
    return render_template("devicestatus.html")







@app.route("/monitoring")
def fun56():
    c=0
    while(True and c==0):
        x = conn.get('/', None)
        dates = list(x.keys())
        select=dates[-1]
        #select='6-11-2019'
        date = dict(conn.get(f'{select}', None))
        #date = conn.get("/"+z, None)
        times = list((date.keys()))
        pre=times[-1]
        result=conn.get("/"+select+"/"+pre,None)
        d = {}
        #Distance,Flowrate,2 paramaters
        for i in result.keys():
            if(str(i) == "Distance"):
                pass
            else:
                for j in result[i]:
                # print(i, end=" : ")
                # print(result[i][j])
                    d[i] = result[i][j]

        # msg = Message('IOT Alert', sender='manoharreddy1818@gmail.com', recipients=['kittu18061997@gmail.com'])
        x = d["Percentage"]
        # if(x>=90):
        #     msg = Message('IOT Alert', sender='kaustubdutt@gmail.com', recipients=['kaustubzgame@gmail.com'])
        #     msg.body = "Dear Customer,\n\nYour Tank is about to be full.\nPlease switch off the motor\n\nThanks and Regards"
        #     mail.send(msg)
        #     c=c+1
        # else:
        #     pass
    return d


@app.route('/',methods = ["POST","GET"])
def main():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if len(email)== 0 and len(password)== 0:
            return render_template("login.html",errorlogin=0,login=0,message="Email or Password is not entered. Please enter and try again.")
        else:
            #user = auth.sign_in_with_email_and_password(email,password)
            user = {}
            if(email == "admin@iot.com" and password == "password"):
                user["email"] = "admin"
            else:
                user["email"] = ""
            global currentemail
            currentemail = user["email"]
            global login
            login = 1
            return render_template("main.html",currentemail=currentemail,login = login)
    return render_template("login.html",errorlogin=1,login=0,message='')

@app.route('/selectionmain')
def selectionmain():
    return render_template("main.html")
@app.route("/getData",methods = ['POST', 'GET'])
def fun1():
        x = conn.get('/', None)
        dates = list(x.keys())
        if request.method == "POST":
            select = request.form['select']
            d = []
            f = []
            p = []
            t = []
            est=[]
            date = dict(conn.get(f'{select}', None))
            times = list((date.keys()))
            for i in times:
                time = date[i]
                di = (list(time['Distance'].keys()))[0]
                d.append(time['Distance'][di])
                fl = (list(time['Flowrate'].keys()))[0]
                f.append(time['Flowrate'][fl])
                tr = (list(time['Transferred liquid in ml'].keys()))[0]
                t.append(time['Transferred liquid in ml'][tr])
                pe = (list(time['Percentage'].keys()))[0]
                p.append(time['Percentage'][pe])
                # esti=estimate(time['Distance'][di],time['Flowrate'][fl],time['Percentage'][pe],time['Transferred liquid in ml'][tr])
                # est.append(esti)
            return render_template('/water_regulation/history.html',value=1, length=[i for i in range(len(times))], dates=dates,
                                   select=select, times=times, p=p, dist=d, flow=f, trans=t)

        return render_template('/water_regulation/history.html', value=0, dates=dates)

@app.route("/Monitoring")
def Monitoring():
    sendata = manoconn.get("/", None)
    temp = sendata["Temperature"]  # float(request.form["temp"])
    hum = sendata["Humidity"]
    soil = sendata["Soil Moisture"]
    return render_template("/control&monitor/monitoring.html",temp=temp, hum=hum, soil=soil)

#@app.route("/main")
#def main():
#    render_template("/main.html")

@app.route("/selection1")
def selection1():
    return render_template("/control&monitor/selection1.html")

@app.route("/selection2")
def selection2():
    return render_template("/water_regulation/selection2.html")
#
# @app.route("/selection3")
# def selection3():
#     return render_template("/crop_yield_prediction/selection3.html")

@app.route("/watertank")
def watertank():
    sendata1 = conn.get("/", None)
    flowrate = sendata1["flowrate"]  # float(request.form["temp"])
    percentage = sendata1["percentage"]
    amount = sendata1["water_transferred_in_ml"]
    return render_template("/water_regulation/watertank.html", flowrate = flowrate, percentage = percentage, amount = amount)



# @app.route("/sensorprediction")
# def sensorprediction():
#     return render_template("/crop_yield_prediction/sensorprediction.html")
#
# @app.route("/userprediction")
# def userprediction():
#     if request.method == "POST":
#
#     return render_template("/crop_yield_prediction/userprediction.html")'''












#Havish part
@app.route("/switches", methods=["POST","GET"])
def switches():
    device_list = dict(db.child("sai").child("led").get().val())
    device_list = list(device_list.keys())
    return render_template("/control&monitor/switches/switches.html",data=device_list)





#Hav API calls
##########################################################
@app.route('/changestatus',methods=["POST","GET"])
def changestatus():
    if request.method == "POST":
        y = request.get_json(silent=True)
        x = changestatusfunc(y)
        return x
    return "nothing was requested"


@app.route('/getdevicedata',methods=["POST","GET"])
def getdevicedata():
    if request.method == "POST":
         y = request.get_json(silent=True)
         x = getdevicedatafunc(y)
         return x
    return "Nothing was requested"
#############################################################


#@rashi
####################################################

@app.route("/selection3")
def selection3():
    return render_template("/crop_yield_prediction/selection3.html")

@app.route("/sensorprediction",methods=["POST","GET"])
def sensorprediction():
    if request.method == "POST":
        sendata = manoconn.get("/",None)
        address = request.form["address"]
        geolocator = Nominatim(user_agent="rashi")
        location = geolocator.geocode(address)
        long= location.longitude
        long = round(long,4)
        lat = location.latitude
        lat = round(lat,4)
        temp = sendata["Temperature"]  #float(request.form["temp"])
        hum = sendata["Humidity"]  # float(request.form["humidity"])
        dp = dew_point(temperature=temp, humidity=hum)
        dp = round(dp,2)
        pred = inp(long, lat, temp, dp, hum/100)
        #pred = round(pred,2)
        return render_template("/crop_yield_prediction/sensorprediction.html", pred=pred,long=long,lat=lat,temp=temp,dp=dp,hum=hum)
    return render_template("/crop_yield_prediction/sensorprediction.html",pred="")
@app.route("/userprediction",methods=["POST","GET"])
def userprediction():
    if request.method == "POST":
        long = float(request.form["longitude"])
        lat = float(request.form["latitude"])
        temp = float(request.form["temp"])
        dp = float(request.form["dewpoint"])
        hum = float(request.form["humidity"])
        pred = inp(long,lat,temp,dp,hum)
        return render_template("/crop_yield_prediction/userprediction.html",pred=pred)
    return render_template("/crop_yield_prediction/userprediction.html",pred="")



####################################################



if __name__ == "__main__":
    app.run(debug=True)
