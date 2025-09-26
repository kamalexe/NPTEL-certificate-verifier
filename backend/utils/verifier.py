import os
import logging
import csv
from PIL import Image
import pytesseract
from pyzbar.pyzbar import decode
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def all_file_paths(folder="./converted-certificate-image"):
    if not os.path.exists(folder):
        logging.warning(f"Folder not found: {folder}")
        return []

    all_files = sorted(os.listdir(folder))
    return [
        os.path.join(folder, file_name)
        for file_name in all_files
        if file_name.lower().endswith((".jpg", ".jpeg"))
    ]

def read_qr_image(qr_image):
    decoded = decode(qr_image)
    if decoded:
        return decoded[0].data.decode()
    return None

def extract_certificate_data(image_path):
    try:
        image = Image.open(image_path)
    except Exception as e:
        logging.error(f"Failed to open image: {image_path} - {e}")
        return {"filename": os.path.basename(image_path), "error": "Could not open image"}

    regions = {
        "qr_code": (3544, 4664, 3973, 5058),
        "name": (1316, 1319, 5795, 1467),
        "course": (1128, 1779, 5884, 2226),
        "marks": (3850, 2273, 4380, 2516),
        "credit": (6500, 4760, 6800, 4900),
        "roll": (580, 4750, 2050, 4920),
        "duration": (3000, 3550, 4200, 3759),
    }

    extracted_data = {"filename": os.path.basename(image_path)}
    for field, box in regions.items():
        try:
            cropped = image.crop(box)
            if field == "qr_code":
                text = read_qr_image(cropped)
            else:
                text = pytesseract.image_to_string(cropped).strip()
            extracted_data[field] = text
        except Exception as e:
            logging.warning(f"OCR failed for {field} in {image_path}: {e}")
            extracted_data[field] = ""

    return extracted_data

def is_valid_nptel_url(url: str) -> bool:
    return url.startswith("https://") and "nptel" in url.lower()

def download_pdf_from_button(response, filename, folder):
    try:
        soup = BeautifulSoup(response.content, 'html5lib')
        certificate_link = soup.find("a", string="Course Certificate")
        if certificate_link and certificate_link.get("href"):
            pdf_path = certificate_link["href"]

            # Normalize the URL
            base_url = "https://archive.nptel.ac.in"
            # Remove any trailing dot from domain if present
            if base_url.endswith('.'):
                base_url = base_url[:-1]

            full_pdf_url = urljoin(base_url, pdf_path)
            print(f"DEBUG {full_pdf_url} ______ {pdf_path} __________")

            pdf_response = requests.get(full_pdf_url)
            if pdf_response.ok:
                os.makedirs(folder, exist_ok=True)
                pdf_file_path = os.path.join(folder, f"{filename}.pdf")
                with open(pdf_file_path, "wb") as f:
                    f.write(pdf_response.content)
                logging.info(f"Certificate downloaded to {pdf_file_path}")
            else:
                logging.warning(f"Failed to download certificate from {full_pdf_url}")
        else:
            logging.warning(f"No 'Course Certificate' link found for {filename}")
    except Exception as e:
        logging.error(f"Error while downloading certificate for {filename}: {e}")
        
def fetch_certificate_url(url):
    try:
        response = requests.get(url)
        return response
    except Exception as e:
        logging.error(f"Unable to fetch the URL {url}: {e}")
        return None

def save_verification_result(result, csv_path="verification_results.csv"):
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["filename", "qr_code", "name", "course", "marks", "credit", "roll", "duration"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(result)
