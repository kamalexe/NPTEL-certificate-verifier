# ✅ Project Workflow
## 1. User Uploads Folder:
	• Use a web interface (React, HTML/JS, or any frontend framework).
	• Accept folder input or multiple PDF files.

## 2. PDF to Image Conversion:
	• Use a backend (Node.js with pdf2img or Python with pdf2image) to convert each PDF to images (usually PNG/JPG).

## 3. Image Cropping for Data Extraction:
	• Predefine bounding box coordinates for:
		- Name
		- Course Title
		- Score/Grade
		- Roll No
		- Credit
		- Duration
		- QR Code

## 4. QR Code Detection and Reading:
	• Use OpenCV + pyzbar (Python) or JS-based libraries like jsQR (for client-side).
	• Extract URL from the QR code.

## 5. Certificate Download from QR Code URL:
	• Fetch the certificate using the extracted URL (likely a PDF).

## 6. Repeat Step 2 & 3 for Downloaded Certificate:
	• Convert, crop, and extract text data from the downloaded certificate.

## 7. Compare Original vs Downloaded Data:
	• Ensure all key fields (name, course, score, roll no, etc.) match.
	• If they match → ✅ Verified.

## 8. Save Extracted Data:
	• Store extracted values from both original and downloaded certificates in separate CSV files.

## 9. Generate Final Verification Result:
	• Compare both CSVs.
	• Generate a final CSV containing verification status and mismatch reasons.
# 🔧 Recommended Tech Stack
	• Frontend: React.js or basic HTML/CSS/JS
	• Backend: Python (FastAPI/Flask)
	• Libraries:
		- pdf2image (PDF to image)
		- Pillow, pyzbar (Image cropping + QR decoding)
		- pytesseract (OCR)
		- requests + BeautifulSoup (HTML parsing and PDF download)
		- csv (for data storage and comparison)
	• Use a `.env` file to manage all directory paths and configuration.
	• Structure backend as utility modules: `data_extractor`, `verifier`, and `main`.


#  Project Architecture Diagram

```
+-------------------+        +----------------------+       +------------------------+
|  User Interface   |        |     Backend Server   |       |      External Service  |
|  (Web Page)       |        |   (Python/Node.js)   |       | (NPTEL Server via QR)  |
+--------+----------+        +----------+-----------+       +-----------+------------+
         |                            |                                   |
         |-- Upload Folder (PDFs) --> |                                   |
         |                            |                                   |
         |                            |--- Convert PDF to Image --------->|
         |                            |                                   |
         |                            |<---------- Image -----------------|
         |                            |                                   |
         |                            |--- Crop & Extract QR ------------>|
         |                            |                                   |
         |                            |<-- QR URL from QR Reader ---------|
         |                            |                                   |
         |                            |--- Download PDF from URL ---------|
         |                            |                                   |
         |                            |--- Compare Extracted Data --------|
         |                            |                                   |
         |<-------- Return Status ----|                                   |
```



Note: Generated this using ChatGPT for clear understanding.