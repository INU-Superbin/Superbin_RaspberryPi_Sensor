import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('./motor.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://world-best-bin-default-rtdb.firebaseio.com'})

ref = db.reference()
ref.update({'can' : 0})

ref = db.reference()
ref.update({'pet' : 0})
