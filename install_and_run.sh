#!/bin/bash
# RPG Game - One-Command Installation & Run Script
# Works on macOS and Linux

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  RPG Game - Installation Script${NC}"
echo -e "${BLUE}=====================================${NC}\n"

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
        sudo apt install -y python3 python3-pip
    fi
else
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}\n"
fi

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}\n"
else
    echo -e "${YELLOW}Warning: Some dependencies may not have installed correctly${NC}\n"
fi

# Run the game
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}  Launching RPG Game...${NC}"
echo -e "${GREEN}=====================================${NC}\n"

python3 game.py

# Cleanup on exit
echo -e "\n${BLUE}Thanks for playing!${NC}"
