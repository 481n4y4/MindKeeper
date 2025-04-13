# import pyrebase

# firebase_config = {
#     "apiKey": "AIzaSyCRh8wFsYJNXvLvo3nTqv35nG-AG1nPXNc",
#     "authDomain": "mindkeeper-trailblazers.firebaseapp.com",
#     "databaseURL": "https://mindkeeper-trailblazers-default-rtdb.asia-southeast1.firebasedatabase.app/",
#     "projectId": "mindkeeper-trailblazers",
#     "storageBucket": "mindkeeper-trailblazers.firebasestorage.app",
#     "messagingSenderId": "1049112821852",
#     "appId": "1:1049112821852:web:6474ef57283b293a1b2699"
# }

# firebase = pyrebase.initialize_app(firebase_config)
# db = firebase.database()

import requests
import json

FIREBASE_DB_URL = "https://mindkeeper-trailblazers-default-rtdb.asia-southeast1.firebasedatabase.app/"

def get_data(path):
    url = f"{FIREBASE_DB_URL}/{path}.json"
    response = requests.get(url)
    return response.json()

def set_data(path, data):
    url = f"{FIREBASE_DB_URL}/{path}.json"
    response = requests.put(url, data=json.dumps(data))
    return response.json()

