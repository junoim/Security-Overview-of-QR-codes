from firestore_operations import check_url_safety

def main():
    while True:
        url = input("\nEnter a URL to check (or type 'exit' to quit): ").strip()
        if url.lower() == "exit":
            print("Exiting program...")
            break

        result = check_url_safety(url)

        if result == "malicious":
            print(f"🚨 {url} is MALICIOUS!")
        elif result == "safe":
            print(f"✅ {url} is SAFE!")
        else:
            print(f"⚠️ Unable to determine safety of {url}.")

if __name__ == "__main__":
    main()
