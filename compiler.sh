#!/bin/bash

# --- 1. Path Setup ---
# Find where the compiler itself is running from (should be /opt/loomscript/vBeta-1/)
LIB_PATH=$(dirname "$(readlink -f "$0")")

if [ -z "$1" ]; then
    echo "Usage: loomcompiler <filename.loomscr>"
    exit 1
fi

SOURCE_ABS=$(readlink -f "$1")
NAME=$(basename "$SOURCE_ABS" .loomscr)

if [ ! -f "$SOURCE_ABS" ]; then
    echo "Error: Source file $1 not found."
    exit 1
fi

echo "🏗️  Loom-Compiler: Packaging $NAME..."

# --- 2. Create the Python Build Wrapper ---
# We inject the LIB_PATH into sys.path so PyInstaller can find your engine
cat <<EOF > build_wrapper.py
import sys
import os

# Add the Loomscript engine directory to the path
sys.path.append("$LIB_PATH")

from loomengine import LoomParser, LoomMemory, LoomUI

if __name__ == "__main__":
    # Initialize the engine components
    mem = LoomMemory()
    ui = LoomUI(mem)
    ui.memory = mem # Link memory to UI
    parser = LoomParser(mem, ui)

    # Run the user's script
    # Note: We use the absolute path captured at compile time
    parser.run("$SOURCE_ABS")
EOF

# --- 3. Execute PyInstaller ---
# --onefile: Bundles everything into a single executable
# --noconsole: Prevents a command prompt from popping up (for GUI apps)
# --paths: Explicitly tells PyInstaller where to look for loomengine.py
echo "Running PyInstaller logic..."
pyinstaller --onefile --noconsole \
    --paths "$LIB_PATH" \
    --name "$NAME" \
    build_wrapper.py

# --- 4. Cleanup ---
echo "Cleaning up temporary build files..."
rm build_wrapper.py "$NAME.spec"
rm -rf build/

echo "------------------------------------------------"
echo "✅ Compilation complete."
echo "Binary Location: ./dist/$NAME"
echo "------------------------------------------------"
