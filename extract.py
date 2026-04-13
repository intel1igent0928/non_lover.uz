import fitz
import os

pdf_path = "Hero.pdf"
doc = fitz.open(pdf_path)

if not os.path.exists("assets"):
    os.makedirs("assets")

for i in range(len(doc)):
    for img in doc.get_page_images(i):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        with open(f"assets/img_{xref}.{image_ext}", "wb") as f:
            f.write(image_bytes)
        print(f"Extracted image {xref} -> assets/img_{xref}.{image_ext}")
