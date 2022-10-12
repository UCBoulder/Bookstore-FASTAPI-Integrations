# Bookstore REST API

Provides RESTful API interface(s) for UCB Bookstore data. 

## Description

The Books API endpoint is a combination of various data, tools, and work involved with making books data available to consumers. Classification of the data involved with this endpoint is typically considered "public" in nature, thus posing low-risk opportunities for implementation.

### Contacts

- Books data is sourced from the University of Colorado Bookstore. The technical contact there has historically been Jeff Schasny (jeff.schasny@colorado.edu).
- As of the time of this writing, [Leepfrog](https://github.com/UCBoulder/data-docs/blob/main/glossary/Leepfrog.md), a vendor whom supports the class search website for UCB, is the primary consumer of this data. 
- Communication with Leepfrog has typically occurred via correspondence with Joey LaConte (joey.laconte@colorado.edu), (Associate Registrar, Technology, Communications & Reporting). Planning for and making changes to this API endpoint have occurred through Joey and are communicated back to OIT via the same channel.

### Resources

- [UCB Bookstore](https://www.cubookstore.com/) : UCB Bookstore website, which has relationships to the books data involved with this endpoint.
- eds-data1.int.colorado.edu : an unmanaged VM which was created to facilitate the work of the EDS team outside of the OIT Data Lake / Platform project.
- [Podman](https://podman.io/) : open source tool used to run containers on eds-data1, with many similarities to Docker.
- [Github Packages](https://github.com/features/packages) : Image / resource distribution used by FastAPI specification for API for image builds.
- [Hasura](https://hasura.io/) : open source platform used to store and make available the books data to the API endpoint provider.
- [PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL) : open source database used to store underlying data for Hasura.
- [FastAPI](https://fastapi.tiangolo.com/) : Pythonic API framework, similar to Flask, etc.
- [Bookstore-FASTAPI-Integrations](https://github.com/UCBoulder/Bookstore-FASTAPI-Integrations) : repo which implements FastAPI to make books data available.
- [Leepfrog Classes Webpage](https://classes.colorado.edu/) : Leepfrog product which implements data shared from Books API endpoint.

## Data Lifecycle

1. The University of Colorado Bookstore sends source data files (`COURSE.EXPORT.*.txt`) to CU Transfer SFTP under the b01435 user. There may be multiple files sent over.
2. OIT Data Services has a Prefect ETL job [oit-ds-flows-bookstore](https://github.com/UCBoulder/oit-ds-flows-bookstore) which picks up source data files and loads the data into a Postgres database (located on eds-data1.int.colorado.edu) on a daily basis. As of 2022/10/12, there is only a production database. Data not in the current set should be removed (similar to a kill-and-fill approach).
3. The data in the Postgres database is made available via a Hasura GraphQL endpoint. This endpoint may be explored via [web console](https://eds-data1.int.colorado.edu:2443/hasura/console/api-explorer) or via [post](https://eds-data1.int.colorado.edu:2443/hasura/v1/graphql).
4. The Books API is a FastAPI implementation that provides a RESTful interface to retrieve data from the GraphQL intermediary. Books data can be returned as JSON or XML. Leepfrog uses the Books API to pull data (specifically in XML) from the database. 

Note: The API endpoint is public-facing, but restricted to a sub-section of IP addresses that are dedicated to Leepfrog. [GREQ0323759](https://colorado.service-now.com/nav_to.do?uri=%2Fu_gnrl_req.do%3Fsysparm_tiny%3Dc2f5476e1b169590cedbea0dad4bcbe4%26sys_id%3Daf36948a1baebcd0a1ab8407ec4bcb61%26sysparm_record_row%3D1) contains information related to networking. LeepFrog uses endpoints in the format of: `https://128.138.127.230:3443/bookstore/SBookInfo?course1=HIST1011&section1=001&session1=B&term1=2221`. The endpoint is also available publicly at `https://eds-data1.int.colorado.edu:3443/bookstore/SBookInfo?course1=HIST1011&section1=001&session1=B&term1=2221`.

## Deployment

Instructions to deploy the Postgres database and Hasura GraphQL service are contained within the OIT Data Services LastPass instance.

To deploy changes to the FastAPI application:

1. Update the Prefect ETL job [oit-ds-flows-bookstore](https://github.com/UCBoulder/oit-ds-flows-bookstore) as needed.
2. Update the JSON return response in the FastAPI code.
3. Update the XML return response in the FastAPI code, particularly the `make_request()` and `flatten_books` functions in `graphql.py` and `utility.py`, respectively.
4. To test the functionality of the API, you can run the API locally using the instructions contained in the README.md. This will require setting local environment variables in your shell, including a `graphql_key`, `basic_username`, and `basic_password`. These can be set arbitrarily, but specific credentials for these variables are available in LasPass for consistency in prod environments. When running the API on a local server, you can check for data responses in a web browser at `{ip_address}:{port}/ready`, `{ip_address}:{port}/SBookInfo?course1=ACCT3230&is_json=False`, and `{ip_address}:{port}/SBookInfo?course1=ACCT3230&is_json=True`. You can also deploy a local Docker container to test locally as well.
4. When creating a PR to merge changes can be into `main`, there are several automated testing processes that are automatically started via a Github Action. These include linting, security, and output tests which are stored in this repo as well.
5. After confirming that changes have passed the automated tests, are merged to main, and function as expected locally, it is time to update the image stored in the Github container repository. Follow the steps in the [Github docs](https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package) to authenticate to Github, build and tag your new container image with semantic versioning, and push your new image to the Github Container Registry. 
6. After creating a new image in the Github Container Registry, access the eds-data1 server and check running docker/podman containers. Run the `docker run` command stored in LastPass under the Bookstore API. You may need to stop and delete old containers that use the same container name (e.g., "bookstore-api") before recreating the container.
