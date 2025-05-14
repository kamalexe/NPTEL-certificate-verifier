import os
from pdf2image import convert_from_path

def convert_all_certificates():
    CERTIFICATE_FOLDER_NAME = "./NPTEL-certificates"
    CONVERTED_CERTIFICATE_IMAGE_FOLDER = "./converted-certificate-image"

    os.makedirs(CONVERTED_CERTIFICATE_IMAGE_FOLDER, exist_ok=True)

    ALL_FILE_LIST = os.listdir(CERTIFICATE_FOLDER_NAME)
    ALL_FILE_PATH = []

    for fileName in ALL_FILE_LIST:
        if not fileName.lower().endswith(".pdf"):
            continue
        fullPath = os.path.join(CERTIFICATE_FOLDER_NAME, fileName)
        ALL_FILE_PATH.append(fullPath)

    for file in ALL_FILE_PATH:
        images = convert_from_path(file)
        filePrefixName = os.path.splitext(os.path.basename(file))[0]
        filePrefixPath = os.path.join(CONVERTED_CERTIFICATE_IMAGE_FOLDER, filePrefixName)
        for i in range(len(images)):
            images[i].save(filePrefixPath + '.jpg', 'JPEG')

if __name__ == "__main__":
    convert_all_certificates()
