import sys
import subprocess
import os
import signal
import tkinter as tk
import customtkinter as ctk

#check version
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_PATH = os.path.join(BASE_DIR, "version.txt")
try:
    with open(VERSION_PATH, "r") as f:
        version = f.read().strip()
except FileNotFoundError:
    print(f"LoomError: version.txt not found at {VERSION_PATH}")
    sys.exit(1)

# Clean exit on Ctrl+C
signal.signal(signal.SIGINT, signal.SIG_DFL)

class LoomMemory:
    def __init__(self):
        self.vars = {}
        self.active_window = None

class LoomDebugger:
    def __init__(self, filename):
        self.filename = filename
        self.errors = []
        self.vars_seen = set()

    def check(self):
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"LoomDebug: File {self.filename} not found.")
            sys.exit(1)

        brace_stack = []
        for i, raw_line in enumerate(lines, 1):
            line = raw_line.split("#")[0].strip()
            if not line: continue

            # Brace Matching
            if "{" in line: brace_stack.append(i)
            if "}" in line:
                if not brace_stack: self.errors.append(f"Line {i}: Unexpected '}}' (no matching block)")
                else: brace_stack.pop()

            # Syntax: var check
            if line.startswith("var "):
                if "=" not in line:
                    self.errors.append(f"Line {i}: 'var' declaration missing '=' assignment")
                else:
                    v_name = line.split("var ")[1].split("=")[0].strip()
                    if not v_name: self.errors.append(f"Line {i}: Variable name is empty")
                    self.vars_seen.add(v_name)

            # Check for undeclared parents in widgets
            if "in=" in line:
                p_win = line.split("in=")[1].split(")")[0].strip()
                if p_win not in self.vars_seen:
                    self.errors.append(f"Line {i}: Target window '{p_win}' used before declaration")

        # Final check for unclosed blocks
        for line_num in brace_stack:
            self.errors.append(f"Line {line_num}: Unclosed block starting with '{{'")

        self.report()

    def report(self):
        if not self.errors:
            print("Verdict: Code is valid. (0 errors)")
            sys.exit(0)
        else:
            print(f"Verdict: Code needs improvements. Found {len(self.errors)} errors.")
            for err in self.errors:
                print(f"  [!] {err}")
            sys.exit(len(self.errors))

