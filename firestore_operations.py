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
