# Loomscript
An easy python-toolkit language to write cTk-apps.
## Installation (Manjaro/Arch[Also may work in DEB/UBUNTU distros. UNTESTED!])
To install the engine and the `loomit` command globally:

1. Clone this repo: `git clone https://github.com/Zhan2os1ks/loomscript`
2. Enter the folder: `cd loomscript`
3. Run the installer: `chmod +x install.sh && ./install.sh`
4. Refresh your shell: `source ~/.bashrc`
## Usage
### Run your script using loomit alias:
``` 
loomit <yourfile.loomscr>
```
or the [<ins>-args</ins>]
```
loomit -[-h]elp | [-v]ersion
```
### Compile your script into an app using loomcompiler alias:
```
loomcompiler <file.loomscr>
```
or the [<ins>-args</ins>]
```
loomcompiler -[-h]elp | -[-v]ersion
```
See more about it on [#Loom-Compiler](https://github.com/zhan2os1ks/loomscript/edit/main/README.md#loom-compiler) 
### Loomdebuger - debug your script:
```
loomdebug <file.loomscr>
```
or the [<ins>-args</ins>]
```
loomdebuger -[-h]elp | [-v]ersion
```
## Reqiurements
The engine is written on python(3.12 or higher), so make sure you have python installed. 
Also other python-libraries should be installed, like CustomTKinter, Py-TOML etc. 
`Note: Python is often installed with your linux distro; the installer installs all the required libraries itself through pacman/apt.` 
## Help
Overall help is avilable on Zhan2os1ks.github.io/loomscript/help/. Usage look in [#Usage](https://github.com/zhan2os1ks/loomscript/edit/main/README.md#usage)
## Loom-Compiler
Loom-compiler is the Compiler for loomscript, that's also written on python/loom itself. It's an easy tool for early ass app tests. It's not recommended for stable app releases. To make an app pro-way, you can use [Loom-Builder]
