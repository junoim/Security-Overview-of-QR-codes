import cv2
from pyzbar.pyzbar import decode
from PIL import Image

def scan_qr_code(image_path):
    """
    Scans a QR code from an image file and extracts the URL.
    """
    try:
        # Load the image
        image = cv2.imread(image_path)

        # Decode QR code(s)
        decoded_objects = decode(image)

        if decoded_objects:
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8")
                print(f"🔍 Extracted QR Code Data: {qr_data}")
                return qr_data  # Return the extracted text (URL or other data)

        print("⚠️ No QR Code found in the image.")
        return None

    except Exception as e:
        print(f"❌ Error scanning QR Code: {e}")
        return None
