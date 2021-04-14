from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Bookstore GraphQL REST Shim"
    admin_email: str = (
        "no-reply@colorado.edu"  # should override this with something better
    )
    graphql_url: str = "https://eds-data1.int.colorado.edu:2443/hasura/v1/graphql"
    graphql_key: str
    basic_username: str
    basic_password: str


settings = Settings()