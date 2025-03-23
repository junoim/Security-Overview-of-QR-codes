import firebase_admin
from firebase_admin import credentials, firestore
import requests
import urllib.parse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Firebase credentials path
FIREBASE_CREDENTIALS = "C:/Users/SHRADHA/OneDrive/Desktop/Project_file/serviceAccountKey.json"

if not FIREBASE_CREDENTIALS:
    raise ValueError("❌ Firebase credentials not found! Check your .env file or set the correct path.")

# Initialize Firebase only if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def encode_url(url):
    """Encodes URL for Firestore-safe document names."""
    return urllib.parse.quote(url, safe="")

def decode_url(encoded_url):
    """Decodes Firestore document ID back to a readable URL."""
    return urllib.parse.unquote(encoded_url)

def normalize_url(url):
    """Normalizes URL to avoid duplicate entries with different formats."""
    parsed_url = urllib.parse.urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}".lower()  # Removes paths, queries, etc.

def add_url_to_firestore(url, status):
    """Stores the URL in Firestore with its safety status."""
    try:
        normalized_url = normalize_url(url)
        encoded_url = encode_url(normalized_url)
        doc_ref = db.collection("urls").document(encoded_url)
        doc_ref.set({
            "original_url": url,
            "status": status,
            "checked_at": firestore.SERVER_TIMESTAMP
        })
        print(f"✅ Firestore Update: {normalized_url} stored as {status}.")
    except Exception as e:
        print(f"❌ Firestore error: {e}")

def get_url_status_from_firestore(url):
    """Checks if the URL exists in Firestore and returns its status."""
    try:
        normalized_url = normalize_url(url)
        encoded_url = encode_url(normalized_url)
        doc_ref = db.collection("urls").document(encoded_url)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()["status"]
        return None
    except Exception as e:
        print(f"❌ Firestore lookup error: {e}")
        return None

def check_url_with_api(url):
    """Checks the URL using Google Safe Browsing API."""
    API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")

    if not API_KEY:
        print("❌ Google Safe Browsing API Key not found! Please check your .env file.")
        return "error"

    try:
        normalized_url = normalize_url(url)
        API_URL = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
        
        payload = {
            "client": {"clientId": "your_project_name", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": normalized_url}]
            }
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            if "matches" in result:
                return "malicious"
            else:
                return "safe"
        else:
            print(f"⚠️ API request failed: {response.status_code}, {response.text}")
            return "unknown"

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return "error"
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return "error"

def check_url_safety(url):
    """Check Firestore first, then API if needed."""
    print(f"\n🔍 Checking URL: {url}")

    # Step 1: Check Firestore first
    status = get_url_status_from_firestore(url)
    if status:
        print(f"📌 {url} found in Firestore as {status}.")
        return status

    # Step 2: If not found in Firestore, check with the API
    print(f"🌐 {url} not found in Firestore. Checking Google Safe Browsing API...")
    status = check_url_with_api(url)

    # Step 3: If API is uncertain, store in Firestore as "unknown"
    if status == "unknown":
        print("🔄 API could not determine the status. Storing as 'unknown' in Firestore.")
        add_url_to_firestore(url, "unknown")

    elif status:
        add_url_to_firestore(url, status)  # Store API result in Firestore

    return status
