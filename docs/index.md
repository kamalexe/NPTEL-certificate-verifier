# 📜 NPTEL Certificate Verifier

This project automates the process of verifying certificates issued by **NPTEL** (National Programme on Technology Enhanced Learning).

---

## ✅ Overview

The tool compares **submitted certificates** with the **official NPTEL versions** by extracting and validating data through embedded QR codes.

---

## 🔄 Workflow Steps

1. **Prepare Certificate Folder**  
   Place all submitted NPTEL certificates in a folder named `submitted-certificates`.

2. **Extract Submitted Certificate Data**  
   The tool extracts key fields such as:
   - `Name`
   - `Roll Number`
   - `QR Code Data`  
   and stores them in `submitted_certificate_details.csv`.

3. **Download Official Certificates**  
   Using the URL from each QR code, the tool downloads the official version of the certificate from the NPTEL server into a folder called `certificates-from-nptel`.

4. **Extract Official Certificate Data**  
   The downloaded certificates are parsed similarly and saved in `downloaded_certificate_details.csv`.

5. **Compare & Verify**  
   The tool compares both `.csv` files and generates a final report:
   - File: `all_certificates_details.csv`
   - Fields:  
     - `verified` (Yes/No)  
     - `reason` (Mismatch explanation or confirmation)

---

## 📂 Output Files

| File Name                         | Description                             |
|----------------------------------|-----------------------------------------|
| `submitted_certificate_details.csv` | Extracted data from user-submitted PDFs |
| `downloaded_certificate_details.csv` | Extracted data from NPTEL's version     |
| `all_certificates_details.csv`   | Final comparison results                |

---

## 🚀 Benefits

- Saves time by automating certificate checks.
- Detects forged or altered certificates.
- Can be scaled for batch verification.