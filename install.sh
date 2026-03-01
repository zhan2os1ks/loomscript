#!/bin/bash

# --- 1. Root Privileges Check ---
if [ "$EUID" -ne 0 ]; then
  echo "Error: Installation requires root privileges."
  echo "Please run: sudo ./install.sh"
  exit 1
fi

# --- 2. Smart Path Detection ---
# This line finds the directory where the script is actually sitting
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPT_DIR" || exit 1

# --- 3. Version Retrieval ---
if [ ! -f "version.txt" ]; then
    echo "Critical Error: version.txt not found in $SCRIPT_DIR"
    exit 1
fi
VERSION=$(cat version.txt | tr -d '\n' | tr -d '\r')
TARGET_DIR="/opt/loomscript/$VERSION"

echo "------------------------------------------------"
echo "Loomscript Installer - Version $VERSION"
echo "Target: $TARGET_DIR"
echo "------------------------------------------------"

# --- 4. Dependency Management ---
echo "Checking system dependencies..."

if command -v pacman >/dev/null; then
    echo "Detected Package Manager: pacman (Arch/Manjaro)"
    pacman -Sy --noconfirm --needed python python-pip tk
elif command -v apt >/dev/null; then
    echo "Detected Package Manager: apt (Debian/Ubuntu)"
    apt update
    apt install -y python3 python3-pip python3-tk
else
    echo "Warning: Unknown package manager. Manual install of Python3/Pip/Tk may be required."
fi

echo "Installing Python libraries..."
pip3 install customtkinter toml pyinstaller --break-system-packages || pip3 install customtkinter toml pyinstaller

# --- 5. File Migration ---
echo "Creating directory structure at $TARGET_DIR..."
mkdir -p "$TARGET_DIR"

echo "Copying engine files from $SCRIPT_DIR..."
cp -r "$SCRIPT_DIR"/* "$TARGET_DIR/"

# --- 6. Global Binary Wrappers (/usr/local/bin) ---
echo "Generating global execution wrappers..."

cat <<EOF > /usr/local/bin/loomit
#!/bin/bash
sudo python3 "$TARGET_DIR/loomengine.py" "\$@"
EOF
chmod +x /usr/local/bin/loomit

cat <<EOF > /usr/local/bin/loomcompiler
#!/bin/bash
sudo bash "$TARGET_DIR/compiler.sh" "\$@"
EOF
chmod +x /usr/local/bin/loomcompiler

cat <<EOF > /usr/local/bin/loombuilder
#!/bin/bash
bash "$TARGET_DIR/loombuilder.sh" "\$@"
EOF
chmod +x /usr/local/bin/loombuilder

# --- 7. Shell Alias Configuration (.bashrc and .zshrc) ---
ACTUAL_USER="${SUDO_USER:-$USER}"
USER_HOME=$(eval echo "~$ACTUAL_USER")
RC_FILES=(".bashrc" ".zshrc")

echo "Configuring shell aliases for user: $ACTUAL_USER"

for RC_FILE in "${RC_FILES[@]}"; do
    RC_PATH="$USER_HOME/$RC_FILE"

    if [ -f "$RC_PATH" ]; then
        echo "Updating $RC_FILE..."

        # Remove old aliases
        sed -i '/# Loomscript Aliases/d' "$RC_PATH"
        sed -i '/alias loomit=/d' "$RC_PATH"
        sed -i '/alias loomcompiler=/d' "$RC_PATH"
        sed -i '/alias loombuilder=/d' "$RC_PATH"

        # Append new aliases
        {
            echo "# Loomscript Aliases"
            echo "alias loomit='sudo python3 $TARGET_DIR/loomengine.py'"
            echo "alias loomcompiler='sudo bash $TARGET_DIR/compiler.sh'"
            echo "alias loombuilder='bash $TARGET_DIR/loombuilder.sh'"
        } >> "$RC_PATH"

        chown "$ACTUAL_USER:$ACTUAL_USER" "$RC_PATH"
    fi
done

echo "------------------------------------------------"
echo "Installation complete."
echo "Please restart your terminal or run: source ~/.zshrc (or .bashrc)"
echo "------------------------------------------------"
