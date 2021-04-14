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
    depts: List[str],
):
    logger.debug(
        f"Request vars: courses:{courses};sessions:{sessions};sections:{sections};terms:{terms};depts:{depts}"
    )

    variables = {}

    # process parameters into variable dict
    # TODO fix the database to present a proper course
    # if courses and len(courses) > 0:
    #    variables["_courses"] = courses
    if sessions and len(sessions) > 0:
        variables["_sessions"] = sessions
    if terms and len(terms) > 0:
        variables["_terms"] = terms
    if sections and len(sections) > 0:
        variables["_sections"] = sections
    if depts and len(depts) > 0:
        variables["_depts"] = depts

    logger.debug(f"Graphql vars: {variables}")

    query = """
query MyQuery($_sections: [String!], $_terms: [String!], $_depts: [String!], $_sessions: [String!]) {
  FLAT_COURSE_BOOKS(where: {DEPT: {_in: $_depts}, TERM: {_in: $_terms}, SECTION: {_in: $_sections}, SESSION_CODE: {_in: $_sessions}}, order_by: {DEPT: asc, COURSE: asc}) {
    ISBN
    COURSE
    TERM
    TITLE
    AUTHOR
    REQ_OPT
    NEW_RETAIL
    USED_RETAIL
    RENTAL_FEE
    USED_RENTAL_FEE
    LOW_COST_OR_OER_FLAG
    NO_COST_FLAG
    ISIS_COURSE
    SESSION_CODE
    DEPT
    SECTION
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
