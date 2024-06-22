# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
import os
import argparse
import logging
import pypdf

def extract_text_from_pdf(file: str) -> str:
    """Extract text from PDF files"""
    text = ""
    with open(file, "rb") as f:
        reader = pypdf.PdfReader(f)
        if reader.is_encrypted:  # Check if the PDF is encrypted
            try:
                reader.decrypt("")
            except pypdf.errors.FileNotDecryptedError as e:
                logging.logger.warning(f"Could not decrypt PDF {file}, {e}")
                return text  # Return empty text if PDF could not be decrypted

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

    if not text.strip():  # Debugging line to check if text is empty
        logging.logger.warning(f"Could not decrypt PDF {file}")

    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="file path")
    args = parser.parse_args()


    # Chemin du fichier PDF
    pdf_path = args.file_path
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    print(f"File Path : {pdf_path}")
    print(f"File Name : {pdf_filename}")


    data = extract_text_from_pdf(args.file_path)
    print(data)


if __name__ == "__main__":
    main()
