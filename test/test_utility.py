from __future__ import absolute_import

import json
import logging
import os
import sys
import xml.etree.ElementTree as e

from app.utility.utility import create_books, flatten_book_record, flatten_book_records

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logger = logging.getLogger(__name__)


def test_utility_create_books():
    with open("test/graphql_output1.json") as json_file:
        data = json.load(json_file)

    flattened_books = flatten_book_records(data["data"]["books_Book"])
    result = create_books(flattened_books)

    # TODO check XML against XML
    assert result, result


def test_flatten_book_records():
    with open("test/graphql_output1.json") as json_file:
        data = json.load(json_file)
    with open("test/flattened_output1.json") as json_file:
        expected = json.load(json_file)

    result = flatten_book_records(data["data"]["books_Book"])

    assert result == expected, "JSONs don't match."


def test_flatten_book_record():
    with open("test/graphql_output1.json") as json_file:
        data = json.load(json_file)
    with open("test/flattened_output1.json") as json_file:
        expected = json.load(json_file)

    result = flatten_book_record(data["data"]["books_Book"][0])

    assert result == expected["books"][0], "JSONs don't match."
