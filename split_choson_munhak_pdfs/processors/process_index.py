import re
from collections import OrderedDict
from typing import Dict, List
from pdfminer.layout import LTTextBoxHorizontal  # type: ignore
from .decode import decode_cid_strings


def decode_index_text(input_string: str) -> str:
    """
    Handles some encoding and formating issues
    :param input_string: the string with unknown encoding
    :return: the properly decoded string
    """
    decoded_output: str = decode_cid_strings(input_string)
    clean_decoded_output: str = re.sub(r"(\.+)(\d+)\s?\n", r"\1 \2 \n", decoded_output)
    return clean_decoded_output


def process_index(paginated_content: Dict) -> OrderedDict:
    index_parsing_regex: str = r"\.{2,}\s?\d+\s"
    title_and_pages: OrderedDict = OrderedDict()
    index_found: bool = False
    for page, page_content in paginated_content.items():

        full_page_content: str = "".join(
            [
                element.get_text()
                for element in page_content
                if type(element) == LTTextBoxHorizontal
            ]
        ).replace("·", ".").replace("􀅻", ".")
        if full_page_content.count("(cid:") > 10:
            full_page_content = decode_index_text(full_page_content)

        is_index_page = re.findall(index_parsing_regex, full_page_content)
        if not is_index_page:
            continue  # skip cover
        if not is_index_page and index_found:
            break
        article_title: str = ""
        first_line_parsed: bool = False
        filtered_page_captions: List[str] = []
        for element in page_content:
            if type(element) != LTTextBoxHorizontal:
                continue
            elif element.get_text().count("\n") > 1:
                filtered_page_captions += element.get_text().split("\n")
            else:
                filtered_page_captions.append(element.get_text())
        filtered_page_captions = [
            caption.replace("·", ".").replace("􀅻", ".")
            for caption in filtered_page_captions
        ]
        for caption in filtered_page_captions:
            if caption.count("(cid:") > 2:
                caption = decode_index_text(caption)
            if not re.findall(index_parsing_regex, caption):
                if first_line_parsed and (not re.findall(r"\d+\s", caption)):
                    article_title += caption  # multiline titles
                    continue
                elif first_line_parsed and re.findall(r"\w+\s+\d+", caption):
                    caption = re.sub(
                        r"(\w+)\s+(\d+)", r"\1 ... \2", caption
                    )  # handle long titles with no periods
                else:
                    continue
            page_number: int = int(re.findall(r"\s?\d+\s", caption)[-1].strip())
            article_title += caption.split("..")[0].strip()
            title_and_pages[page_number] = article_title
            article_title = ""
            first_line_parsed = True
        index_found = True

    return title_and_pages
