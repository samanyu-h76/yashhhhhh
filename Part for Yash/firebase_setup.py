import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    # Make sure the path matches the downloaded JSON key file
    cred = credentials.Certificate("restaurant-data-backend-firebase-adminsdk-fbsvc-bdeb44e4a8.json")

    # Prevent multiple initializations
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    return firestore.client()
