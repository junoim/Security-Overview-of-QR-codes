import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase using the service account key
cred = credentials.Certificate("serviceAccountKey.json")  # Make sure this matches your file name
firebase_admin.initialize_app(cred)

# Initialize Firestore Database
db = firestore.client()

print("✅ Firebase setup successful!")
