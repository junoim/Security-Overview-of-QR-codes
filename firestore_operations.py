import firebase_admin
from firebase_admin import credentials, firestore
import requests
import urllib.parse
import os

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/SHRADHA/OneDrive/Desktop/Project_file/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Secure API Key Storage
API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")

def encode_url(url):
    """Encodes a URL safely for Firestore document names."""
    return urllib.parse.quote(url, safe="")

def add_url_to_firestore(url, status):
    """Adds a URL with its safety status to Firestore."""
    encoded_url = encode_url(url)
    db.collection("urls").document(encoded_url).set({"status": status})
    print(f"✅ URL {url} added successfully as {encoded_url}!")

def check_url_in_firestore(url):
    """Checks if a URL is already stored in Firestore."""
    encoded_url = encode_url(url)
    doc = db.collection("urls").document(encoded_url).get()
    
    if doc.exists:
        status = doc.to_dict().get("status", "Unknown")
        print(f"📌 {url} -> Found in database as {status}")
        return status
    else:
        print(f"🔍 {url} -> Not found in database")
        return None

def check_url_safety(url):
    """Checks URL safety: First in Firestore, then Google Safe Browsing API if not found."""
    status = check_url_in_firestore(url)
    if status is not None:
        return status  # ✅ If found in Firestore, return existing status.

    # Call Google Safe Browsing API
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

    if "matches" in result:
        status = "unsafe"
        print(f"⚠️ ALERT: {url} is MALICIOUS!")
    else:
        status = "safe"
        print(f"✅ SAFE: {url}")

    # Store the result in Firestore for future reference
    add_url_to_firestore(url, status)
    return status

# Function to test adding and checking URLs
if __name__ == "__main__":
    test_urls = [
        "https://example.com",
        "http://malicious-site.com"
    ]
    
    for url in test_urls:
        check_url_safety(url)