class LoomUI:
    def __init__(self, memory):
        self.memory = memory
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def create_window(self, var_name, title):
        w = ctk.CTk() if not self.memory.active_window else ctk.CTkToplevel()
        w.title(title)
        w.geometry("600x450")
        self.memory.vars[var_name] = w
        self.memory.active_window = w

    def center_window(self, win_obj):
        win_obj.update_idletasks()
        width, height = win_obj.winfo_width(), win_obj.winfo_height()
        x = (win_obj.winfo_screenwidth() // 2) - (width // 2)
        y = (win_obj.winfo_screenheight() // 2) - (height // 2)
        win_obj.geometry(f'{width}x{height}+{x}+{y}')

    def create_menu(self, var_name, parent_name):
        parent = self.memory.vars.get(parent_name)
        if not parent: return
        m = tk.Menu(parent, tearoff=0)
        self.memory.vars[var_name] = m
        if isinstance(parent, (ctk.CTk, ctk.CTkToplevel)):
            parent.config(menu=m)

    def create_widget(self, w_type, var_name, text, parent_name=None):
        parent = self.memory.vars.get(parent_name) if parent_name else self.memory.active_window
        if not parent: return
        widgets = {"label": ctk.CTkLabel, "button": ctk.CTkButton, "checkbox": ctk.CTkCheckBox, "radio": ctk.CTkRadioButton}
        if w_type in widgets:
            obj = widgets[w_type](parent, text=text)
            self.memory.vars[var_name] = obj

class LoomParser:
    def __init__(self, memory, ui):
        self.memory = memory
        self.ui = ui

    def extract_block(self, lines, start_idx):
        block, brace_count, i = [], 0, start_idx
        if "{" in lines[i]:
            brace_count += 1
            first = lines[i].split("{", 1)[1]
            if first.strip(): block.append(first)
        i += 1
        while i < len(lines) and brace_count > 0:
            line = lines[i]
            if "{" in line: brace_count += 1
            if "}" in line: brace_count -= 1
            if brace_count > 0: block.append(line)
            elif brace_count == 0:
                last = line.split("}")[0]
                if last.strip(): block.append(last)
                break
            i += 1
        return block, i

    def parse_block(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i].split("#")[0].strip()
            if not line: i += 1; continue

            # Event: onclick:inpy { ... }
            if ".onclick:inpy" in line and "{" in line:
                obj_name = line.split(".")[0].strip()
                obj = self.memory.vars.get(obj_name)
                block, new_i = self.extract_block(lines, i)
                code = "\n".join(block)
                if obj: obj.configure(command=lambda c=code: exec(c, {}, self.memory.vars))
                i = new_i + 1; continue

            # Loops / Conditionals / Python Injection
            if any(line.startswith(x) for x in ["inpy", "if", "while", "for"]):
                keyword = line.split()[0].split("(")[0]
                block, new_i = self.extract_block(lines, i)
                if keyword == "inpy": exec("\n".join(block), {}, self.memory.vars)
                elif keyword == "if":
                    cond = line.split("(")[1].split(")")[0]
                    if eval(cond, {}, self.memory.vars): self.parse_block(block)
                elif keyword == "while":
                    cond = line.split("(")[1].split(")")[0]
                    while eval(cond, {}, self.memory.vars): self.parse_block(block)
                elif keyword == "for":
                    v_name, it = line.split("(")[1].split(")")[0].split(" in ")
                    for val in eval(it, {}, self.memory.vars):
                        self.memory.vars[v_name.strip()] = val
                        self.parse_block(block)
                i = new_i + 1; continue

            self.execute_line(line)
            i += 1

    def execute_line(self, line):
        # Variable & Widget Creation
        if line.startswith("var "):
            name, call = line.split("var ")[1].split("=", 1)
            name, call = name.strip(), call.strip()
            if "window(" in call: self.ui.create_window(name, call.split('("')[1].split('")')[0])
            elif "menu(" in call: self.ui.create_menu(name, call.split("in=")[1].split(")")[0].strip())
            elif "(" in call:
                w_type = call.split("(")[0]
                params = call.split("(", 1)[1].rsplit(")", 1)[0]
                text = params.split(",")[0].strip('"')
                p_win = params.split("in=")[1].strip() if "in=" in params else None
                self.ui.create_widget(w_type, name, text, p_win)
            else:
                try: self.memory.vars[name] = eval(call, {}, self.memory.vars)
                except: self.memory.vars[name] = call.strip('"')
            return

        # Object Actions
        if "." in line:
            obj_name, action = line.split(".", 1)
            obj = self.memory.vars.get(obj_name.strip())
            if not obj: return
            if action == "center()": self.ui.center_window(obj)
            elif action.startswith("addcascade("):
                lbl = action.split("label=")[1].split(",")[0].strip().strip('"')
                sub = action.split("menu=")[1].split(")")[0].strip()
                obj.add_cascade(label=lbl, menu=self.memory.vars.get(sub))
            elif action.startswith("addcommand("):
                lbl = action.split("label=")[1].split(",")[0].strip().strip('"')
                cmd_str = action.split("onclick:")[1].split(")")[0].strip() if "onclick:" in action else None
                def menu_trigger(c=cmd_str):
                    if not c: return
                    if "shell(" in c: subprocess.run(c.split('("')[1].split('")')[0], shell=True)
                    elif "." in c:
                        t_obj = self.memory.vars.get(c.split(".")[0])
                        if "hide()" in c: t_obj.withdraw() if hasattr(t_obj, 'withdraw') else t_obj.pack_forget()
                        elif "show()" in c: t_obj.deiconify() if hasattr(t_obj, 'deiconify') else t_obj.pack()
                obj.add_command(label=lbl, command=menu_trigger)
            elif action.startswith("addseparator()"): obj.add_separator()
            elif action.startswith("resize("):
                dims = action.split("(")[1].split(")")[0].split(",")
                obj.geometry(f"{dims[0].strip()}x{dims[1].strip()}")
            elif action.startswith("pack("):
                arg_str = action.split("(")[1].rsplit(")", 1)[0]
                kwargs = {p.split("=")[0].strip(): p.split("=")[1].strip().strip('"') for p in arg_str.split(",")} if arg_str.strip() else {}
                obj.pack(**kwargs)

        # Updated Theme Logic: theme(m="dark", c="blue")
        if line.startswith("theme("):
            params = line.split("(", 1)[1].rsplit(")", 1)[0]
            if 'm="' in params: ctk.set_appearance_mode(params.split('m="')[1].split('"')[0])
            if 'c="' in params: ctk.set_default_color_theme(params.split('c="')[1].split('"')[0])

    def run(self, filename):
        try:
            with open(filename, 'r') as f: self.parse_block(f.readlines())
            if self.memory.active_window: self.memory.active_window.mainloop()
        except Exception as e: print(f"LoomError: {e}")

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print("Usage: loomit <file.loomscr> [-db]")
        sys.exit(1)

    # 1. Version and Help checks
    if any(arg in ["-v", "--version"] for arg in args):
        print("Current LoomScript version is: "+version)
        sys.exit(0)

    if any(arg in ["-h", "--help"] for arg in args):
        print("Loomscript Help:")
        print("  loomit <file>       Run script")
        print("  loomit <file> -d    Debug script (check for syntax/logic errors)")
        print("  loomit <file> -v    Check current LoomScript version")
        print("  loomit <file> -u    Check for uppdates/Update LoomScript")
        print("For further help check: https://zhan2os1ks.github.io/loomscript/help/ .")
        sys.exit(0)

    # 2. Separate filename from flags
    filename = None
    is_debug = False

    for arg in args:
        if arg in ["-d", "--debug"]:
            is_debug = True
        else:
            filename = arg

    # 3. Execution Logic
    if is_debug:
        debugger = LoomDebugger(filename)
        debugger.check()
    else:
        p = LoomParser(LoomMemory(), LoomUI(None))
        p.ui.memory = p.memory
        p.run(filename)
