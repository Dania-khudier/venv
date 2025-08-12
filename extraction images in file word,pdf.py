import os
import zipfile
import fitz  # PyMuPDF
from PIL import Image
import io

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def extract_images_from_docx(docx_path, output_dir):
    ensure_dir(output_dir)
    with zipfile.ZipFile(docx_path, 'r') as docx_zip:
        media_files = [f for f in docx_zip.namelist() if f.startswith('word/media/')]
        for media_file in media_files:
            filename = os.path.basename(media_file)
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'wb') as f:
                f.write(docx_zip.read(media_file))
            print(f"[Word] Extracted: {output_path}")

def extract_images_from_pdf(pdf_path, output_dir):
    ensure_dir(output_dir)
    doc = fitz.open(pdf_path)
    img_count = 0
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            img_count += 1
            image = Image.open(io.BytesIO(image_bytes))
            image_filename = os.path.join(output_dir, f"page{page_num+1}_img{img_index}.{image_ext}")
            image.save(image_filename)
            print(f"[PDF] Extracted: {image_filename}")

def extract_images(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    base_output_dir = "extracted_images"
    if ext == '.docx':
        extract_images_from_docx(file_path, os.path.join(base_output_dir, "word"))
    elif ext == '.pdf':
        extract_images_from_pdf(file_path, os.path.join(base_output_dir, "pdf"))
    else:
        print(f"Unsupported file type: {ext}")


extract_images("Product Requirements Document.docx")
extract_images("Biology.pdf")