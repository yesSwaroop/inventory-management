
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import datetime

cred = credentials.Certificate('invsystem-7a8da-firebase-adminsdk-u3sny-a4aa912743.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://invsystem-7a8da-default-rtdb.asia-southeast1.firebasedatabase.app'
})


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



database = db.reference('/Panel-prediction')
countdb = db.reference('/count')
datasetdb = db.reference('/Dataset/')
count = countdb.get()
ct = datetime.datetime.now()
data = ret_json_obj(count+1,1,2,3,4,5,str(ct))


print(type(data))
key = datasetdb.push(data)
print(key)
countdb.set(count+1)


# newkey = datasetdb.push().key
# datasetdb.patch('adf',data)


# datasetdb.child(count+1).set(data)
# message = database.child('Panel1')
# message.set(0)