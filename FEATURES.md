# ✨ SwiftConvert: Feature Overview

SwiftConvert is a powerful, lightweight tool for handling your image and document conversions. It is designed for speed, quality, and simplicity.

---

## 🖼️ Image Features

### **1. Format Conversion**
Easily switch between common image formats. Perfect for making HEIC (iPhone) photos compatible with other systems.
- **Supports**: `HEIC`, `JPG`, `PNG`, `WEBP`.
- **Output**: High-quality `JPG` or `PNG`.

### **2. Smart Compression**
Reduce image file sizes by up to 90% without losing noticeable quality.
- **Customizable Quality**: Choose between "Extreme", "Medium", or "High" quality presets.
- **Smart Logic**: Automatically picks the best format for the smallest size.

### **3. Image to PDF**
Turn your photos into professional PDF documents.
- **Single Mode**: One image → One PDF.
- **Merge Mode**: Combine multiple images into a single multi-page PDF document.

### **4. Image to Word (OCR)**
Convert images containing text into editable Microsoft Word (.docx) files.

---

## 📄 PDF Features

### **5. PDF Compression**
Shrink large PDF files for easier sharing via email or messaging apps.
- **Image Re-optimization**: Re-encodes embedded images to save space.
- **Compatibility**: Results remain 100% compatible with Adobe Acrobat and all major PDF viewers.

---

## 🌐 Connectivity Features

### **6. Cross-System API**
All features are available via a REST API, allowing other systems (like your custom scripts or mobile apps) to use the SwiftConvert engine.
- **Format-friendly**: Easy-to-use `multipart/form-data` endpoints.
- **Remote Access**: Works over your local Wi-Fi.

### **7. Web Interface**
A beautiful, responsive web dashboard to perform all conversions in your browser.

---

## 🛠️ Technical Implementation

SwiftConvert uses industry-standard libraries to ensure maximum compatibility and performance:

- **Image Engine**: Powered by [Pillow](https://python-pillow.org/) and [Pillow-HEIF](https://github.com/cascornelissen/pillow-heif) for specialized iPhone format support.
- **PDF Engine**: Powered by [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) for high-performance PDF manipulation and stream compression.
- **Office Engine**: Powered by [python-docx](https://python-docx.readthedocs.io/) for generating clean Microsoft Word documents.

---

> [!TIP]
> Use the **Merge to PDF** feature to quickly create a single document from multiple scanned pages or screenshots!
