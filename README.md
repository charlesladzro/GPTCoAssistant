# GPTCoAssistant

## Overview
**GPTCoAssistant** provides a secure and extensible environment for enabling GPT (from OpenAI's ChatGPT platform) to interact with code and files in a specified directory (`START_DIR`).

---

## Features

1. **File and Directory Operations**
   - GPT can create, read, update, and delete files or folders within the `START_DIR`.

2. **Git Integration**
   - Automatically stages and commits changes made through API interactions.
   - Adds commit SHA to responses for traceability.

3. **Secure API**
   - Offers a Flask-based API for handling requests.
   - Protects endpoints with API key authentication.

4. **Scoped Interactions**
   - Limits all operations to the specified `START_DIR` for safety and control.

5. **OpenAPI Documentation**
   - Serves OpenAPI specifications at:
     - `/openapi.json` (JSON format)
     - `/openapi.yaml` (YAML format).

6. **Logging**
   - Logs all incoming requests and outgoing responses for debugging and monitoring.

---

## Setup Instructions

### Prerequisites

1. **Download ngrok**:
   - Go to [ngrok's official website](https://ngrok.com/download).
   - Download the `ngrok.exe` file for your platform (Windows).
   - Place the downloaded `ngrok.exe` file in the `ngrok` folder in this project.

2. **Install Git**:
   - Download and install Git from [git-scm.com](https://git-scm.com/).
   - Ensure Git is added to your system's PATH.

3. **Install Python dependencies**:
   - Use `setup.sh` (instructions below) to install required Python packages.

---

### Running the Application

1. **Execute `setup.sh`**:
   - Open **Git Bash** or **Cygwin** and navigate to the project folder.
   - Run the setup script:
     ```bash
     ./setup.sh
     ```
   - During execution, you will be prompted to specify the `START_DIR`:
     - This is the directory where all modifications made via the API will take place.
     - Ensure you select a directory with appropriate permissions and structure.
   - The script will also:
     - Install Python dependencies from `requirements.txt`.
     - Initialize Git for version control if not already set up.

2. **Run `run_app.bat`**:
   - Double-click `run_app.bat` or execute it from a terminal.
   - This script will:
     - Start the Flask server on `localhost:5000`.
     - Launch `ngrok` to create a public URL for accessing the server.

3. **Access the Application**:
   - After running `run_app.bat`, you will see two URLs:
     - **Localhost**: `http://localhost:5000` for local access.
     - **Ngrok URL**: A public URL (e.g., `https://<random-id>.ngrok.io`) for external access.

---

## Important Information

- **START_DIR**:
  - All file and folder operations performed via the API will take place within the directory specified as `START_DIR` during `setup.sh` execution.
  - This ensures that operations are isolated to a controlled environment.
  - The `START_DIR` can be changed later by modifying the `config.ini` file.

---

## Folder Structure

- **`app.py`**: Main application script.
- **`auth.py`**: Handles API key authentication.
- **`config.py`**: Manages configuration from `config.ini`.
- **`func_utils.py`**: Provides utility functions for Git operations.
- **`actions/`**: Contains dynamically registered API scripts.
- **`utils/`**: Contains logging middleware.
- **`logs/`**: Stores request and response logs.
- **`ngrok/`**: Contains `ngrok.exe` for public URL generation.

---

## Requirements
- Python 3.8+
- Flask
- Git
- ngrok

---

## Contributing
Feel free to contribute by adding scripts to the `actions` folder. Ensure that scripts:
- Define a function named `<filename>_action`.
- Follow Flask route conventions.

---

## License
This project is licensed under the MIT License.
