from pdfminer.pdfparser import PDFParser  # type: ignore
from pdfminer.pdfdocument import PDFDocument  # type: ignore
from pdfminer.pdfpage import PDFPage  # type: ignore
from pdfminer.pdfpage import PDFTextExtractionNotAllowed  # type: ignore
from pdfminer.pdfinterp import PDFResourceManager  # type: ignore
from pdfminer.pdfinterp import PDFPageInterpreter  # type: ignore
from pdfminer.pdfdevice import PDFDevice  # type: ignore
from pdfminer.layout import LAParams  # type: ignore
from pdfminer.converter import PDFPageAggregator  # type: ignore
import os
import re
from processors import process_index, process_multipage_text, process_pagination
from typing import List
from collections import OrderedDict

# input path: where the pdfs are stored
ROOT_PATH: str = "D:\\Backup\\chosonmunhak"
# where the plain text files will be outputed
SAVE_PATH: str = "D:\\Backup\\chosonmunhak\\fulltext"
# extension for the plain text files
TEXT_EXTENSION: str = ".txt"
files: List[str] = [file for file in os.listdir(ROOT_PATH) if file.endswith(".pdf")]
# The list of genres we want to filter for
allowlist: List[str] = ["단편소설", "전국문학축전작품"]


for file in files:
    file_path: str = os.path.join(ROOT_PATH, file)
    issue: str = file.split("_")[0]
    print(issue)
    year_str, volume_str = issue.split("-")
    year: int = int(year_str)
    volume: int = int("".join([c for c in volume_str if c.isdigit()]))
    current_output_path: str = os.path.join(SAVE_PATH, issue)
    os.makedirs(current_output_path, exist_ok=True)

    with open(file_path, mode="rb") as fp:
        parser: PDFParser = PDFParser(fp)
        document: PDFDocument = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        rsrcmgr: PDFResourceManager = PDFResourceManager()
        device: PDFDevice = PDFDevice(rsrcmgr)
        laparams: LAParams = LAParams()
        page_aggregator: PDFPageAggregator = PDFPageAggregator(
            rsrcmgr, laparams=laparams
        )
        interpreter: PDFPageInterpreter = PDFPageInterpreter(rsrcmgr, page_aggregator)

        paginated_content: OrderedDict = OrderedDict()
        for i, page in enumerate(PDFPage.create_pages(document)):

            interpreter.process_page(page)
            layout = page_aggregator.get_result()
            paginated_content[i] = layout

        content_index = process_index(paginated_content)
        paginated_content = process_pagination(paginated_content, year, volume)

        for element_index, index_element in enumerate(content_index.items()):
            article_first_page, article_title = index_element
            if element_index == len(content_index) - 1:
                end_page = len(paginated_content)
            else:
                end_page = list(content_index.keys())[element_index + 1]
            article_pages = [
                paginated_content[j] for j in range(article_first_page, end_page)
            ]
            article_content = process_multipage_text(article_pages)

            # filtering for certain type of articles, the condition can be remove to extract all content
            # in a structured way
            if any(word in article_content[:50] for word in allowlist) and (
                len(article_content) > 7500
            ):
                cleaned_title = re.sub(r"[^\w\d\s]+", "", article_title)
                # replace whitespace & crlf
                cleaned_title = "_".join(
                    cleaned_title.replace("\n", " ").split()
                )
                output_file_name = (
                    str(article_first_page)
                    + "-"
                    + str(end_page)
                    + "_"
                    + cleaned_title
                    + TEXT_EXTENSION
                )
                output_file_path = os.path.join(current_output_path, output_file_name)
                with open(output_file_path, "w", encoding="utf8") as outfp:
                    outfp.write(article_content)
