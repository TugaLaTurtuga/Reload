#!/bin/bash

SCRIPT_DIR=$(dirname "$0")

# Function to run Update_screen.py in the background
run_update_screen() {
    if [ -f "$SCRIPT_DIR/Contents/Saves/Update_screen.py" ]; then
        python3 "$SCRIPT_DIR/Contents/Saves/Update_screen.py" &
        UPDATE_SCREEN_PID=$!
    else
        echo "Contents/Saves/Update_screen.py not found. Please check the path and try again."
        exit 1
    fi
}

# Function to stop the Update_screen.py process
stop_update_screen() {
    if [ -n "$UPDATE_SCREEN_PID" ]; then
        kill $UPDATE_SCREEN_PID
    fi
}


run_update_screen
# Check for Python installation
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Installing Python3..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # For macOS
        if ! command -v brew &>/dev/null; then
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python
        # Upgrade pip
        python3 -m pip install --upgrade pip
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # For Linux
        if command -v apt-get &>/dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip
            # Upgrade pip
            python3 -m pip install --upgrade pip
        elif command -v yum &>/dev/null; then
            sudo yum install -y python3 python3-pip
            # Upgrade pip
            python3 -m pip install --upgrade pip
        elif command -v pacman &>/dev/null; then
            sudo pacman -Syu python python-pip
            # Upgrade pip
            python3 -m pip install --upgrade pip
        else
            echo "Unsupported package manager. Please install Python3 manually."
            exit 1
        fi
    else
        echo "Unsupported OS type. Please install Python3 manually."
        exit 1
    fi
else
    echo "Python3 is already installed."
fi

# Install pygame and mutagen
python3 -m pip install pygame mutagen
stop_update_screen


# Run the Main.py script
if [ -f "$SCRIPT_DIR/Contents/Main.py" ]; then
    python3 "$SCRIPT_DIR/Contents/Main.py"
else
    echo "Contents/Main.py not found. Please check the path and try again."
    exit 1
fi