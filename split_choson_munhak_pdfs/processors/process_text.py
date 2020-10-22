import pdfminer  # type: ignore
from typing import List, Optional
import re
from .decode import decode_cid_strings


def process_text(lt_objs, res: List[Optional[str]] = []) -> List[Optional[str]]:

    for obj in lt_objs:

        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            text: str = obj.get_text().replace("\n", " ")
            if re.search(u"[\u3131-\ucb4c]", text):
                res.append(text)
            elif text.count("(cid:") > 2:
                res.append(decode_cid_strings(text))

        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure) and len(obj._objs) > 1:
            res += process_text(obj._objs, res)

    return res


def process_multipage_text(pages: List) -> str:
    res: List[Optional[str]] = []
    for page in pages:
        page_content: str = " ".join(
            [content for content in process_text(page, []) if content is not None]
        )
        res.append(page_content)
    return "".join([_ for _ in res if res is not None])
