import PyPDF3 as pdf
import re
from pathlib import Path


def extract_pdf_pages(input_file, output_file="", start_page=1, end_page=0):
    """
    Extracts specific pages from a PDF file and saves them to a new PDF file.

    Parameters:
    input_file (str): Path to the input PDF file.
    output_file (str): Path to the output PDF file.
    start_page (int): Page number to start extraction (1-indexed).
    end_page (int): Page number to end extraction (inclusive).

    Returns:
    bool: True if successful, False otherwise.
    """

    if output_file == "":
        output_file = input_file.split(".")[0] + "_extracted.pdf"

    # Validate page range
    if start_page < 1 or (end_page != 0 and end_page < start_page):
        print("Invalid page range.")
        return False

    try:
        # Create a PDF reader object
        with open(input_file, "rb") as file:
            pdf_reader = pdf.PdfFileReader(file)

            if end_page == 0:
                end_page = pdf_reader.numPages

            # Validate the page range
            if end_page > pdf_reader.numPages:
                print("Invalid end page, the PDF contains only", pdf_reader.numPages, "pages.")
                return False

            # Create a PDF writer object
            pdf_writer = pdf.PdfFileWriter()

            # Add selected pages to the writer
            for page_num in range(start_page - 1, end_page):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)

            # Write the extracted pages to a new file
            with open(output_file, "wb") as output:
                pdf_writer.write(output)

            print("Pages extracted successfully.")
            return True

    except Exception as e:
        print("An error occurred:", str(e))
        return False


def rename_pdfs(path, naming_pattern, num_groups=1):
    # Get the list of files in the directory
    root = Path(path)
    # Loop through the files
    for element in root.iterdir():
        # Check if the file is a directory
        if element.suffix == '.pdf':
            rename_pdf(element, pattern=naming_pattern, num_groups=num_groups)


def rename_pdf(file_path, pattern, num_groups=1):
    # The regex pattern and the groups to be used in the file name
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = pdf.PdfFileReader(pdf_file)
        first_page = pdf_reader.getPage(0)
        text = first_page.extractText()

    # Only the first match is considered
    match = re.search(pattern, text)
    new_name = ''
    for group in range(1, num_groups + 1):
        new_name += match.group(group) + '_'
    new_name = new_name[:-1] + '.pdf'
    file_path.rename(file_path.with_name(new_name))


if __name__ == "__main__":
    # Example usage:
    input_pdf_file = "input.pdf"  # Replace with the path to your input PDF file
    output_pdf_file = "output.pdf"  # Replace with the path where you want to save the extracted pages

    # Extract pages 3 to 5 from the input PDF and save them to the output PDF
    extract_pdf_pages(input_pdf_file, output_pdf_file, 3, 5)