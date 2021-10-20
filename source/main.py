from time import process_time
from plant import SmartPlant
from google.cloud import storage
import os
from firebase import firebase
from apscheduler.schedulers.blocking import BlockingScheduler
import faulthandler; faulthandler.enable()

os.system('sudo htpdate -s firebase.google.com')

sp = SmartPlant()
picture_counter = 0

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/var/local/eproject2021-555cc-firebase-adminsdk-94yit-faec66311f.json"
firebase = firebase.FirebaseApplication('https://eproject2021-555cc-default-rtdb.europe-west1.firebasedatabase.app/', None)
client = storage.Client()
bucket = client.get_bucket('eproject2021-555cc.appspot.com')

def post_firebase(self):
    sp.measure()
    data = sp.return_data()
    folder = '/data/'+data['date']+'/'+data['timestamp']
    print(data)
    result = firebase.post(url=folder, data=data)
    print(result)
    if data["img_path"] != None:
        imageBlob = bucket.blob('/')
        imagePath = data["img_path"]
        imageBlob = bucket.blob(data["img_path"])
        imageBlob.upload_from_filename(imagePath)
    pass

def get_firebase():
    folder_cmd = "/cmd/"
    folder_trig = "/trig/"
    result_cmd = firebase.get(folder_cmd, None)
    result_trig = firebase.get(folder_trig, None)
    if result_cmd != None:
        for r in result_cmd:
            watering = result_cmd[r]["watering"]
            break
    else:
        watering = [0, 0, 0, 0]
    if result_trig != None:
        for t in result_trig:
            triggers = result_trig[t]["triggers"]
    else:
        triggers = None

    flag = sp.water(watering,1.5,triggers)
    if flag:
        status = firebase.delete(folder_cmd, name=None)
        status = firebase.delete(url="/flags/", name=None)
    else:
        status = firebase.post(url="/flags/", data={"watered" : flag})
    #print(status)
    pass

if __name__ == '__main__':
    get_firebase()
    post_firebase()
    scheduler = BlockingScheduler(job_defaults={'max_instances': 2})
    scheduler.add_job(post_firebase, 'interval', seconds=1800)
    scheduler.add_job(get_firebase, 'interval', seconds=30)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
