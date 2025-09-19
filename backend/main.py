import os
import csv
import logging
from dotenv import load_dotenv
from utils import pdf_to_image, data_extractor, verifier

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load path configs from .env
SUBMITTED_CERT_FOLDER = os.getenv("SUBMITTED_CERT_FOLDER")
DOWNLOADED_CERT_FOLDER = os.getenv("DOWNLOADED_CERT_FOLDER")
CONVERTED_IMAGE_FOLDER = os.getenv("CONVERTED_IMAGE_FOLDER")
SUBMITTED_CERT_EXTRACTED_RESULT = os.getenv("SUBMITTED_CERT_EXTRACTED_RESULT")
DOWNLOADED_CERT_EXTRACTED_RESULT = os.getenv("DOWNLOADED_CERT_EXTRACTED_RESULT")
FINAL_RESULT = os.getenv("FINAL_RESULT")

def main():
    # Construct full image folder path
    submitted_image_folder = os.path.join(SUBMITTED_CERT_FOLDER, CONVERTED_IMAGE_FOLDER)
    os.makedirs(submitted_image_folder, exist_ok=True)

    # Step 1: Convert PDF to image
    pdf_to_image.convert_all_certificates(pdf_folder=SUBMITTED_CERT_FOLDER, output_folder=submitted_image_folder)

    # Step 2: Read all certificate images from the folder
    image_paths = data_extractor.all_file_paths(submitted_image_folder)

    # Step 3: Process each image
    for image_path in image_paths:
        logging.info(f"Processing: {image_path}")

        # Extract certificate fields
        result = verifier.extract_certificate_data(image_path)

        # Debug: show extracted QR code
        print(f"[KAMAL] Extracted QR code for {result['filename']}: {result.get('qr_code', '')}")

        # Save extracted details
        verifier.save_verification_result(result, csv_path=SUBMITTED_CERT_EXTRACTED_RESULT)

        # Step 4: Handle QR and download
        qr_url = result.get("qr_code", "")
        if verifier.is_valid_nptel_url(qr_url):
            response = verifier.fetch_certificate_url(qr_url)
            print(f"[KAMAL] Fetched download response for {result['filename']}: {response}")
            if response:
                verifier.download_pdf_from_button(response, result["filename"].split('.')[0], folder=DOWNLOADED_CERT_FOLDER)
        else:
            logging.warning(f"Invalid or missing QR URL for {result['filename']}")

    # Construct full image folder path
    downloaded_image_folder = os.path.join(DOWNLOADED_CERT_FOLDER, CONVERTED_IMAGE_FOLDER)
    os.makedirs(downloaded_image_folder, exist_ok=True)

    # Step 1: Convert PDF to image
    pdf_to_image.convert_all_certificates(pdf_folder=DOWNLOADED_CERT_FOLDER, output_folder=downloaded_image_folder)

    # Step 2: Read all certificate images from the folder
    downloaded_image_paths = data_extractor.all_file_paths(downloaded_image_folder)

    # Step 3: Process each image
    for image_path in downloaded_image_paths:
        logging.info(f"Processing: {image_path}")

        # Extract certificate fields
        result = verifier.extract_certificate_data(image_path)

        # Debug: show extracted data
        print(f"[KAMAL] Extracted data for {result['filename']}: {result}")

        # Save extracted details
        verifier.save_verification_result(result, csv_path=DOWNLOADED_CERT_EXTRACTED_RESULT)



def compare_both_cert_details():
    # Read submitted certificate extracted results
    submitted_data = {}
    with open(SUBMITTED_CERT_EXTRACTED_RESULT, newline='', encoding='utf-8') as sub_file:
        reader = csv.DictReader(sub_file)
        for row in reader:
            submitted_data[row['filename']] = row
    print(f"[KAMAL CHECK] Loaded submitted data: {submitted_data}")

    # Read downloaded certificate extracted results
    downloaded_data = {}
    with open(DOWNLOADED_CERT_EXTRACTED_RESULT, newline='', encoding='utf-8') as down_file:
        reader = csv.DictReader(down_file)
        for row in reader:
            downloaded_data[row['filename']] = row
    print(f"[KAMAL CHECK] Loaded downloaded data: {downloaded_data}")

    # Prepare result rows
    result_rows = []
    # Fieldnames: use the submitted fields + verified + reason
    submitted_fieldnames = list(next(iter(submitted_data.values())).keys()) if submitted_data else []
    fieldnames = submitted_fieldnames + ['verified', 'reason']

    # For each submitted certificate, compare with downloaded
    for filename, submitted_row in submitted_data.items():
        downloaded_row = downloaded_data.get(filename)
        row_result = submitted_row.copy()
        if not downloaded_row:
            row_result['verified'] = False
            row_result['reason'] = "Downloaded certificate not found"
            print(f"[KAMAL CHECK] {filename}: Downloaded certificate not found")
        else:
            mismatches = []
            for key in ['name', 'course', 'marks', 'roll', 'duration', 'credit']:
                if submitted_row.get(key, '').strip() != downloaded_row.get(key, '').strip():
                    mismatches.append(key)
            if mismatches:
                row_result['verified'] = False
                row_result['reason'] = f"Mismatched fields: {', '.join(mismatches)}"
                print(f"[KAMAL CHECK] {filename}: Mismatched fields: {mismatches}")
            else:
                row_result['verified'] = True
                row_result['reason'] = "All fields matched"
                print(f"[KAMAL CHECK] {filename}: All fields matched")
        result_rows.append(row_result)

    # Write the final result CSV
    with open(FINAL_RESULT, mode='w', newline='', encoding='utf-8') as result_file:
        writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result_rows)
    print(f"[KAMAL CHECK] Final verification CSV written to: {FINAL_RESULT}")

if __name__ == "__main__":
    main()
    compare_both_cert_details()
