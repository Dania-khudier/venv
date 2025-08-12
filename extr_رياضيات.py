import os
import fitz  
from PIL import Image
from PIL import ImageShow
import io


os.chdir(os.path.dirname(os.path.abspath(__file__)))
def extract_text(pdf_path, output_txt_path):

    """
    Extracts all text from the PDF file, saves it to a text file,
    and prints the text to the console.
    Supports Arabic, English, numbers, and dates.
    """
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")  # Extract plain text
        full_text += f"\n--- Page {page_num + 1} ---\n{text}\n"
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    doc.close()
    print(f"Text extracted and saved to: {output_txt_path}\n")
    print("--- Extracted Text Preview ---")
    print(full_text)

def extract_images(pdf_path, output_folder, zoom=3):
    """
    Extracts images from the PDF file with increased resolution and size,
    saves images as PNG files,
    and opens each image after saving.
    """
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_count = 0
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))

            # Resize image by zoom factor
            width, height = image.size
            new_size = (width * zoom, height * zoom)
            image = image.resize(new_size, Image.LANCZOS)

            # Convert CMYK images to RGB to avoid saving errors
            if image.mode == "CMYK":
                image = image.convert("RGB")

            image_count += 1
            image_path = os.path.join(output_folder, f"page{page_num + 1}_img{img_index + 1}.png")
            image.save(image_path, "PNG", quality=95)

            # ImageShow.show(image)  # هذا السطر معلق لمنع فتح الصور تلقائيًا

    doc.close()
    print(f"Extracted {image_count} images saved to folder: {output_folder}")

def process_pdf(pdf_path):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    text_output = f"{base_name}_extracted_text.txt"
    images_output = f"{base_name}_extracted_images"

    extract_text(pdf_path, text_output)
    extract_images(pdf_path, images_output, zoom=3)

if __name__ == "__main__":
    pdf_filename = "رياضيات علمي.pdf"
    process_pdf(pdf_filename)
    