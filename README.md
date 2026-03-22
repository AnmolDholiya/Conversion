# Image Conversion API

This is a Django-based API for converting images between formats (HEIC, JPG, PNG), to PDF, and to Word documents (DOCX). It is designed to be fully compatible with iOS device uploads (HEIC).

## Table of Contents
- [Local Network Setup](#local-network-setup)
- [Endpoints](#endpoints)
  - [1. Convert Image Format](#1-convert-image-format)
  - [2. Convert Image to PDF (Single or Merge)](#2-convert-image-to-pdf-single-or-merge)
  - [3. Convert Image to Word](#3-convert-image-to-word)
  - [4. Compress Image](#4-compress-image)
  - [5. Compress PDF](#5-compress-pdf)
- [Response Format](#response-format)
- [Example Usage](#example-usage)

---

## Local Network Setup

To use the API from another device (like an iPhone or Android) on the same Wi-Fi:
1.  **Find your IP address**:
    - Windows: `ipconfig` (Your current IP is: `10.158.19.134`)
2.  **Run the Backend on your IP**:
    ```bash
    python manage.py runserver 0.0.0.0:8001
    ```
3.  **Run the Frontend on your IP**:
    ```bash
    cd frontend
    npm run host
    ```
4.  **Access on other devices**:
    - Frontend: `http://10.158.19.134:5173`
    - API: `http://10.158.19.134:8001/api/`

---

## Endpoints

All endpoints require `POST` requests with `Content-Type: multipart/form-data`.

### 1. Convert Image Format
- **Endpoint**: `/api/convert-image-format/`
- **Fields**:
  - `file`: (Required) HEIC, JPG, or PNG file.
  - `target_format`: (Optional) `JPG` or `PNG`. Default is `JPG`.
- **Action**: Converts any image (including HEIC) to the target format.

### 2. Convert Image to PDF (Single or Merge)
- **Endpoint**: `/api/convert-to-pdf/`
- **Fields**:
  - `file`: (Required) One or more image files.
  - `merge`: (Optional) Set to `true` to merge multiple files into a single multi-page PDF.
- **Action**: Generates a PDF from a single image or merges multiple images into one PDF.

### 3. Convert Image to Word
- **Endpoint**: `/api/convert-to-word/`
- **Fields**:
  - `file`: (Required) HEIC, JPG, or PNG file.
- **Action**: Generates a `.docx` file with the image inserted.

### 4. Compress Image
- **Endpoint**: `/api/compress-image/`
- **Fields**:
  - `file`: (Required) Image file to compress.
  - `quality`: (Optional) Integer 1-95. (Presets: Extreme=30, High=50, Recommended=78).
- **Action**: Compresses image using smart logic (tries JPEG/PNG, picks smallest).

### 5. Compress PDF
- **Endpoint**: `/api/compress-pdf/`
- **Fields**:
  - `file`: (Required) PDF file to compress.
  - `quality`: (Optional) Integer 1-95.
- **Action**: Re-encodes internal PDF images to reduce file size.

---

## Response Format

Success Response (`200 OK`):
```json
{
  "message": "Image converted successfully",
  "converted_url": "http://192.168.1.10:8001/media/conversions/photo_20260322_163812.jpg"
}
```

Error Response (`400 Bad Request` or `500 Internal Server Error`):
```json
{
  "error": "Error message description"
}
```

---

## Example Usage

### JavaScript (fetch)
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('target_format', 'PNG');

const response = await fetch('http://<YOUR_IP>:8001/api/convert-image-format/', {
  method: 'POST',
  body: formData
});
const data = await response.json();
console.log(data.converted_url);
```

### Swift (iOS)
```swift
let url = URL(string: "http://<YOUR_IP>:8001/api/convert-to-pdf/")!
var request = URLRequest(url: url)
request.httpMethod = "POST"

let boundary = "Boundary-\(UUID().uuidString)"
request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

// ... build your multipart body with the file data ...
```

### cURL
```bash
curl -X POST -F "file=@image.heic" -F "target_format=PNG" http://<YOUR_IP>:8001/api/convert-image-format/
```
