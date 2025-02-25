import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/SHRADHA/OneDrive/Desktop/Project_file/serviceAccountKey.json")  # Update with your actual path
    firebase_admin.initialize_app(cred)

# Get Firestore database instance
db = firestore.client()

# 🔹 1️⃣ Function to ADD QR Code data
def add_qr_code(qr_id, data):
    """
    Adds a QR code to Firestore.

    :param qr_id: Unique ID for the QR code
    :param data: Dictionary containing QR code data
    """
    db.collection("qr_codes").document(qr_id).set(data)
    print(f"✅ QR Code {qr_id} added successfully!")


# 🔹 2️⃣ Function to RETRIEVE QR Code data
def get_qr_code(qr_id):
    """
    Retrieves QR code data from Firestore.

    :param qr_id: Unique ID of the QR code
    :return: Dictionary with QR code data or None if not found
    """
    doc = db.collection("qr_codes").document(qr_id).get()
    if doc.exists:
        print(f"📌 QR Code {qr_id} found: {doc.to_dict()}")
        return doc.to_dict()
    else:
        print(f"❌ QR Code {qr_id} not found!")
        return None


# 🔹 3️⃣ Function to UPDATE QR Code data
def update_qr_code(qr_id, updated_data):
    """
    Updates an existing QR code in Firestore.

    :param qr_id: Unique ID of the QR code
    :param updated_data: Dictionary with updated fields
    """
    doc_ref = db.collection("qr_codes").document(qr_id)
    if doc_ref.get().exists:
        doc_ref.update(updated_data)
        print(f"✅ QR Code {qr_id} updated successfully!")
    else:
        print(f"❌ QR Code {qr_id} not found!")


# 🔹 4️⃣ Function to DELETE QR Code data
def delete_qr_code(qr_id):
    """
    Deletes a QR code from Firestore.

    :param qr_id: Unique ID of the QR code
    """
    doc_ref = db.collection("qr_codes").document(qr_id)
    if doc_ref.get().exists:
        doc_ref.delete()
        print(f"🗑️ QR Code {qr_id} deleted successfully!")
    else:
        print(f"❌ QR Code {qr_id} not found!")

import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/SHRADHA/OneDrive/Desktop/Project_file/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Google Safe Browsing API Key (Replace with your actual key)
API_KEY = "YOUR_GOOGLE_SAFE_BROWSING_API_KEY"

def check_url_safety(url):
    """
    Checks if a URL is malicious using Google Safe Browsing API.
    Stores the result in Firestore for future reference.
    """
    # Check Firestore first (local database)
    existing_doc = db.collection("urls").document(url).get()
    if existing_doc.exists:
        print(f"📌 URL found in database: {url} -> {existing_doc.to_dict()['status']}")
        return existing_doc.to_dict()["status"]

    # If not found, check with the Google Safe Browsing API
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
    payload = {
        "client": {"clientId": "your_project", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    response = requests.post(api_url, json=payload)
    result = response.json()

    # Determine status
    if "matches" in result:
        status = "unsafe"
        print(f"⚠️ ALERT: {url} is MALICIOUS!")
    else:
        status = "safe"
        print(f"✅ SAFE: {url}")

    # Store the result in Firestore
    db.collection("urls").document(url).set({"status": status})
    
    return status

import base64
from google.cloud import firestore

db = firestore.Client()

def encode_url(url):
    """Encodes the URL to make it Firestore-safe."""
    return base64.urlsafe_b64encode(url.encode()).decode()

def check_url_safety(url):
    """Checks if the URL exists in Firestore and returns its status."""
    encoded_url = encode_url(url)
    existing_doc = db.collection("urls").document(encoded_url).get()

    if existing_doc.exists:
        return existing_doc.to_dict().get("status", "Unknown")
    else:
        return "Not found in database"


