#!/bin/bash
# RPG Game - One-Command Installation & Run Script
# Works on macOS and Linux (handles virtual environments automatically)

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  RPG Game - Installation Script${NC}"
echo -e "${BLUE}=====================================${NC}\n"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || exit

echo -e "${YELLOW}Current directory: $SCRIPT_DIR${NC}\n"

# Check if Python is installed
echo -e "${YELLOW}Checking for Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python3 not found. Installing...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install python3
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv
    fi
else
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}\n"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}\n"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}\n"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}\n"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}\n"
else
    echo -e "${YELLOW}Warning: Some dependencies may not have installed correctly${NC}\n"
fi

# Run the game
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}  Launching RPG Game...${NC}"
echo -e "${GREEN}=====================================${NC}\n"

python game.py

# Cleanup
echo -e "\n${BLUE}Thanks for playing!${NC}"
echo -e "${YELLOW}Virtual environment is still active. Type 'deactivate' to exit it.${NC}"
