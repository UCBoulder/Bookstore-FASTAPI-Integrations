""" configuration for api """
from pydantic import BaseSettings

# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """settings for pydantic"""

    app_name: str = "Bookstore GraphQL REST Shim"
    admin_email: str = (
        "no-reply@colorado.edu"  # should override this with something better
    )
    graphql_url: str
    graphql_key: str
    basic_username: str
    basic_password: str
