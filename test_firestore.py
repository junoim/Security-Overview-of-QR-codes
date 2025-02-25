from firestore_operations import add_qr_code, get_qr_code, update_qr_code, delete_qr_code

# Sample QR Code Data
qr_id = "12345"
qr_data = {"name": "Test QR", "url": "https://example.com", "scanned": 0}

# 1️⃣ Add a QR Code
add_qr_code(qr_id, qr_data)

# 2️⃣ Retrieve the QR Code
get_qr_code(qr_id)

# 3️⃣ Update the QR Code
update_qr_code(qr_id, {"scanned": 5})

# 4️⃣ Delete the QR Code
delete_qr_code(qr_id)
