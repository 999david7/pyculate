import customtkinter as ctk
import math
import statistics
from datetime import datetime

# ==================== APP SETUP ====================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Ultimate Glass Calculator")
app.geometry("460x640")
app.minsize(420, 640)

# ==================== SAFE MATH ====================
allowed_math = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
allowed_math.update({
    "abs": abs,
    "round": round,
    "pow": pow
})

# ==================== STATE ====================
expression = ""
memory = 0
history = []

# ==================== CORE LOGIC ====================
def update_display():
    display_var.set(expression)


def press(value):
    global expression
    expression += str(value)
    update_display()


def clear():
    global expression
    expression = ""
    update_display()


def backspace():
    global expression
    expression = expression[:-1]
    update_display()


def add_history(expr, result):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {expr} = {result}"
    history.append(entry)
    history_box.insert("end", entry + "\n")
    history_box.see("end")


def calculate():
    global expression
    try:
        result = eval(expression, {"__builtins__": None}, allowed_math)
        add_history(expression, result)
        expression = str(result)
        update_display()
    except Exception:
        display_var.set("Error")
        expression = ""

# ==================== MEMORY ====================
def memory_add():
    global memory
    try:
        memory += float(expression or 0)
    except:
        pass


def memory_sub():
    global memory
    try:
        memory -= float(expression or 0)
    except:
        pass


def memory_recall():
    press(str(memory))


def memory_clear():
    global memory
    memory = 0

# ==================== STATISTICS ====================
def stats_mean():
    try:
        nums = list(map(float, expression.split(",")))
        result = statistics.mean(nums)
        press(str(result))
    except:
        display_var.set("Stats Error")


def stats_std():
    try:
        nums = list(map(float, expression.split(",")))
        result = statistics.stdev(nums)
        press(str(result))
    except:
        display_var.set("Stats Error")

# ==================== UNIT CONVERTER ====================
def meters_to_feet():
    try:
        val = float(expression)
        clear()
        press(str(val * 3.28084))
    except:
        display_var.set("Conv Error")


def kg_to_lb():
    try:
        val = float(expression)
        clear()
        press(str(val * 2.20462))
    except:
        display_var.set("Conv Error")

# ==================== KEYBOARD ====================
def key_handler(event):
    key = event.char
    if key in "0123456789+-*/().,":
        press(key)
    elif key == "\r":
        calculate()
    elif key == "\x08":
        backspace()
    elif key.lower() == "c":
        clear()

app.bind("<Key>", key_handler)

# ==================== LAYOUT ROOT ====================
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

main = ctk.CTkFrame(app, corner_radius=28)
main.grid(row=0, column=0, padx=18, pady=18, sticky="nsew")
main.grid_rowconfigure(1, weight=1)
main.grid_columnconfigure(0, weight=1)

# ==================== DISPLAY ====================
display_var = ctk.StringVar()

display = ctk.CTkEntry(
    main,
    textvariable=display_var,
    height=100,
    font=("Segoe UI", 40),
    justify="right",
    corner_radius=22
)
display.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="ew")

# ==================== TABS ====================
tabs = ctk.CTkTabview(main, corner_radius=20)
tabs.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

calc_tab = tabs.add("Basic")
sci_tab = tabs.add("Scientific")
stats_tab = tabs.add("Statistics")
conv_tab = tabs.add("Convert")
history_tab = tabs.add("History")

for tab in [calc_tab, sci_tab, stats_tab, conv_tab]:
    tab.grid_columnconfigure((0, 1, 2, 3), weight=1)
    tab.grid_rowconfigure(tuple(range(6)), weight=1)

# ==================== BASIC ====================
basic = [
    ("C", clear), ("⌫", backspace), ("(", lambda: press("(")), (")", lambda: press(")")),
    ("7", lambda: press("7")), ("8", lambda: press("8")), ("9", lambda: press("9")), ("/", lambda: press("/")),
    ("4", lambda: press("4")), ("5", lambda: press("5")), ("6", lambda: press("6")), ("*", lambda: press("*")),
    ("1", lambda: press("1")), ("2", lambda: press("2")), ("3", lambda: press("3")), ("-", lambda: press("-")),
    ("0", lambda: press("0")), (".", lambda: press(".")), ("=", calculate), ("+", lambda: press("+")),
]

for i, (t, c) in enumerate(basic):
    ctk.CTkButton(calc_tab, text=t, command=c, font=("Segoe UI", 20, "bold"), corner_radius=16)\
        .grid(row=i // 4, column=i % 4, padx=6, pady=6, sticky="nsew")

# ==================== SCIENTIFIC ====================
sci = [
    ("sin", lambda: press("sin(")), ("cos", lambda: press("cos(")),
    ("tan", lambda: press("tan(")), ("asin", lambda: press("asin(")),
    ("acos", lambda: press("acos(")), ("atan", lambda: press("atan(")),
    ("sqrt", lambda: press("sqrt(")), ("log", lambda: press("log(")),
    ("ln", lambda: press("log(")), ("^", lambda: press("**")),
    ("!", lambda: press("factorial(")), ("π", lambda: press("pi")),
    ("e", lambda: press("e")), ("M+", memory_add),
    ("M-", memory_sub), ("MR", memory_recall),
    ("MC", memory_clear),
]

for i, (t, c) in enumerate(sci):
    ctk.CTkButton(sci_tab, text=t, command=c, font=("Segoe UI", 16, "bold"), corner_radius=16)\
        .grid(row=i // 4, column=i % 4, padx=6, pady=6, sticky="nsew")

# ==================== STATISTICS ====================
stats_buttons = [
    ("mean (a,b,c)", stats_mean),
    ("std dev", stats_std),
]

for i, (t, c) in enumerate(stats_buttons):
    ctk.CTkButton(stats_tab, text=t, command=c, font=("Segoe UI", 18), corner_radius=16)\
        .grid(row=i, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

# ==================== CONVERSIONS ====================
conv_buttons = [
    ("meters → feet", meters_to_feet),
    ("kg → pounds", kg_to_lb),
]

for i, (t, c) in enumerate(conv_buttons):
    ctk.CTkButton(conv_tab, text=t, command=c, font=("Segoe UI", 18), corner_radius=16)\
        .grid(row=i, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

# ==================== HISTORY ====================
history_tab.grid_rowconfigure(0, weight=1)
history_tab.grid_columnconfigure(0, weight=1)

history_box = ctk.CTkTextbox(history_tab, font=("Consolas", 14), corner_radius=16)
history_box.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

# ==================== RUN ====================
app.mainloop()