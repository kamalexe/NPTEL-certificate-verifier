# ✅ Project Workflow
##	1.	User Uploads Folder:
	•	Use a web interface (React, HTML/JS, or any frontend framework).
	•	Accept folder input or multiple PDF files.
##	2.	PDF to Image Conversion:
	•	Use a backend (Node.js with pdf2img or Python with pdf2image) to convert each PDF to images (usually PNG/JPG).
##	3.	Image Cropping for Data Extraction:
	•	Predefine bounding box coordinates for:
	•	Name
	•	Course Title
	•	Score/Grade
	•	QR Code
##	4.	QR Code Detection and Reading:
	•	Use OpenCV + pyzbar (Python) or JS-based libraries like jsQR (for client-side).
	•	Extract URL from the QR code.
##	5.	Certificate Download from QR Code URL:
	•	Fetch the certificate using the extracted URL (likely a PDF).
##	6.	Repeat Step 2 & 3 for Downloaded Certificate:
	•	Convert, crop, and extract text data from the downloaded certificate.
##	7.	Compare Original vs Downloaded Data:
	•	Ensure all key fields (name, course, score) match.
	•	If they match → ✅ Verified.


# 🔧 Recommended Tech Stack
	•	Frontend: React.js or basic HTML/CSS/JS
	•	Backend: Python (FastAPI/Flask) or Node.js
	•	Libraries:
	•	pdf2image (Python) or pdf-lib (Node.js)
	•	Pillow, OpenCV, pyzbar (for image processing)
	•	PyMuPDF or pdfplumber (for text extraction as a backup)
	•	requests (for downloading from QR link)
    

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