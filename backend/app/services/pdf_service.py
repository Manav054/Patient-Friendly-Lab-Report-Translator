import pymupdf
from fastapi import HTTPException, UploadFile


def process_file_to_images(file: UploadFile, max_size_mb: int = 5) -> list[bytes]:
    """
    Reads an uploaded file and returns a list of image bytes.
    If it's a PDF, converts each page to an image.
    If it's an image, returns it directly.
    """
    # Read file content
    content = file.file.read()

    # Check size
    size_mb = len(content) / (1024 * 1024)
    if size_mb > max_size_mb:
        raise HTTPException(
            status_code=413, detail=f"File size exceeds {max_size_mb}MB limit."
        )

    images_bytes = []

    if file.filename.lower().endswith(".pdf"):
        try:
            # Open PDF with PyMuPDF
            pdf_document = pymupdf.open(stream=content, filetype="pdf")
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                # Render page to an image (pixmap) at roughly 150-200 DPI
                pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
                images_bytes.append(pix.tobytes("png"))
            pdf_document.close()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing PDF: {e!s}")
    elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        images_bytes.append(content)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload PDF, PNG, or JPG.",
        )

    return images_bytes
