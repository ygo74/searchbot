from dotenv import load_dotenv
import os
import argparse
import logging
import pypdf

from langchain_community.document_loaders import UnstructuredFileLoader

try:
    from unstructured.partition.auto import partition

    HAS_UNSTRUCTURED = True
except ImportError:
    HAS_UNSTRUCTURED = False

TEXT_FORMATS = [
    "txt",
    "json",
    "csv",
    "tsv",
    "md",
    "html",
    "htm",
    "rtf",
    "rst",
    "jsonl",
    "log",
    "xml",
    "yaml",
    "yml",
    "pdf",
]
UNSTRUCTURED_FORMATS = [
    "doc",
    "docx",
    "epub",
    "msg",
    "odt",
    "org",
    "pdf",
    "ppt",
    "pptx",
    "rtf",
    "rst",
    "xlsx",
]  # These formats will be parsed by the 'unstructured' library, if installed.

if HAS_UNSTRUCTURED:
    TEXT_FORMATS += UNSTRUCTURED_FORMATS
    TEXT_FORMATS = list(set(TEXT_FORMATS))

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



    # Parse with UnstructuredFileLoader
    # https://unstructured-io.github.io/unstructured/integrations.html#integration-with-langchain
    print("".ljust(80,"="))
    print(f"Parse file , {args.file_path}!")
    print("".ljust(80,"="))

    _, file_extension = os.path.splitext(args.file_path)
    file_extension = file_extension.lower()

    if file_extension == ".pdf":
        data = extract_text_from_pdf(args.file_path)
    else:
        loader = UnstructuredFileLoader(args.file_path)
        data = loader.load()

    print(data)

if __name__ == "__main__":
    main()
