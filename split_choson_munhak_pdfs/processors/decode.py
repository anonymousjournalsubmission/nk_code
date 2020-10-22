from typing import List, Optional
import re


def decode_cid_strings(input_string: str) -> str:
    """
    (Crudely) handles the CID mapping for a font used in PDFs of the late 1990's
    :param input_string: the encoded string
    :return: the decoded string
    """
    char_ids: List[Optional[str]] = [
        re.sub(r"[^0-9]", "", char)
        for char in input_string.split("(cid:")
        if re.sub(r"[^0-9]", "", char) != ""
    ]
    decode_string: str = ""
    for char_id_str in char_ids:
        if char_id_str is None:
            continue
        char_id: int = int(char_id_str)
        if char_id in range(5879, 17000):
            decode_string += chr(char_id + 38153)
        elif char_id in range(159, 123 + 129):
            decode_string += chr(char_id - 129)
        elif char_id == 379:
            decode_string += "."
        elif char_id in range(381, 391):
            decode_string += chr(char_id - 333)
        else:
            decode_string += " "
    return decode_string
