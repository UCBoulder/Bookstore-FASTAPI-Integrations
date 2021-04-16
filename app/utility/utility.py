import xml.etree.ElementTree as e


def flatten_book_record(book):
    """
    Take a book record in gql JSON and flatten it down.
    """

    result = {}
    result["isbn13"] = book["isbn13"]
    result["title"] = book["title"]
    result["author"] = book["author"]
    result["new_price"] = book["new_retail"]
    result["used_price"] = book["used_retail"]
    result["rental_fee"] = book["rental_fee"]
    result["used_rental_fee"] = book["used_rental_fee"]
    result["no_cost_flag"] = book["no_cost_flag"]
    result["low_cost_or_oer_flag"] = book["low_cost_or_oer_flag"]

    if book.get("Section"):
        result["section"] = book["Section"]["code"]
        if book["Section"]["Course_SubjectAreaCourse"]:
            result["course"] = book["Section"]["Course_SubjectAreaCourse"][
                "subjectareacourse_code"
            ]
            result["class_nbr"] = book["Section"]["Course_SubjectAreaCourse"][
                "siscourse_code"
            ]

    if book.get("Session"):
        result["session"] = book["Session"]["code"]
        if book["Session"].get("Term"):
            result["term"] = book["Session"]["Term"]["code"]

    if book.get("ClassBookRequirement"):
        result["requirement"] = book["ClassBookRequirement"]["code"]

    return result


def create_books(books_json):
    """
    Take the big blop of JSON and convert to XML
    """

    root = e.Element("BigDoc")
    course = e.SubElement(root, "Course")
    for book in books_json:
        # get the json back in a flat structure
        flat_book = flatten_book_record(book)

        # Create a "book" element
        course_book = e.SubElement(course, "CourseBooks")

        # for each property of the flat book, create an XML element
        for k, v in flat_book.items():
            e.SubElement(course_book, k).text = v

    xmlstr = e.tostring(root, encoding="unicode", method="xml")
    return xmlstr
