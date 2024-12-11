import PyPDF2

def extract_text_from_pdf(pdf_path):
    try:
        # Open the PDF file in read-binary mode
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""

            # Iterate through all the pages
            for page in reader.pages:
                text += page.extract_text()

            return text

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
pdf_path = r"backend logic\testpdf.pdf"  # Replace with the path to your PDF file
extracted_text = extract_text_from_pdf(pdf_path)
print("Extracted Text:")
print(extracted_text)
