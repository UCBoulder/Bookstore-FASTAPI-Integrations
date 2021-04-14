import xml.etree.ElementTree as e


def create_book(course, book):
    """
    Take the book dictionary info and tack it into an XML element
    """

    course_book = e.SubElement(course, "CourseBooks")
    e.SubElement(course_book, "isbn").text = str(book["ISBN"])
    e.SubElement(course_book, "course").text = str(book["DEPT"]) + str(book["COURSE"])
    e.SubElement(course_book, "term").text = str(book["TERM"])
    e.SubElement(course_book, "section").text = str(book["SECTION"])
    e.SubElement(course_book, "title").text = str(book["TITLE"])
    e.SubElement(course_book, "author").text = str(book["AUTHOR"])
    e.SubElement(course_book, "requirement").text = str(book["REQ_OPT"])
    e.SubElement(course_book, "class_nbr").text = str(book["ISIS_COURSE"])
    e.SubElement(course_book, "new_price").text = str(book["NEW_RETAIL"])
    e.SubElement(course_book, "used_price").text = str(book["USED_RETAIL"])
    e.SubElement(course_book, "rental_fee").text = str(book["RENTAL_FEE"])
    e.SubElement(course_book, "used_rental_fee").text = str(book["USED_RENTAL_FEE"])
    e.SubElement(course_book, "session").text = str(book["SESSION_CODE"])
    e.SubElement(course_book, "no_cost").text = str(book["NO_COST_FLAG"])
    e.SubElement(course_book, "low_cost_or_oer").text = str(
        book["LOW_COST_OR_OER_FLAG"]
    )


def create_books(books_json):
    """
    Take the big blop of JSON and convert to XML
    """

    root = e.Element("BigDoc")
    course = e.SubElement(root, "Course")
    for book in books_json:
        create_book(course, book)

    xmlstr = e.tostring(root, encoding="unicode", method="xml")
    return xmlstr
