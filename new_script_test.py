import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/SHRADHA/OneDrive/Desktop/Project_file/serviceAccountKey.json"

from google.cloud import firestore

# Check if the credentials are set
print("GOOGLE_APPLICATION_CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# Initialize Firestore
try:
    db = firestore.Client()
    print("Firestore connection successful! 🎉")
except Exception as e:
    print("Firestore connection failed:", e)
