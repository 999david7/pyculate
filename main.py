import customtkinter as ctk
import math
import statistics
from datetime import datetime

# ==================== SETUP ====================
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("500x450")
app.title("Calculator")
app.resizable(True, True)
app.configure(fg_color="#000000")

# ==================== SAFE MATH ====================
allowed_math = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
allowed_math.update({"abs": abs, "round": round, "pow": pow})

# ==================== STATE ====================
expression = ""
memory = 0
history = []
advanced_mode = False

# ==================== DISPLAY ====================
display_var = ctk.StringVar(value="0")

def update_display(value=None):
    if value is not None:
        display_var.set(value)
    else:
        display_var.set(expression if expression else "0")

display = ctk.CTkLabel(
    app,
    textvariable=display_var,
    font=("Helvetica Neue", 42),
    text_color="white",
    anchor="e",
    padx=20
)
display.pack(fill="both", pady=(20, 10))

# ==================== CORE ====================
def press(val):
    global expression
    expression += str(val)
    update_display()

def clear():
    global expression
    expression = ""
    update_display("0")

def backspace():
    global expression
    expression = expression[:-1]
    update_display()

def calculate():
    global expression
    try:
        result = eval(expression, {"__builtins__": None}, allowed_math)
        add_history(expression, result)
        expression = str(result)
        update_display()
    except:
        update_display("Error")
        expression = ""

# ==================== HISTORY ====================
def add_history(expr, result):
    timestamp = datetime.now().strftime("%H:%M:%S")
    history.append(f"[{timestamp}] {expr} = {result}")

def show_history():
    win = ctk.CTkToplevel(app)
    win.title("History")
    win.geometry("300x400")
    box = ctk.CTkTextbox(win)
    box.pack(fill="both", expand=True)
    box.insert("end", "\n".join(history))

# ==================== MEMORY ====================
def memory_add():
    global memory
    try: memory += float(expression)
    except: pass

def memory_sub():
    global memory
    try: memory -= float(expression)
    except: pass

def memory_recall():
    press(str(memory))

def memory_clear():
    global memory
    memory = 0

# ==================== STATS ====================
def stats_mean():
    try:
        nums = list(map(float, expression.split(",")))
        set_result(statistics.mean(nums))
    except:
        update_display("Stats Err")

def stats_std():
    try:
        nums = list(map(float, expression.split(",")))
        set_result(statistics.stdev(nums))
    except:
        update_display("Stats Err")

# ==================== CONVERSIONS ====================
def meters_to_feet():
    try:
        set_result(float(expression) * 3.28084)
    except:
        update_display("Err")

def kg_to_lb():
    try:
        set_result(float(expression) * 2.20462)
    except:
        update_display("Err")

def set_result(val):
    global expression
    expression = str(val)
    update_display()

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

# ==================== BUTTON STYLE ====================
def make_btn(parent, text, cmd, bg, row, col, colspan=1):
    btn = ctk.CTkButton(
        parent,
        text=text,
        command=cmd,
        width=70,
        height=70,
        corner_radius=35,
        fg_color=bg,
        hover_color=bg,
        text_color="white",
        font=("Helvetica Neue", 20)
    )
    btn.grid(row=row, column=col, columnspan=colspan, padx=6, pady=6, sticky="nsew")

# ==================== FRAMES ====================
main_frame = ctk.CTkFrame(app, fg_color="#000000")
main_frame.pack()

adv_frame = ctk.CTkFrame(app, fg_color="#000000")

# Grid config
for f in [main_frame, adv_frame]:
    for i in range(6):
        f.grid_rowconfigure(i, weight=1)
    for i in range(4):
        f.grid_columnconfigure(i, weight=1)

# Colors
GRAY = "#a5a5a5"
DARK = "#333333"
ORANGE = "#ff9500"

# ==================== STANDARD ====================
std_buttons = [
    ("AC", clear, GRAY), ("⌫", backspace, GRAY), ("Mode", lambda: toggle_mode(), GRAY), ("÷", lambda: press("/"), ORANGE),
    ("7", lambda: press("7"), DARK), ("8", lambda: press("8"), DARK), ("9", lambda: press("9"), DARK), ("×", lambda: press("*"), ORANGE),
    ("4", lambda: press("4"), DARK), ("5", lambda: press("5"), DARK), ("6", lambda: press("6"), DARK), ("−", lambda: press("-"), ORANGE),
    ("1", lambda: press("1"), DARK), ("2", lambda: press("2"), DARK), ("3", lambda: press("3"), DARK), ("+", lambda: press("+"), ORANGE),
]

for i, (t, c, col) in enumerate(std_buttons):
    make_btn(main_frame, t, c, col, i//4, i%4)

make_btn(main_frame, "0", lambda: press("0"), DARK, 4, 0, 2)
make_btn(main_frame, ".", lambda: press("."), DARK, 4, 2)
make_btn(main_frame, "=", calculate, ORANGE, 4, 3)

# ==================== ADVANCED ====================
adv_buttons = [
    ("sin", lambda: press("sin(")), ("cos", lambda: press("cos(")),
    ("tan", lambda: press("tan(")), ("√", lambda: press("sqrt(")),
    ("log", lambda: press("log(")), ("π", lambda: press("pi")),
    ("e", lambda: press("e")), ("^", lambda: press("**")),
    ("M+", memory_add), ("M-", memory_sub),
    ("MR", memory_recall), ("MC", memory_clear),
    ("mean", stats_mean), ("std", stats_std),
    ("m→ft", meters_to_feet), ("kg→lb", kg_to_lb),
    ("Hist", show_history), ("Back", lambda: toggle_mode())
]

for i, item in enumerate(adv_buttons):
    if len(item) == 2:
        t, c = item
        make_btn(adv_frame, t, c, DARK, i//4, i%4)

# ==================== MODE SWITCH ====================
def toggle_mode():
    global advanced_mode
    advanced_mode = not advanced_mode

    if advanced_mode:
        main_frame.pack_forget()
        adv_frame.pack()
    else:
        adv_frame.pack_forget()
        main_frame.pack()

# ==================== RUN ====================
app.mainloop()
