# **GPTCoAssistant**

## **Overview**
GPTCoAssistant provides a secure and extensible environment for enabling GPT (from OpenAI's ChatGPT platform) to interact with code and files in a specified directory (`START_DIR`).

---

## **Features**

### **File and Directory Operations**
- GPT can create, read, update, and delete files or folders within the `START_DIR`.

### **Git Integration**
- Automatically stages and commits changes made through API interactions.
- Adds commit SHA to responses for traceability.

### **Secure API**
- Offers a Flask-based API for handling requests.
- Protects endpoints with API key authentication.

### **Scoped Interactions**
- Limits all operations to the specified `START_DIR` for safety and control.

### **OpenAPI Documentation**
- Serves OpenAPI specifications at:
  - `/openapi.json` (JSON format)
  - `/openapi.yaml` (YAML format).

### **Logging**
- Logs all incoming requests and outgoing responses for debugging and monitoring.

---

## **Quick Start Guide**
To get started with GPTCoAssistant, refer to the [Quick Start Guide for GPTCoAssistant](Quick_Start_Guide.md).  
This guide includes detailed setup instructions, prerequisites, and integration with ChatGPT.

---

## **Important Information**

### **START_DIR**
- All file and folder operations performed via the API will take place within the directory specified as `START_DIR` during `setup.sh` execution.
- This ensures that operations are isolated to a controlled environment.
- To change the `START_DIR`, rerun `./setup.sh`.

---

## **Folder Structure**

- `app.py`: Main application script.
- `auth.py`: Handles API key authentication.
- `config.py`: Manages configuration from `config.ini`.
- `func_utils.py`: Provides utility functions for Git operations.
- `actions/`: Contains dynamically registered API scripts.
- `utils/`: Contains logging middleware.
- `logs/`: Stores request and response logs.
- `ngrok/`: Contains `ngrok.exe` for public URL generation.

---

## **Requirements**

- Python 3.8+
- Flask
- Git
- ngrok

---

## **Contributing**
Feel free to contribute by adding scripts to the `actions` folder. Ensure that scripts:
- Define a function named `<filename>_action`.
- Follow Flask route conventions.

---

## **License**
This project is licensed under the MIT License.
