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


from qr_scanner import scan_qr_code

image_path = "test_qr.png"  # Replace with the actual path to your QR code image
extracted_url = scan_qr_code(image_path)

if extracted_url:
    print(f"Extracted URL: {extracted_url}")
else:
    print("No URL found in the QR code.")
