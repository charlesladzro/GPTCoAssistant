#!/bin/bash

# Detect the platform (Windows or Linux)
PLATFORM="linux"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    PLATFORM="windows"
fi

# Predefined default values
DEFAULT_SERVER_URL="http://127.0.0.1:5000"
DEFAULT_TITLE="GPTCoAssistant"
DEFAULT_VERSION="1.0.0"
DEFAULT_SECRET_API_KEY="default_secret_key_@"
DEFAULT_START_DIR="my_project"

# Function to prompt for each configuration value
prompt_for_config_value() {
    local config_name="$1"
    local current_value="$2"
    local default_value="$3"
    local user_input

    # If current value exists, show it, otherwise show the predefined default
    if [[ -n "$current_value" ]]; then
        read -p "Enter $config_name (current: $current_value): " user_input
    else
        read -p "Enter $config_name (default: $default_value): " user_input
    fi

    # Use user input if provided; otherwise, fall back to current or default value
    if [[ -z "$user_input" ]]; then
        if [[ -n "$current_value" ]]; then
            echo "$current_value"
        else
            echo "$default_value"
        fi
    else
        echo "$user_input"
    fi
}

# Function to generate a 64-character random SECRET_API_KEY
generate_secret_key() {
    echo "Generating a 64-character random SECRET_API_KEY..."
    SECRET_KEY=$(openssl rand -base64 48 | tr -d '\n')
    echo "Generated SECRET_API_KEY: $SECRET_KEY"
    read -p "Would you like to use this key? ([y]/n): " use_key
    use_key=${use_key:-y} # Default to 'y' if input is empty
    if [[ "$use_key" != "y" ]]; then
        SECRET_API_KEY=$(prompt_for_config_value "SECRET_API_KEY" "${config_values[SECRET_API_KEY]}" "$SECRET_KEY")
    fi
}

# Function to read existing config or prompt for new values
manage_config_file() {
    CONFIG_FILE="config.ini"
    declare -A config_values

    # Load existing values if config.ini exists
    if [[ -f "$CONFIG_FILE" ]]; then
        echo "Existing config.ini found. Loading current values..."
        while IFS=' = ' read -r key value; do
            # Skip empty lines or lines starting with comments
            if [[ -z "$key" || "$key" =~ ^\# ]]; then
                continue
            fi
            if [[ "$key" != "" && "$value" != "" ]]; then
                config_values[$key]=$value
            fi
        done < "$CONFIG_FILE"
    fi

    # Prompt for each value, using either current or predefined defaults
    START_DIR=$(prompt_for_config_value "Project Name" "${config_values[START_DIR]}" "$DEFAULT_START_DIR")
    SERVER_URL=$(prompt_for_config_value "SERVER_URL" "${config_values[SERVER_URL]}" "$DEFAULT_SERVER_URL")
    TITLE=$(prompt_for_config_value "TITLE" "${config_values[TITLE]}" "$DEFAULT_TITLE")
    VERSION=$(prompt_for_config_value "VERSION" "${config_values[VERSION]}" "$DEFAULT_VERSION")

    # Automatically generate and assign SECRET_API_KEY
    generate_secret_key

    # Write the updated values back to config.ini
    echo "Writing to config.ini..."
    cat > "$CONFIG_FILE" <<EOL
[default]
START_DIR = $START_DIR
SERVER_URL = $SERVER_URL
TITLE = $TITLE
VERSION = $VERSION
SECRET_API_KEY = $SECRET_API_KEY
EOL
    echo "config.ini created/updated successfully."
}

# Step 1: Download and install ngrok
if [[ "$PLATFORM" == "linux" ]]; then
    echo "Downloading ngrok for Linux..."
    NGROK_ZIP="ngrok.zip"
    curl -s https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip -o $NGROK_ZIP
    unzip -o $NGROK_ZIP
    rm $NGROK_ZIP
    echo "ngrok downloaded successfully."
else
    echo "On Windows, please download ngrok manually from https://ngrok.com/download."
fi

# Step 2: Create a Python virtual environment
if [[ ! -d "venv" ]]; then
    echo "Creating Python virtual environment..."
    if [[ "$PLATFORM" == "windows" ]]; then
        python -m venv venv
    else
        python3 -m venv venv
    fi
    echo "Virtual environment created."
fi

# Step 3: Activate the virtual environment and install dependencies
if [[ "$PLATFORM" == "windows" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed successfully."

# Step 4: Create or update the config.ini file
manage_config_file

# Step 5: Create $START_DIR folder in current directory if it does not exist
if [[ ! -d "$START_DIR" ]]; then
    echo "Creating project directory: $START_DIR..."
    mkdir -p "$START_DIR"
    echo "Directory $START_DIR created successfully."
else
    echo "Directory $START_DIR already exists."
fi

# Final Message
echo "Setup completed successfully!"
echo "To start the virtual environment, run:"
if [[ "$PLATFORM" == "windows" ]]; then
    echo "venv\\Scripts\\activate"
else
    echo "source venv/bin/activate"
fi
echo "To run ngrok, execute: ./ngrok http 5000"
