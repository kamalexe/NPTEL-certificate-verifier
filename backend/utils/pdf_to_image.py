import os
from pdf2image import convert_from_path

def convert_all_certificates(pdf_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    ALL_FILE_LIST = os.listdir(pdf_folder)
    ALL_FILE_PATH = []

    for fileName in ALL_FILE_LIST:
        if not fileName.lower().endswith(".pdf"):
            continue
        fullPath = os.path.join(pdf_folder, fileName)
        ALL_FILE_PATH.append(fullPath)

    for file in ALL_FILE_PATH:
        images = convert_from_path(file)
        filePrefixName = os.path.splitext(os.path.basename(file))[0]
        filePrefixPath = os.path.join(output_folder, filePrefixName)
        for i in range(len(images)):
            images[i].save(filePrefixPath + '.jpg', 'JPEG')
