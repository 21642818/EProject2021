from google.cloud import storage
import os
from firebase import firebase

os.system('sudo htpdate -s firebase.google.com')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/var/local/eproject2021-555cc-firebase-adminsdk-94yit-faec66311f.json"
firebase = firebase.FirebaseApplication('https://eproject2021-555cc-default-rtdb.europe-west1.firebasedatabase.app/', None)

def post_firebase_test():
    data = {
        "watering" : [1,0,0,0]
    }
    folder = "/cmd/"
    result = firebase.post(url=folder, data=data)
    print(result)

def get_firebase_test():
    folder = "/cmd/"
    result = firebase.get(url=folder, name=None)
    for r in result:
       print(result[r]["watering"])

def delete_firebase_test():
    folder = "/cmd/"
    result = firebase.delete(url=folder, name=None)
    print(result)

get_firebase_test()
