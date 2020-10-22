from collections import OrderedDict


def process_pagination(
    paginated_content: OrderedDict, year: int, volume: int
) -> OrderedDict:
    """
    Handles all the various edge cases due to pagination errors or variability
    in the PDFs (easier and more robust than actually parsing the pagination)
    """
    if (
        1977 < year < 2007
    ):  # cover page is counted as page 1 during most time periods after 1977
        if (
            (year == 1978 and volume < 8)
            or (year == 2004 and volume > 8)
            or (year == 2005 and volume in [5, 6])
            or (year == 2006 and volume > 1)
            or (year == 1986 and volume > 5)
            or (year == 1983 and volume == 3)
            or (year == 1985 and volume in [1, 3, 7, 8, 10, 11])
            or (year == 1979 and volume == 2)
            or (year == 1981 and volume == 4)
            or (year == 1989 and volume == 1)
            or (year == 1994 and volume == 1112)
            or (year == 1999 and volume == 1)
            or (year == 2002 and volume in [4, 8])
            or (year == 2005 and volume in [1, 3, 9, 11, 12])
            or (year == 2011 and volume == 7)
            or (year == 2009 and volume in [1, 5, 7])
        ):
            pass
        elif (year == 1980 and volume == 1) or (year == 1994 and volume == 8):
            paginated_content = OrderedDict(
                (k + 2, v) for k, v in paginated_content.items()
            )
        elif year == 1997 and volume == 9:
            paginated_content = OrderedDict(
                ((k + 1 if k < 15 else k + 2), v) for k, v in paginated_content.items()
            )
            paginated_content[16] = paginated_content[15]
        else:
            paginated_content = OrderedDict(
                (k + 1, v) for k, v in paginated_content.items()
            )
    return paginated_content
