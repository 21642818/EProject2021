from plant import SmartPlant
from google.cloud import storage
import os
from firebase import firebase

sp = SmartPlant()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/var/local/eproject2021-555cc-firebase-adminsdk-94yit-faec66311f.json"
firebase = firebase.FirebaseApplication('https://eproject2021-555cc-default-rtdb.europe-west1.firebasedatabase.app/', None)
client = storage.Client()
bucket = client.get_bucket('https://console.firebase.google.com/project/eproject2021-555cc/storage/eproject2021-555cc.appspot.com/files')

def update_database():
    sp.measure()
    data = sp.return_data()
    folder = '/data/'+data['date']+'/'+data['timestamp']
    print(data)
    result = firebase.post(url=folder, data=data)
    print(result)
    imagePath = data["img"]
    imageBlob = data['date']+'/'
    imageBlob.upload_from_filename(imagePath)


update_database()
