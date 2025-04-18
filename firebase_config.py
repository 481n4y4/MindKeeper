import pyrebase

firebase_config = {
    "apiKey": "AIzaSyCRh8wFsYJNXvLvo3nTqv35nG-AG1nPXNc",
    "authDomain": "mindkeeper-trailblazers.firebaseapp.com",
    "databaseURL": "https://mindkeeper-trailblazers-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "mindkeeper-trailblazers",
    "storageBucket": "mindkeeper-trailblazers.firebasestorage.app",
    "messagingSenderId": "1049112821852",
    "appId": "1:1049112821852:web:6474ef57283b293a1b2699"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

def get_data(path):
    return db.child(path).get().val()

def set_data(path, data):
    return db.child(path).set(data)

def set_data(path, data):
    return db.child(path).set(data)

# Tambahkan ini:
__all__ = ["get_data", "set_data", "db"]
