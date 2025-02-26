from firestore_operations import check_url_safety

# Example URLs to check
test_urls = [
    "https://example.com",
    "http://malicious-site.com"
]

# Check URLs
for url in test_urls:
    status = check_url_safety(url)
    print(f"🔎 {url} -> {status}")
