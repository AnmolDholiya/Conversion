# SwiftConvert: System Documentation

SwiftConvert is a high-performance image conversion and compression platform designed for seamless compatibility with iOS (HEIC support) and modern web workflows.

## 🏗️ Architecture Overview

The system follows a decoupled Client-Server architecture:

- **Frontend**: A reactive single-page application (SPA) built with Vite and React.
- **Backend**: A robust RESTful API powered by Django and Django REST Framework (DRF).
- **Processing Engine**: A Python-based set of utilities using Pillow, PyMuPDF, and python-docx.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React (Vite) | Interactive user interface |
| **Backend** | Django / DRF | API orchestration and request handling |
| **Image Engine** | Pillow (PIL) | Core image manipulation and format conversion |
| **HEIC Support** | pillow-heif | Decoding iOS high-efficiency image containers |
| **PDF Engine** | PyMuPDF (fitz) | Advanced PDF compression and re-encoding |
| **Docs Engine** | python-docx | Converting images into formatted Word documents |
| **Icons** | Lucide React | Modern UI iconography |

---

## 🛰️ API Endpoints & Data Flow

All endpoints consume `multipart/form-data` and return JSON responses containing a `converted_url`.

### 1. Image Format Conversion
- **Endpoint**: `/api/convert-image-format/`
- **Logic**: Converts HEIC/JPG/PNG to the specified target format (JPG/PNG).
- **Optimization**: Automatically flattens alpha channels if converting to JPEG.

### 2. Image to PDF (Single & Merge)
- **Endpoint**: `/api/convert-to-pdf/`
- **Logic**: 
  - **Single**: Converts one image to a PDF page.
  - **Merge**: Accepts multiple files and stitches them into a single multi-page PDF document.

### 3. Smart Image Compression
- **Endpoint**: `/api/compress-image/`
- **Logic**: Implements a "best-result" strategy. It compresses the input using both JPEG and PNG optimization techniques, then serves the version with the smallest file size.

### 4. PDF Compression
- **Endpoint**: `/api/compress-pdf/`
- **Logic**: Deep-inspects PDF internal streams, extracts embedded images, re-encodes them using specialized JPEG compression, and rebuilds the PDF structure to reduce bloat.

### 5. Image to Word
- **Endpoint**: `/api/convert-to-word/`
- **Logic**: Wraps the image within a `.docx` container with appropriate scaling for document printing.

---

## 📂 File Management & Security

1. **Storage**: Converted files are stored in a dedicated `media/` directory, organized by conversion type (`conversions/`, `pdfs/`, `compressed/`, `word_docs/`).
2. **Unique Naming**: The system uses a timestamp-based naming convention (`filename_YYYYMMDD_HHMMSS.ext`) to ensure zero naming collisions.
3. **Secure Downloads**: A specialized `/api/download/` view handles file retrieval, sanitizing paths to prevent directory traversal attacks and forcing broad browser compatibility for downloads.

---

## 🚀 Local Network Integration

The system is configured to be accessible across a local network (Wi-Fi), allowing users to upload HEIC photos directly from their iPhone to the server running on a PC.

- **Frontend Host**: `npm run host` (Binds to `0.0.0.0`)
- **Backend Host**: `python manage.py runserver 0.0.0.0:8001`
