import requests
import json

# Configuration
SERVER_IP = "192.168.137.202"
PORT = "8001"
BASE_URL = f"http://{SERVER_IP}:{PORT}/api/"

def compress_image(file_path, quality=60):
    """Example of calling the image compression API."""
    url = f"{BASE_URL}compress-image/"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'quality': quality}
            
            print(f"Connecting to {url}...")
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("SUCCESS!")
                print(f"Original Size: {result['original_size']} bytes")
                print(f"Compressed Size: {result['compressed_size']} bytes")
                print(f"Saved: {result['saved_percent']}%")
                print(f"URL: {result['converted_url']}")
                return result['converted_url']
            else:
                print(f"FAILED: {response.status_code}")
                print(response.text)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

def convert_to_pdf(file_paths, merge=True):
    """Example of converting images to a single PDF."""
    url = f"{BASE_URL}convert-to-pdf/"
    
    files = []
    opened_files = []
    try:
        for path in file_paths:
            f = open(path, 'rb')
            opened_files.append(f)
            files.append(('file', f))
        
        data = {'merge': str(merge).lower()}
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"PDF Created: {result['converted_url']}")
            return result['converted_url']
        else:
            print(f"Failed to create PDF: {response.text}")
    finally:
        for f in opened_files:
            f.close()

if __name__ == "__main__":
    print("SwiftConvert API Client Example")
    print("-" * 30)
    # Uncomment and replace with a local file path to test
    # compress_image("test_image.jpg", quality=50)
