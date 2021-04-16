from typing import List, Optional
import requests, logging, json


logger = logging.getLogger(__name__)


def make_request(
    url: str,
    api_key: str,
    courses: List[str],
    sessions: List[str],
    terms: List[str],
    sections: List[str],
):
    logger.debug(
        f"Request vars: courses:{courses};sessions:{sessions};sections:{sections};terms:{terms}"
    )

    variables = {}

    # process parameters into variable dict
    if courses and len(courses) > 0:
        variables["_courses"] = courses
    if sessions and len(sessions) > 0:
        variables["_sessions"] = sessions
    if terms and len(terms) > 0:
        variables["_terms"] = terms
    if sections and len(sections) > 0:
        variables["_sections"] = sections

    logger.debug(f"Graphql vars: {variables}")

    query = """
query MyQuery($_courses:[String!], $_terms: [String!], $_sessions: [String!], $_sections: [String!]) {
  books_Book(where: {Session: {code: {_in: $_sessions}, Term: {code: {_in: $_terms}}}, Section: {code: {_in: $_sections}, Course_SubjectAreaCourse: {subjectareacourse_code: {_in: $_courses}}}}) {
    author
    isbn13
    new_retail
    no_cost_flag
    title
    used_rental_fee
    used_retail
    rental_fee
    Session {
      code
      Term {
        code
      }
    }
    Section {
      code
      Course_SubjectAreaCourse {
        siscourse_code
        sisoffer_code
        subjectareacourse_code
      }
    }
    low_cost_or_oer_flag
    ClassBookRequirement {
      code
    }
  }
}
    """

    # TODO Move to JWT
    headers = {
        "X-hasura-admin-secret": api_key,
        "content-type": "application/json",
    }

    datadict = dict({"query": query})
    if len(variables) > 0:
        datadict["variables"] = variables

    try:
        r = requests.post(url, json=datadict, headers=headers)
        if r.status_code == 200:
            return r.status_code, r.json()
        else:
            return r.status_code, None
    except requests.exceptions.ConnectionError as e:
        # Most common if the graphql server is down.
        logger.error(str(e))
        gql_status_code = 424
        gql_status_text = str(e)
    except Exception as e:
        logger.error(str(e))
        gql_status_code = 500
        gql_status_text = str(e)

    return gql_status_code, gql_status_text
