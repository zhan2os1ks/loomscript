# Loomscript
Loomscript-vBETA-1 is a high-level python-based scripting toolkit designed to streamline the creation of modern, hardware-accelerated GUIs using the CustomTkinter framework. By abstracting complex Python code into a clean, block-based syntax. Loomscript allows developers to focus on UI structure and logic without the overhead of standard class-based GUI management.

## Technical Overview
Loomscript operates as a Recursive Block Parser. It handles memory management, widget parentage, and event-loop delegation, while allowing for In-Script Python (InPy) injection for low-level control.

## Installation
>[!Note]
>The following instructions are verified for Manjaro and Arch Linux. Compatibility with Debian/Ubuntu is currently untested.
To install the engine and the loomit command globally:
1. Clone the repository: `git clone https://github.com/Zhan2os1ks/loomscript`
2. Enter the folder: `cd loomscript`
3. Run the installer: `chmod +x install.sh && ./install.sh`
4. Refresh your shell:
  - Bash/Sh: `source ~/.bashrc`
  - Zsh: `source ~/.zshrc`

## Usage
### 1. Loomit: Execution Engine
Run scripts using the interpreter:
```
loomit <file.loomscr>
```
### 2. Loom-Compiler: Rapid Prototyping
A tool for early-stage application testing:
```
loomcompiler <file.loomscr>
```
### 3. Loom-Debugger: Logic Verification
Debug scripts and track variable states:
```
loomdebug <file.loomscr>
```
### Arguments(for all command):
Get the release number / version info:
```
loomit -[-v]ersion 
```
Get help/usage info:
```
loomit -[-h]elp 
```
Update LoomScript(v1.0+), get update info for LoomScript(vBETA-1):
```
loomit -[-u]pdate
```
>[!NOTE]
>`loomit --update` argument works only on `loomit` command.  
>It automatically updates the Wrapper, Builder, Debuger and Compiler/Engine.   
>The auto-update function only works from the stable release(v1.0+), so it doesn't work right now; on beta versions you have to update it manually!

## Requirements:
Python 3.12 or higher.
Python libraries: CustomTkinter, Py-TOML.
The install.sh script automates dependency installation via pacman or apt.

## Help
Documentation is available at: Zhan2os1ks.github.io/loomscript/help/ .

## Loom-Compiler
Loom-compiler is a utility written in Loomscript for quick app testing. It is not recommended for stable releases. For production-grade builds, use Loom-Builder.
