---
layout: default
parent: Documents parsing
title: Parsing PDF files
nav_order: 1
has_children: true
---


## Poppler-utils & tesseract

### Prerequisites

``` bash
sudo apt update

sudo apt-get install poppler-utils
sudo apt-get install pdfinfo
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev

which pdfinfo
tesseract --version
```

### Python packages

``` bash
pip install pdf2image poppler-utils
pip install pytesseract
```

### Research sample

File : research/rag/documents_parsing/01-parse-pdf-documents-with-ocr.py

Process is :

- Save file to images (pdfinfo + poppler-utils)
  1 image per page
- Convert image to text thanks to OCR (tesseract-ocr)

``` bash
# Parse a pdf file, need a temporary folder to store image
input_file_path="/tmp/my pdf file.pdf"
output_path="./tmp/outoupt/parsing"

python research/rag/documents_parsing/01-parse-pdf-documents-with-ocr.py --file_path "$input_file_path" --output_path "$output_path"
```

## PyPDF

### Python packages

``` bash
pip install pypdf
```

### Research sample

File : research/rag/documents_parsing/02-parse-pdf-documents-with-pypdf.py

Process is :

- Use PdfReader to read the pdf
- Browse pages and extract text

``` bash
# Parse a pdf file, need a temporary folder to store image
input_file_path="/tmp/my pdf file.pdf"

python research/rag/documents_parsing/02-parse-pdf-documents-with-pypdf.py --file_path "$input_file_path"
```

## Langchain

### Python packages

``` bash
pip install langchain langchain-community
```