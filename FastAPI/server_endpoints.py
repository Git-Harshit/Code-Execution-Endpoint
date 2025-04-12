# Imports
from os import makedirs
import subprocess
import fastapi
from time import strftime

# Application
application = fastapi.FastAPI()

# API Endpoints (looped onto for registration)
register_endpoints = [
    # 'URL' and the execution 'command' are the necessary parameters required here per entry. Ensure that the command/alias used is installed on the server machine.
    { "URL": "bash", "command":"bash", "file_extension":".sh", "timeout":10 },
    { "URL": "python3", "command":"py", "file_extension":".py", "timeout":10 },
]

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

for endpoint in register_endpoints:
    # Source Upload Endpoint
    @application.post("/"+endpoint["URL"])
    def execute_program(string: str):
        content = string
        # Local, temporary file generation
        local_timestamp = strftime("_%Y-%m-%d_%H-%M-%S")
        file_name = "program"+local_timestamp
        if "file_extension" in endpoint: file_name += endpoint["file_extension"]
        file_path = generate_source_file(content, file_name)

        # Execution
        status = subprocess.run(f"{endpoint['command']} \"{file_path}\"", capture_output=True, timeout=endpoint["timeout"] if "timeout" in endpoint else 60)

        return status

    # File Upload Endpoint
    @application.post("/%s/upload" %endpoint["URL"])
    async def execute_program_file(file: fastapi.UploadFile):
        # Reading file content
        content = await file.read()

        # Executing the program
        return execute_program(content.decode("utf-8"))

# Starting the application server on direct file run
if __name__ == "__main__":
    # Launching the server using uvicorn
    import uvicorn
    # Host = 0.0.0.0 to allow connections from any network interface on the machine through all of the available IPv4 addresses.
    uvicorn.run(application, host="0.0.0.0", port=8000)