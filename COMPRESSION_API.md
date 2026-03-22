# 📉 Compression API Documentation

This document describes the Image and PDF compression endpoints available in the SwiftConvert service.

## 1. Image Compression
**Endpoint**: `/api/compress-image/`  
**Method**: `POST`  
**Content-Type**: `multipart/form-data`

### **Fields**
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `file` | File | Yes | Image file to compress (Supports HEIC, JPG, PNG). |
| `quality` | Integer | No | Image quality (1-95). Higher numbers mean better quality and larger size. |

### **Recommended Quality Presets**
- **30** (Low Quality): Extreme compression for maximum size reduction.
- **50** (Medium Quality): Good balance between visual quality and file size.
- **78** (High Quality): Recommended for best visual fidelity.

---

## 2. PDF Compression
**Endpoint**: `/api/compress-pdf/`  
**Method**: `POST`  
**Content-Type**: `multipart/form-data`

### **Fields**
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `file` | File | Yes | PDF file to compress. |
| `quality` | Integer | No | Internal image quality (1-95). Re-encodes images inside the PDF. |

### **How it Works**
- This service re-encodes all embedded images in the PDF at the specified quality.
- It also performs garbage collection and stream deflation to further reduce size.
- Results are 100% compatible with Adobe Acrobat and other major PDF viewers.

---

## Example Usage

### JavaScript (`fetch`)
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('quality', 50);

const response = await fetch('http://<YOUR_IP>:8001/api/compress-image/', {
  method: 'POST',
  body: formData
});
const data = await response.json();
console.log(`Saved: ${data.saved_percent}%`);
window.location.href = data.converted_url;
```

### cURL
```bash
curl -X POST \
  -F "file=@document.pdf" \
  -F "quality=30" \
  http://<YOUR_IP>:8001/api/compress-pdf/
```

---

## Response Format
Success Response (`200 OK`):
```json
{
  "message": "File compressed successfully",
  "converted_url": "http://<IP>:8001/media/compressed/file_20260323_001045.jpg",
  "original_size": 250432,
  "compressed_size": 184320,
  "saved_percent": 26.4
}
```
> [!TIP]
> If the file is already optimized and cannot be reduced further, `saved_percent` will be `0.0` and the original file will be returned as the `converted_url`.
