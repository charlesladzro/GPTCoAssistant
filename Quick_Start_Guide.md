# Quick Start Guide for GPTCoAssistant

## Introduction
Welcome to GPTCoAssistant! This guide will help you set up and use GPTCoAssistant quickly and efficiently. By the end, you’ll have a running instance ready to collaborate with ChatGPT in your local environment.

---

## 1. Prerequisites
Before you begin, ensure you have the following:

- **Operating System**: Tested on Windows, but it is expected to work on Linux and macOS as well.
- **Software**:
  - Python 3.8 or later (with pip installed).
  - Git for version control.
  - ngrok: A tunneling service (setup instructions below).
  - A ChatGPT Plus subscription (required to use custom GPTs).
- **Network**: Stable internet connection for API communication.

---

## 2. Installation

### Step 1: Clone the Repository
Open your terminal or command prompt and run:

```bash
git clone https://github.com/charlesladzro/GPTCoAssistant.git
cd GPTCoAssistant
```

### Step 2: Set Up ngrok
1. Download the **ngrok.exe** file for Windows from the official site:  
   [Download ngrok for Windows](https://download.ngrok.com/windows)

2. Place the downloaded `ngrok.exe` file in the `ngrok` folder within the GPTCoAssistant project directory. Create the folder if it does not exist.

3. Create an **ngrok account**:
   - Go to the [ngrok website](https://ngrok.com/) and sign up for a free account.
   - Once your account is created, log in and retrieve your authentication token from the dashboard.

4. Configure ngrok by running this command in your terminal:

```bash
ngrok config add-authtoken <your-auth-token>
```

Replace `<your-auth-token>` with the token from the ngrok dashboard.

5. Obtain your **static domain**:
   - In your ngrok dashboard, navigate to **"Deploy Your App Online"** and select **"Static Domain"**.
   - Note the static domain provided to you.

6. You will see a command like this:

```bash
ngrok http --url=<domain>.ngrok-free.app 80
```

The URL will look like `<domain>.ngrok-free.app`.

### Step 3: Run the Setup Script
Run the `setup.sh` script in **Git Bash**:

```bash
./setup.sh
```

During the script execution:

- **Environment Setup**: The script will create and activate a Python virtual environment and install the required dependencies.
- **Interactive Configuration**:
  - **Enter Project Name**: Input the name of your project or press Enter to accept the default (`my_project`).
  - **Enter SERVER_URL**: Enter your ngrok static domain (e.g., `<domain>.ngrok-free.app`).
  - The script will automatically generate a 64-character random `SECRET_API_KEY`.

**Example Output**:

```bash
Enter Project Name (default: my_project): my_project
Enter SERVER_URL - without https:// (default: 127.0.0.1:5000): example-domain.ngrok-free.app
Generating a 64-character random SECRET_API_KEY...
A new SECRET_API_KEY has been generated and set.
```

### Step 4: Review the config.ini File
The generated `config.ini` file will contain the following structure:

```ini
[default]
START_DIR = my_project
SERVER_URL = example-domain.ngrok-free.app
TITLE = GPTCoAssistant
VERSION = 1.0.0
SECRET_API_KEY = <generated-key>
```

Verify that the details match your project setup, particularly:

- **`START_DIR`**: Ensure it is the correct project directory.
- **`SERVER_URL`**: Ensure it is your ngrok static domain (e.g., `example-domain.ngrok-free.app`).
- **`SECRET_API_KEY`**: Verify that the generated key is present.

---

## 3. Running GPTCoAssistant

### Step 5: Start the Application
Run `run_app.bat`:

- Double-click on the `run_app.bat` file in the project directory.
- This will open three command prompt windows:
  - One for Flask.
  - One for ngrok.
  - One to stop the program.

Ensure all windows are running without errors.

---

## 4. Create a Custom GPT

### Step 6: Configure the Custom GPT
To integrate GPTCoAssistant with ChatGPT, create a custom GPT:

1. **Open `GPT_Instructions.md`**:
   - Open the file `GPT_Instructions.md` in Notepad++ or a similar text editor.

2. **Log in to ChatGPT**:
   - Ensure you have a paid **ChatGPT Plus** account.
   - Go to the ChatGPT website and click on **Explore GPTs**.
   - Click on **Create**.

3. **Configure the Custom GPT**:
   - **Name**: Copy the project name from `GPT_Instructions.md`.
   - **Description**: Copy the project description from `GPT_Instructions.md`.
   - **Instructions**: Copy all lines starting from `INSTRUCTIONS FOR YOU TO FOLLOW IT. IT IS MANDATORY` to the end of the file, ensuring this line is included.

4. **Set Capabilities**:
   - Uncheck all options under capabilities.

5. **Create a New Action**:
   - **Authentication**:
     - Click on the parameter icon and select **API Key**.
     - Enter the `SECRET_API_KEY` from `config.ini`, ensuring no leading or trailing spaces.
     - Select **Basic** for the authentication type and click **Save**.
   - **Schema**:
     - Click **Import from URL**.
     - Enter the full link:

```bash
https://<domain>.ngrok-free.app/openapi.yaml
```

Replace the entire `<domain>.ngrok-free.app` with your actual ngrok static link.

**Example**: If your static link is `example-domain.ngrok-free.app`, enter:

```bash
https://example-domain.ngrok-free.app/openapi.yaml
```

Click **Import** and ensure all actions are displayed.

6. **Finalize**:
   - Click **Create** in the top-right corner.
   - Select **Only Me** and click **Save**.

---

### Step 7: Verify the Custom GPT
Return to the main page of ChatGPT.
Verify that the custom GPT named **GPTCoAssistant** is listed and accessible.

---

## 5. Example Commands

### List All Files
To list all files in the root directory and its subdirectories:

1. Open the **GPTCoAssistant** custom GPT in ChatGPT.
2. Send the following command:

```plaintext
List all files in the root directory and its subdirectories.
```

The GPT will respond with a hierarchical list of all files and folders starting from the root directory.

### Create and Test a Hangman Game
To create and test a hangman game:

1. Open the **GPTCoAssistant** custom GPT in ChatGPT.
2. Send the following command:

```plaintext
Create and test a hangman game.
```

The GPT will create a Python script for the hangman game and test it by itself on your local machine.

---

## 6. Troubleshooting

### Common Issues
1. **ngrok or Flask Not Running**: Ensure all command windows opened by `run_app.bat` are active and error-free.
2. **Invalid API Key**: Verify the `SECRET_API_KEY` in the `config.ini` file and in the ChatGPT settings.
3. **Schema Import Fails**: Double-check the ngrok static domain URL in the schema import step.

---

## Conclusion
Congratulations! You’ve successfully set up and integrated GPTCoAssistant. 🎉 Explore its capabilities and streamline your workflows!
