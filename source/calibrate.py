import os
from firebase import firebase
from numpy.core.arrayprint import DatetimeFormat
from plant import SmartPlant

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/var/local/eproject2021-555cc-firebase-adminsdk-94yit-faec66311f.json"
auth = firebase.FirebaseAuthentication(secret='TFpXyKJjxfoQwed62o5mDFlXwT8h16JlxNmZHqHC', email='gerth.mmarais@gmail.com')
firebase.authentication = auth
firebase = firebase.FirebaseApplication('https://eproject2021-555cc-default-rtdb.europe-west1.firebasedatabase.app/', auth)
sp = SmartPlant()

(min_cali, max_cali) = sp.calibrate()
data = {
    'min': min_cali,
    'max': max_cali,
}
folder = "/calibration/"
result = firebase.get(url=folder, name=None)
if result != None:
    for r in result:
        update_folder = folder+r
        firebase.put(url=update_folder, name='min', data=min_cali)
        firebase.put(url=update_folder, name='max', data=max_cali)
else:
    firebase.post(url=folder, data=data)