# Complete Game Installation & Setup Guide

## Quick Start (30 seconds)

```bash
# 1. Install Python 3.8+ from python.org
# 2. Open terminal/command prompt and run:
pip install -r requirements.txt
python game.py
```

That's it! The game should launch.

---

## Detailed Installation by OS

### Windows

1. **Download and Install Python:**
   - Go to https://www.python.org/downloads/
   - Download Python 3.11 or higher
   - **IMPORTANT:** Check "Add Python to PATH" during installation
   - Click Install

2. **Open Command Prompt:**
   - Press `WIN + R`
   - Type `cmd` and press Enter

3. **Navigate to your game folder:**
   ```cmd
   cd path\to\a-python-game-idk-
   ```

4. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the game:**
   ```cmd
   python game.py
   ```

---

### macOS

1. **Install Python (if not already installed):**
   ```bash
   # Using Homebrew (recommended)
   brew install python3
   
   # Or download from https://www.python.org/downloads/
   ```

2. **Open Terminal:**
   - Press `CMD + Space`, type `terminal`, press Enter

3. **Navigate to your game folder:**
   ```bash
   cd /path/to/a-python-game-idk-
   ```

4. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run the game:**
   ```bash
   python3 game.py
   ```

**Note for Apple Silicon (M1/M2/M3):**
If you get pygame installation errors:
```bash
pip3 install pygame --upgrade --force-reinstall
```

---

### Linux (Ubuntu/Debian)

1. **Install Python and pip:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Navigate to your game folder:**
   ```bash
   cd /path/to/a-python-game-idk-
   ```

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the game:**
   ```bash
   python3 game.py
   ```

---

## Alternative: Using Virtual Environment (Recommended)

### Why use a virtual environment?
- Keeps your project dependencies isolated
- Prevents conflicts with other Python projects
- Easy to clean up

### Setup

**All Operating Systems:**

1. **Navigate to your game folder:**
   ```bash
   cd path/to/a-python-game-idk-
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment:**
   
   **Windows:**
   ```cmd
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game:**
   ```bash
   python game.py
   ```

6. **Deactivate when done:**
   ```bash
   deactivate
   ```

---

## Troubleshooting

### Problem: "command not found: python"
**Solution:** Python might not be in your PATH
- Reinstall Python and check "Add Python to PATH"
- Or use `python3` instead of `python`

### Problem: "No module named 'pygame'"
**Solution:** Pygame didn't install correctly
```bash
pip install pygame --upgrade
```

If still failing:
```bash
pip uninstall pygame
pip install pygame
```

### Problem: Black window appears but game doesn't start
**Solution:** Try these steps:
1. Close the window
2. Update pygame: `pip install --upgrade pygame`
3. Run again: `python game.py`

### Problem: "Port already in use" or similar
**Solution:** This is normal for Pygame. Just try again:
```bash
python game.py
```

### Problem: Game runs slowly
**Solution:**
1. Close other applications
2. Check your system has enough RAM (2GB+ recommended)
3. Update your graphics drivers

---

## Verify Installation

To verify everything is installed correctly, run:

```bash
python -c "import pygame; print('Pygame version:', pygame.version.ver)"
```

You should see output like:
```
Pygame version: 2.5.2
```

---

## Running with Different Options

### Run in full debug mode (shows more info):
```bash
python -u game.py
```

### Check Python version:
```bash
python --version
```

### Check pip installed packages:
```bash
pip list
```

---

## Getting Help

If you still have issues:

1. **Check Python version:** Must be 3.8 or higher
   ```bash
   python --version
   ```

2. **Verify files are present:**
   - `game.py` should exist
   - `requirements.txt` should exist

3. **Try with virtual environment** (see above section)

4. **Check the original game still works:**
   ```bash
   python fun.py
   ```
   (This is the text-based version, should run without GUI)

---

## System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|------------|
| Python | 3.8 | 3.10+ |
| RAM | 512 MB | 2 GB+ |
| Storage | 50 MB | 100 MB |
| Screen Resolution | 1024x600 | 1200x700 |
| OS | Windows 7+ / macOS 10.12+ / Linux | Any modern OS |

---

## Next Steps

Once the game is running:
1. **Press SPACE** on the main menu to start
2. **Follow on-screen instructions**
3. **Have fun defeating enemies!**

---

## Updating the Game

To get latest updates from GitHub:

```bash
cd path/to/a-python-game-idk-
git pull origin main
```

(Requires Git installed. Download from https://git-scm.com/)

---

Good luck, adventurer! 🎮⚔️
