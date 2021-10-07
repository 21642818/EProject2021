from datetime import datetime
from plant import SmartPlant
import os

from apscheduler.schedulers.blocking import BlockingScheduler

os.system('sudo htpdate -s firebase.google.com')
sp = SmartPlant()

def update_database():
    sp.measure()
    data = sp.return_data()
    #folder = '/data/'+data['date']+'/'+data['timestamp']
    print(data)
    #result = firebase.post(url=folder, data=data)
    #print(result)
    #imageBlob = bucket.blob('/')
    #imagePath = data["img_path"]
    #imageBlob = bucket.blob(data["img_path"])
    #imageBlob.upload_from_filename(imagePath)
    print('Tick! The time is: %s' % datetime.now())


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(update_database, 'interval', seconds=30)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass