# 🚀 SwiftConvert API Guide (External Systems)

Use the following endpoints to interact with the SwiftConvert service from any other system.

**Base URL**: `http://192.168.137.202:8001/api/`

---

## 📸 Image Endpoints

### 1. Convert Image Format
Change an image's format (e.g., JPEG to PNG).
- **URL**: `http://192.168.137.202:8001/api/convert-image-format/`
- **Method**: `POST`
- **Body (`multipart/form-data`)**:
  - `file`: The image file.
  - `target_format`: (Optional) `JPG` or `PNG`. Default is `JPG`.

### 2. Compress Image
Reduce an image's file size.
- **URL**: `http://192.168.137.202:8001/api/compress-image/`
- **Method**: `POST`
- **Body (`multipart/form-data`)**:
  - `file`: The image file.
  - `quality`: (Optional) `1-95`. Default is `60`.

---

## 📄 Document Endpoints

### 3. Convert to PDF
Convert one or more images into a PDF document.
- **URL**: `http://192.168.137.202:8001/api/convert-to-pdf/`
- **Method**: `POST`
- **Body (`multipart/form-data`)**:
  - `file`: One or more image files.
  - `merge`: (Optional) `true` or `false`. Merge multiple images into one PDF.

### 4. Convert to Word
Convert an image to a Word document (.docx).
- **URL**: `http://192.168.137.202:8001/api/convert-to-word/`
- **Method**: `POST`
- **Body (`multipart/form-data`)**:
  - `file`: The image file.

### 5. Compress PDF
Reduce a PDF's file size.
- **URL**: `http://192.168.137.202:8001/api/compress-pdf/`
- **Method**: `POST`
- **Body (`multipart/form-data`)**:
  - `file`: The PDF file.
  - `quality`: (Optional) `1-95`. Default is `60`.

---

## 📥 Download Endpoint

### 6. Download File
Force download a file using its relative path.
- **URL**: `http://192.168.137.202:8001/api/download/?path=<FILE_PATH>`
- **Method**: `GET`
- **Parameter**: `path` (The relative path returned in `converted_url`).

---

## 🐍 Python Example (using `requests`)

```python
import requests

# Set your server IP and Port
BASE_URL = "http://192.168.137.202:8001/api/"

def compress_image(image_path, quality=60):
    url = f"{BASE_URL}compress-image/"
    files = {'file': open(image_path, 'rb')}
    data = {'quality': quality}
    
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        result = response.json()
        print(f"Compressed! Download here: {result['converted_url']}")
        print(f"Space saved: {result['saved_percent']}%")
    else:
        print(f"Error: {response.text}")

# compress_image("my_photo.jpg", quality=50)
```
