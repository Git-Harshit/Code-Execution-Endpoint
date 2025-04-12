# Code Execution Endpoint

A Back-end server to run a source code on the server machine.

## Setup

### One-time 

1. Install Python v3 from http://www.python.org/downloads.
1. (Recommended, but not necessary) Create a Virtual Environment with Python to separately use the module dependencies for this application.

    i.  Run `py -m venv <Environment_Name>` to create a separate Environment that is stored as a folder where the command is invoked.

    ii. Launch the environment using the `<Environment_Name>/Scripts/activate` script call.

2. Install [FastAPI](https://fastapi.tiangolo.com/) using `pip install fastapi[standard]` or a static server such as Uvicorn with `pip install uvicorn[standard]`. The \[standard] variant includes the standard package with the recommended module items to setup the server.

3. In order to use the endpoints, language-specific entries in the register_endpoints List under the server_endpoints.py file can be updated to list the supported languages. Make sure to have the provided commands installed on the machine where the server is to be launched.

### Launching the server

1. Launch the [server_endpoints.py](./server_endpoints.py) script using `fastapi dev server_endpoints.py` for a development server or `fastapi run server_endpoints.py` to start the server.
    - Note that the `fastapi` command is only available when the "fastapi[standard]" package is installed using pip and not when the "fastapi" package is installed without the standard recommendations.
    - Alternatively, a static server can also be started using `uvicorn server_endpoints:application` or simply calling `python3 server_endpoints.py`.

## Server Endpoints

All of the below registered endpoints support POST request.

1. /bash           - To run Bourne again Shell (Bash) Program by using the source code.
2. /bash/upload    - To run Bourne again Shell (Bash) Program by uploading the file with the source code.
3. /python3        - To run Python 3 Program by pushing the source code.
4. /python3/upload - To run Python 3 Program by uploading the file with the source code.

Note: To access Swagger UI from /docs, a one-time Internet connection has been noted as required for Swagger to load its UI files.