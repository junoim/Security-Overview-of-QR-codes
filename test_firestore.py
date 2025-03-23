from firestore_operations import add_url_to_firestore

# Malicious URLs (except one that API should detect)
malicious_urls = [
    "https://bit.ly/3abcXYZ",
    "https://xn--pple-43d.com",
    "https://secure-login-verify.com"
]

# Safe URLs
safe_urls = [
    "https://www.example.com/redirect?url=https://www.safe-site.com",
    "https://www.example.com/%7Euser/profile",
    "https://mail.service.example.com"
]

# Add malicious URLs to Firestore
for url in malicious_urls:
    add_url_to_firestore(url, "malicious")

# Add safe URLs to Firestore
for url in safe_urls:
    add_url_to_firestore(url, "safe")

print("✅ Firestore updated with tricky URLs.")
