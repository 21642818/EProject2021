from plant import SmartPlant
from google.cloud import storage
from firebase import firebase

sp = SmartPlant()
firebase = firebase.FirebaseApplication('https://eproject2021-555cc-default-rtdb.europe-west1.firebasedatabase.app/', None)
#client = storage.Client()
#bucket = client.get_bucket('<your firebase storage path>')

def update_database():
    sp.measure()
    data = sp.return_data()
    folder = '/data/'+data['date']+'/'+data['timetamp']
    print(data)
    #result = firebase.post(url=folder, data=data)
    #print(result) 
    #imagePath = data["img"]
    #imageBlob = sp.return_last_img_name()
    #imageBlob.upload_from_filename(imagePath)


update_database()