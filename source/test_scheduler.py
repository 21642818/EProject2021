from datetime import datetime
from plant import SmartPlant
import os
from firebase import firebase
from google.cloud import storage
from apscheduler.schedulers.blocking import BlockingScheduler

os.system('sudo htpdate -s firebase.google.com')
sp = SmartPlant()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/var/local/eproject2021-555cc-firebase-adminsdk-94yit-faec66311f.json"
firebase = firebase.FirebaseApplication('https://eproject2021-555cc-default-rtdb.europe-west1.firebasedatabase.app/', None)
client = storage.Client()
bucket = client.get_bucket('eproject2021-555cc.appspot.com')

def post_firebase():
    sp.measure()
    data = sp.return_data()
    folder = '/data/'+data['date']+'/'+data['timestamp']
    result = firebase.post(url=folder, data=data)
    imageBlob = bucket.blob('/')
    imagePath = data["img_path"]
    imageBlob = bucket.blob(data["img_path"])
    imageBlob.upload_from_filename(imagePath)
    print('**********************************************')
    print('data', data)
    print('firebase response', result)
    print('Tick! The time is: %s' % datetime.now())

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(post_firebase, 'interval', seconds=30)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
