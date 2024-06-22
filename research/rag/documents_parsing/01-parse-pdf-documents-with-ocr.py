# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
import os
import argparse
import logging

from pdf2image import convert_from_path
import pytesseract
from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="file path")
    parser.add_argument("--output_path", help="file path")
    args = parser.parse_args()


    # Chemin du fichier PDF
    pdf_path = args.file_path
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    print(f"File Path : {pdf_path}")
    print(f"File Name : {pdf_filename}")

    # Create output folder path
    output_path = args.output_path
    os.makedirs(output_path, exist_ok=True)

    # Convertir le PDF en une liste d'images
    print("Convert pdf to images")
    images = convert_from_path(pdf_path)

    # Enregistrer chaque page comme image
    for i, image in enumerate(images):
        save_image_path = os.path.join(output_path, f"{pdf_filename}_{i}.png")
        print(f"\t- Save Image : {save_image_path}")
        image.save(save_image_path, 'PNG')

        # Ouvrir l'image
        img = Image.open(save_image_path)

        # Utiliser pytesseract pour extraire le texte
        text = pytesseract.image_to_string(img)

        print("\t  File content :")
        print("")
        print(text)
        print("")


if __name__ == "__main__":
    main()
