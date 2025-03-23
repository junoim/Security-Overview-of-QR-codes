from firestore_operations import check_url_safety

# List of tricky URLs to check
tricky_urls = [
    "https://bit.ly/3abcXYZ",
    "https://xn--pple-43d.com",
    "https://secure-login-verify.com",
    "https://www.example.com/redirect?url=https://www.safe-site.com",
    "https://www.example.com/%7Euser/profile",
    "https://mail.service.example.com"
]

# Check each URL
for url in tricky_urls:
    result = check_url_safety(url)
    print(f"🔎 {url} -> {result}")
