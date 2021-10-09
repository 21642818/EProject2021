from google.cloud import storage
import os
from firebase import firebase

os.system('sudo htpdate -s firebase.google.com')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/var/local/eproject2021-555cc-firebase-adminsdk-94yit-faec66311f.json"
firebase = firebase.FirebaseApplication('https://eproject2021-555cc-default-rtdb.europe-west1.firebasedatabase.app/', None)

def post_firebase_test():
    data = {
        "watering" : [0,0,1,0],
        "triggers" : [5,5,5,5],
    }
    folder = "/cmd/"
    result = firebase.post(url=folder, data=data)
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

post_firebase_test()
