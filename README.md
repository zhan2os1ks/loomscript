# Loomscript
An easy programming language to write Qt5-apps, based on python.
## Installation (Manjaro/Arch[Also may work in DEB/UBUNTU distros. UNTESTED!])
To install the engine and the `loomit` command globally:

1. Clone this repo: `git clone https://github.com/Zhan2os1ks/loomscript`
2. Enter the folder: `cd loomscript`
3. Run the installer: `chmod +x install.sh && ./install.sh`
4. Refresh your shell: `source ~/.bashrc`
## Usage
Run your script using loomit alias:
``` BASH
loomit <yourfile.loomscr>
```
or the [-args]
```
loomit -[-h]elp | loomit -[-v]ersion
```
Compile your script into an app using 'loom-compile'
## Reqiurements
The engine is written on python(3.12 or higher), so make sure you have python installed. 
Also other python-libraries should be installed, like PyQt5, Py-TOML etc. 
`Note: Python is often installed with your linux distro; the installer installs all the required libraries itself through pacman/apt.` 
## Help
Overall help is avilable on Zhan2os1ks.github.io/loomscript/help/. Usage look in [#Usage](https://github.com/zhan2os1ks/loomscript/edit/main/README.md#usage)
## Loom-Compile(r)
Loom-compiler is the Compiler for loomscript, that's also written on python/loom itself. 
