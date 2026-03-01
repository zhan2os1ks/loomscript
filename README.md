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
loomit <file.loomscr> -d
```
### Arguments(for all commands):
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
Debug scripts:
```
loomit -[-d]ebug
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

## Loom-Builder
>[!NOTE]
>Development-Phase, I assume it will be packaged with vBETA-2
### Description
Loom-builder is an IDE(Integrated Development Environment). It's functionallity is far beyound compiling and packaging. You can edit and debug the code, include multiple folders and more!
### Why not LoomCompiler?
LoomCompiler is a fast but not reliable way to distribute your apps. Here's the full breakthrough:
| Pro/Con | LoomCompiler | Loombuilder | 
| :---: | :---: | :---: |
| Compiling script to a linux executable | ✅ | ✅ | 
| Compiling script to a windows executable  |  | ✅ |
| Including all used python-libraries | ✅ | ✅ |
| Including all used python-libraries outside of .loomscr |  | ✅ |
| Including other folders/assets |  | ✅ |
| A complete IDE(Integrated Development Environment) |  | ✅ |        
Also LoomCompiler is only the compiler(translator .loomscr -> .bin/.exe) that is built in the LoomBuilder.
### Why it's not ready now?
Because it's really hard to make a stable version of Loomscript while also making a Builder for the apps on **loomscript**!
## What will be added next?
I think I'll add more standart python programms later.
## Special Thanks:
- @github <- let me host this
- gemini.google.com <- helped with code formatting
