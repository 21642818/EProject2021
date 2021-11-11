from google.cloud import storage
import os
from firebase import firebase

os.system('sudo htpdate -s firebase.google.com')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/var/local/eproject2021-555cc-firebase-adminsdk-94yit-faec66311f.json"
auth = firebase.FirebaseAuthentication(secret='TFpXyKJjxfoQwed62o5mDFlXwT8h16JlxNmZHqHC', email='gerth.mmarais@gmail.com')
firebase.authentication = auth
firebase = firebase.FirebaseApplication('https://eproject2021-555cc-default-rtdb.europe-west1.firebasedatabase.app/', auth)


def post_firebase_test():
    data_watering = {
        "watering" : [0,0,0,0],
        
    }
    data_triggers = {
        "triggers" : [5,5,5,5],
    }
    folder_watering = "/cmd/"
    folder_triggers = "/trig/"
    #result_watering = firebase.post(url=folder_watering, data=data_watering)
    #firebase.delete(folder_triggers,None)
    #result_triggers = firebase.post(url=folder_triggers, data=data_triggers)
    result = firebase.post(url="/flag/", data={"float_switch" : False})
    print(result)

def get_firebase_test():
    folder = "/cmd/"
    result = firebase.get(url=folder, name=None)
    print(result)
    if result != None:
        for r in result:
            print(result[r]["watering"])
            try:
                print(result[r]["triggers"])
            except:
                print("No new triggers")
                break

def delete_firebase_test():
    folder = "/cmd/"
    result = firebase.delete(url=folder, name=None)
    print(result)

def reverse_firebase():
    result = firebase.get(url="/data/", name=None)
    for date in result:
        for time in date:
            print(time)
            break
        break


reverse_firebase()
