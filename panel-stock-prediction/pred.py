import mysql.connector as c
import datetime
import pandas as pd
import numpy as np
from numpy import array
from keras.models import Sequential,load_model
from keras.layers import LSTM
from keras.layers import Dense
from tensorflow import keras
from math import ceil
import json
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask_cors import CORS

cred = credentials.Certificate('invsystem-7a8da-firebase-adminsdk-u3sny-a4aa912743.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://invsystem-7a8da-default-rtdb.asia-southeast1.firebasedatabase.app'
})

database = db.reference('/Panel-prediction')
countdb = db.reference('/count')
datasetdb = db.reference('/Dataset/')


from flask import Flask, render_template, request
import flask
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS']='Content_Type'


n_features = 1
n_steps = 7

conn = c.connect(
    host="localhost",
    user="invDev",
    passwd="dontbegreedy",
    database="inventory_management"
)

if (conn.is_connected()):
    print("Connection successfull")
else:
    print("Connectivity issue")
cursor = conn.cursor(buffered=True)




model1=keras.models.load_model("panel1.h5")
model2=keras.models.load_model("panel2.h5")
model3=keras.models.load_model("panel3.h5")
model4=keras.models.load_model("panel4.h5")
model5=keras.models.load_model("panel5.h5")


def ret_json_obj(count,val1,val2,val3,val4,val5,t):
    x = {
        count:{
            "Panel1":val1,
            "Panel2":val2,
            "Panel3":val3,
            "Panel4":val4,
            "Panel5":val5,
            "Timestamp":t
        }
    }

    # y=json.dumps(x)
    return x



def split_sequence(sequence,n_steps):
    X,y = list(),list()
    for i in range(len(sequence)):
        end_ix = i+n_steps
        if end_ix>len(sequence)-1:
            break
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)




def fetch_data():
    cursor.execute("""select panel_type,count(panel_type),DATE(order_date) from orders_placed O, panel_details P
                   where O.order_id=P.order_id and
                   order_date > current_date - interval 7 day
                   group by panel_type
                   order by order_date desc""")

    conn.commit()
    myres = cursor.fetchall()
    return myres

def split_data(myres):
    col = []
    panel1,panel2,panel3,panel4,panel5 = [],[],[],[],[]
    for row in myres:
        col.append(list(row))
        if row[0]==1:
            panel1.append(list(row))
        elif row[0]==2:
            panel2.append(list(row))
        elif row[0]==3:
            panel3.append(list(row))
        elif row[0]==4:
            panel4.append(list(row))
        elif row[0]==5:
            panel5.append(list(row))
    #return panel1,panel2,panel3,panel4,panel5
    p1=[0,0,0,0,0,0,0]
    p2=[0,0,0,0,0,0,0]
    p3=[0,0,0,0,0,0,0]
    p4=[0,0,0,0,0,0,0]
    p5=[0,0,0,0,0,0,0]
    
    for i in panel1:
        p1[(datetime.date.today()-i[2]).days] = i[1]
    for i in panel2:
        p2[(datetime.date.today()-i[2]).days] = i[1]
    for i in panel3:
        p3[(datetime.date.today()-i[2]).days] = i[1]
    for i in panel4:
        p4[(datetime.date.today()-i[2]).days] = i[1]
    for i in panel5:
        p5[(datetime.date.today()-i[2]).days] = i[1]
    p1,p2,p3,p4,p5 = np.array(p1),np.array(p2),np.array(p3),np.array(p4),np.array(p5)
    
    p1 = p1.reshape((1, n_steps, n_features))
    p2 = p2.reshape((1, n_steps, n_features))
    p3 = p3.reshape((1, n_steps, n_features))
    p4 = p4.reshape((1, n_steps, n_features))
    p5 = p5.reshape((1, n_steps, n_features))
    out=[0,0,0,0,0]
    out[0] = int(ceil((model1.predict(p1, verbose=0)).tolist()[0][0]))
    out[1] = int(ceil((model2.predict(p2, verbose=0)).tolist()[0][0]))
    out[2] = int(ceil((model3.predict(p3, verbose=0)).tolist()[0][0]))
    out[3] = int(ceil((model4.predict(p4, verbose=0)).tolist()[0][0]))
    out[4] = int(ceil((model5.predict(p5, verbose=0)).tolist()[0][0]))
    return out


def write_message(panel_type,data):
    message = database.child(panel_type)
    message.set(data)


@app.route('/get-prediction',methods=['GET'])
def pred_sales():
    myres = fetch_data()
    out = split_data(myres)
    for i in range(len(out)):
    	if out[i]<0:
    		out[i]=0
    write_message('Panel1',out[0])
    write_message('Panel2',out[1])
    write_message('Panel3',out[2])
    write_message('Panel4',out[3])
    write_message('Panel5',out[4])

    count = countdb.get()
    ct = datetime.datetime.now()
    data = ret_json_obj(count+1,out[0],out[1],out[2],out[3],out[4],str(ct))
    datasetdb.push(data)
    countdb.set(count+1)

    return out
    
if __name__ == "__main__":
	app.run(debug=True)
