#!/bin/bash

# --- 1. Path Setup ---
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

echo "🏗️  Loom-Compiler: Baking $NAME into standalone binary..."

# --- 2. Read the .loomscr content into a variable ---
# We escape backticks and dollar signs to ensure the content
# is passed correctly into the python heredoc.
SCRIPT_CONTENT=$(cat "$SOURCE_ABS")

# --- 3. Create the Python Build Wrapper ---
# We use a triple-quoted string in Python to hold the Loomscript code.
cat <<EOF > build_wrapper.py
import sys
import os

# Ensure the engine from /opt can be found
sys.path.append("$LIB_PATH")

from loomengine import LoomParser, LoomMemory, LoomUI

# The "Baked" Loomscript content
LOOM_CODE = """$SCRIPT_CONTENT"""

if __name__ == "__main__":
    mem = LoomMemory()
    ui = LoomUI(mem)
    ui.memory = mem
    parser = LoomParser(mem, ui)

    # Run from the embedded string instead of a file
    # We convert the string into a list of lines for the parser
    parser.parse_block(LOOM_CODE.splitlines())

    if mem.active_window:
        mem.active_window.mainloop()
EOF

# --- 4. Execute PyInstaller ---
echo "Bundling with PyInstaller..."
pyinstaller --onefile --noconsole \
    --paths "$LIB_PATH" \
    --name "$NAME" \
    --clean \
    build_wrapper.py

# --- 5. Cleanup ---
echo "Cleaning up..."
rm build_wrapper.py "$NAME.spec"
rm -rf build/

echo "------------------------------------------------"
echo "✅ Compilation complete: ./dist/$NAME"
echo "This binary is now fully standalone."
echo "------------------------------------------------"
