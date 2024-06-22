# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
import os
import argparse
import logging

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="file path")
    args = parser.parse_args()


    # Chemin du fichier PDF
    pdf_path = args.file_path
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    print(f"File Path : {pdf_path}")
    print(f"File Name : {pdf_filename}")

    loader = UnstructuredFileLoader(args.file_path)
    data = loader.load()

    print(data)


if __name__ == "__main__":
    main()
