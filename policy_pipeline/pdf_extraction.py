from pathlib import Path
import PyPDF2


def extract_text(pdf_path: Path) -> str:
    """Extract text from a PDF file.

    Args:
        pdf_path (Path): Path to the PDF file

    Returns:
        str: Extracted text
    """

    # Open the PDF file
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        # Iterate through each page and extract text
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text()

    return text
