import random, requests, string, time, logging, secrets
from typing import List, Optional
from fastapi import FastAPI, Request, Response, status, HTTPException, Depends
from fastapi.params import Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseSettings

# app-specific modules and packages
import app.graphql.graphql as gql
from app.utility.utility import create_books
from . import config

logging.config.fileConfig("app/logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()
security = HTTPBasic()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Tidy bit of logging assist to show how long each call takes.
    Found here: https://philstories.medium.com/fastapi-logging-f6237b84ea64
    """
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/SBookInfo")
def read_item(
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security),
    course1: Optional[List[str]] = Query(None),
    session1: Optional[List[str]] = Query(None),
    section1: Optional[List[str]] = Query(None),
    term1: Optional[List[str]] = Query(None),
    dept1: Optional[List[str]] = Query(None),
    is_json: bool = False,
):
    """
    Rebuilding under an existing service.

    Basic user/password auth.

    Note the duplicate session1 queries args:
    e.g., https://ws.colorado.edu/BookStore/SBookInfo?course1=ACCT3230&session1=001&session1=B&term1=2217
    """

    correct_username = secrets.compare_digest(
        credentials.username, config.settings.basic_username
    )
    correct_password = secrets.compare_digest(
        credentials.password, config.settings.basic_password
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Call the GraphQL service to fetch data
    gql_status, results = gql.make_request(
        url=config.settings.graphql_url,
        api_key=config.settings.graphql_key,
        courses=course1,
        sections=section1,
        terms=term1,
        sessions=session1,
    )

    # return or replace the status_code with what's received from the make_request()
    response.status_code = gql_status

    if gql_status == 200 and results.get("data"):
        if is_json:
            return results["data"]
        else:
            # convert to XML and return it.
            books_xml = create_books(results["data"]["books_Book"])
            return Response(content=books_xml, media_type="application/xml")

    # TODO obscure internal details of the failing
    return {"An internal error has occurred."}
