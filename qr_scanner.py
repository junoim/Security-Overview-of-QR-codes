import cv2
import pyzbar.pyzbar as pyzbar
from firestore_operations import check_url_safety

def scan_qr_code_from_webcam():
    """Scans a QR code using the webcam and extracts the URL."""
    cap = cv2.VideoCapture(0)  # Open webcam
    print("Show the QR code to the camera... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            url = obj.data.decode('utf-8')
            print(f" Extracted URL: {url}")
            cap.release()
            cv2.destroyAllWindows()
            return url  # Return the first URL found

        cv2.imshow("QR Scanner", frame)

        # Press 'q' to exit scanning
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

if __name__ == "__main__":
    while True:
        extracted_url = scan_qr_code_from_webcam()

        if extracted_url:
            print(f" Checking security for: {extracted_url}")
            status = check_url_safety(extracted_url)
            print(f"Final Classification: {extracted_url} -> {status}")
        else:
            print("No valid URL extracted from the QR code.")

        # Ask if the user wants to scan another QR code
        again = input("\n Do you want to scan another QR code? (yes/no): ").strip().lower()
        if again != "yes":
            print("Exiting program...")
            break
