# Imports
from os import makedirs
import subprocess
import fastapi
from time import strftime

# Application
application = fastapi.FastAPI()

# Helper function to generate a source file
def generate_source_file(source_string: str, file_name: str = "source_"+strftime("%Y-%m-%d_%H-%M-%S")) -> str:
    relative_file_path = "uploads/"
    makedirs(relative_file_path, exist_ok=True)
    relative_file_path+=file_name
    file = open(relative_file_path, "+w")
    file.write(source_string)
    file.close()

    return relative_file_path

# Home Endpoint
@application.get("/")
def greet():
    return "Hello! The code execution endpoint server is up and running."

# Python 3 Source Upload Endpoint
@application.post("/python3")
def execute_py(string: str):
    content = repr(string)[1:-1]      # repr() prevents escape sequence and such unintended string modifications. Slicing to omit quotation marks.
    local_timestamp = strftime("_%Y-%m-%d_%H-%M-%S")
    file_name = "program"+local_timestamp+".py"
    file_path = generate_source_file(content, file_name)

    status = subprocess.run(f"py {file_path}", capture_output=True, timeout=60)

    if status.stderr: return status

    return status.stdout

# Python 3 File Upload Endpoint
@application.post("/python3/upload")
async def execute_py_file(file: fastapi.UploadFile):
    # Reading file content and dumping it to a temporary file
    content = await file.read()
    local_timestamp = strftime("_%Y-%m-%d_%H-%M-%S")
    file_name = "program"+local_timestamp+".py"
    file_path = generate_source_file(content.decode("utf-8"), file_name)

    # Executing the Python program
    status = subprocess.run(f"py {file_path}", capture_output=True, timeout=60)

    return status

# Starting the application server on direct file run
if __name__ == "__main__":
    # Launching the server using uvicorn
    import uvicorn
    # Host = 0.0.0.0 to allow connections from any network interface on the machine through all of the available IPv4 addresses.
    uvicorn.run(application, host="0.0.0.0", port=8000)