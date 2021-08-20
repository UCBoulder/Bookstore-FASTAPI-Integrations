""" various utility functions for bookstore api """
import logging
import xml.etree.ElementTree as e  # nosec
from box import Box

logger = logging.getLogger(__name__)


def flatten_book_record(book):
    """
    Take a book record in gql JSON and flatten it down.

    Returns a dict of a "book"
    """

    book = Box(book)

    result = Box()

    result.isbn13 = book.isbn13
    result.title = book.title
    result.author = book.author
    result.new_price = book.new_retail
    result.used_price = book.used_retail
    result.rental_fee = book.rental_fee
    result.used_rental_fee = book.used_rental_fee
    result.no_cost_flag = book.no_cost_flag
    result.low_cost_flag = book.low_cost_flag
    result.no_cost_flag = book.no_cost_flag
    result.oer_flag = book.oer_flag
    result.section = book.Section.code
    result.course = book.Section.Course_SubjectAreaCourse.subjectareacourse_code
    result.class_nbr = book.Section.Course_SubjectAreaCourse.siscourse_code
    result.session = book.Session.code
    result.term = book.Session.Term.code
    result.requirement = book.ClassBookRequirement.code

    return result.to_dict()


def flatten_book_records(books):
    """
    Take the big blop of JSON and convert to a list of json flat "books"
    """

    response = []
    for book in books:
        # get the json back in a flat structure
        flat_book = flatten_book_record(book)

        response.append(flat_book)

    return {"books": response}


def create_books(books_json):
    """
    Take the flattened JSON and convert to XML
    """

    root = e.Element("BigDoc")
    course = e.SubElement(root, "Course")

    # get the list from the 'books' key
    for book in books_json["books"]:

        # Create a "book" element
        course_book = e.SubElement(course, "CourseBooks")

        # for each property of the flat book, create an XML element
        for key, val in book.items():
            e.SubElement(course_book, key).text = val

    xmlstr = e.tostring(root, encoding="unicode", method="xml")
    return xmlstr
