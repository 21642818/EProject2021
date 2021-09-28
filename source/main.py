from plant import SmartPlant
from google.cloud import storage
from firebase import firebase

sp = SmartPlant()
firebase = firebase.FirebaseApplication('https://YOUR_FIREBASE_URL.firebaseio.com/', None)
client = storage.Client()
bucket = client.get_bucket('<your firebase storage path>')

def update_database():
    sp.measure()
    data = sp.return_data
    firebase.post('/data/', data) 
    imagePath = data["img"]
    imageBlob =  sp.return_last_img_name()
    imageBlob.upload_from_filename(imagePath)


print(sp.return_data())