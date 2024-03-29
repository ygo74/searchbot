# sudo apt-get install poppler-utils
# which pdfinfo
# pip install pdf2image
# pip install  poppler-utils
#
# sudo apt update
# sudo apt install tesseract-ocr
# sudo apt install libtesseract-dev
# tesseract --version


from pdf2image import convert_from_path

# Chemin du fichier PDF
pdf_path = "/mnt/c/Users/Administrator/Documents/fatal picard - Copie.pdf"

# Convertir le PDF en une liste d'images
images = convert_from_path(pdf_path)

# Enregistrer chaque page comme image
for i, image in enumerate(images):
    image.save(f'/mnt/d/devel/github/searchbot/models/output/page_{i}.png', 'PNG')


import pytesseract
from PIL import Image

# Ouvrir l'image
img = Image.open('/mnt/d/devel/github/searchbot/models/output/page_0.png')

# Utiliser pytesseract pour extraire le texte
text = pytesseract.image_to_string(img)

print(text)