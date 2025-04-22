# MathMe v1.2 20250416.04:17
import math
import random
import tkinter as tk
from tkinter import messagebox
import math_me_logger
from math_me_logger import log_error, log_debug

def with_logging(fn):
    def wrapper():
        value_str = display.get().strip()
        log_debug(f"{fn.__name__} called with input: {value_str}")
        try:
            result = fn(value_str)
            display.delete(0, tk.END)
            display.insert(0, result)
            log_debug(f"{fn.__name__} result: {result}")
        except Exception as e:
            log_error(f"{fn.__name__} error with input '{value_str}': {e}")
            messagebox.showerror("Error", f"Invalid input: {fn.__name__.split('_')[0]}")
    return wrapper

def process_single_operand(operation):
    value_str = display.get().strip()
    num = float(value_str)
    return operation(num)

@with_logging
def sin_func(value_str):
    return math.sin(float(value_str))

@with_logging
def cos_func(value_str):
    return math.cos(float(value_str))

@with_logging
def tan_func(value_str):
    return math.tan(float(value_str))

@with_logging
def log10_func(value_str):
    return math.log10(float(value_str))

@with_logging
def ln_func(value_str):
    return math.log(float(value_str))

@with_logging
def sqrt_func(value_str):
    num = float(value_str)
    if num < 0:
        raise ValueError("Negative number for square root")
    return math.sqrt(num)

@with_logging
def square_func(value_str):
    return float(value_str) ** 2

@with_logging
def reciprocal_func(value_str):
    num = float(value_str)
    if num == 0:
        raise ZeroDivisionError("Division by zero")
    return 1 / num

@with_logging
def factorial_func(value_str):
    num = int(float(value_str))
    if num < 0:
        raise ValueError("Negative number for factorial")
    return math.factorial(num)

@with_logging
def percent_func(value_str):
    return float(value_str) / 100

def insert_current_value(val):
    try:
        log_debug(f"insert_current_value called with {val}")
        display.insert(tk.END, val)
        log_debug(f"Inserted: {val}")
    except Exception as e:
        log_error(f"insert_current_value error: {e}")
        messagebox.showerror("Error", f"Failed to insert {val}")

def insert_pi():
    insert_current_value(math.pi)

def insert_e():
    insert_current_value(math.e)

def random_number_func():
    try:
        log_debug("random_number_func called")
        number = random.random()
        display.delete(0, tk.END)
        display.insert(0, number)
        log_debug(f"Random number generated: {number}")
    except Exception as e:
        log_error(f"random_number_func error: {e}")
        messagebox.showerror("Error", "Failed to generate random number")

def insert_decimal():
    try:
        log_debug("insert_decimal called")
        display.insert(tk.END, '.')
    except Exception as e:
        log_error(f"insert_decimal error: {e}")
        messagebox.showerror("Error", "Failed to insert decimal point")

def clear_display():
    try:
        log_debug("clear_display called")
        display.delete(0, tk.END)
    except Exception as e:
        log_error(f"clear_display error: {e}")
        messagebox.showerror("Error", "Failed to clear display")

def backspace():
    try:
        current_text = display.get()
        log_debug(f"backspace called, current_text='{current_text}'")
        new_text = current_text[:-1]
        display.delete(0, tk.END)
        display.insert(0, new_text)
        log_debug(f"After backspace, new_text='{new_text}'")
    except Exception as e:
        log_error(f"backspace error: {e}")
        messagebox.showerror("Error", "Failed to delete last character")

def num_button_click(val):
    try:
        log_debug(f"num_button_click called with value: {val}")
        if val == '=':
            expression = display.get()
            log_debug(f"Evaluating expression: {expression}")
            try:
                # It might be safer to limit eval's scope in production code.
                result = eval(expression)
                log_debug(f"Result of '{expression}' = {result}")
                display.delete(0, tk.END)
                display.insert(0, result)
            except Exception as eval_e:
                log_error(f"Error evaluating expression '{expression}': {eval_e}")
                messagebox.showerror("Error", "Invalid expression")
        else:
            display.insert(tk.END, val)
    except Exception as e:
        log_error(f"num_button_click error with value '{val}': {e}")
        messagebox.showerror("Error", "Failed to process button click")

root = tk.Tk()
root.configure(bg='black')
root.title("MathMe")

try:
    icon = tk.PhotoImage(file="/bin/Python/Math_Me/math-me_icon.png")
    root.iconphoto(False, icon)
except Exception as e:
    log_error(f"Failed to load icon: {e}")

display = tk.Entry(root, width=40, font=('Arial', 20), bg='black', fg='white',
                   borderwidth=5, relief=tk.RIDGE, justify='right')
display.grid(row=0, column=0, columnspan=9, padx=5, pady=5)

def bind_enter_key(event):
    num_button_click('=')

root.bind('<Return>', bind_enter_key)
root.bind('<KP_Enter>', bind_enter_key)

sci_buttons = {
    'sin': sin_func,
    'cos': cos_func,
    'tan': tan_func,
    'log': log10_func,
    '%': percent_func,
    'ln': ln_func,
    '√': sqrt_func,
    'x²': square_func,
    '1/x': reciprocal_func,
    'π': insert_pi,
    'e': insert_e,
    'Rnd': random_number_func,
    '!': factorial_func,
    'C': clear_display,
    '⌫': backspace
}

row_index = 1
col_index = 0
for key, func in sci_buttons.items():
    log_debug(f"Creating button '{key}' at row {row_index}, column {col_index}")
    btn = tk.Button(root, text=key, width=4, height=1,
                    bg='black', fg='white', font=('Arial', 12),
                    command=func)
    btn.grid(row=row_index, column=col_index, padx=2)
    col_index += 1
    if col_index > 4:
        col_index = 0
        row_index += 1

num_buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

for r, row_vals in enumerate(num_buttons):
    for c, val in enumerate(row_vals):
        log_debug(f"Creating number pad button '{val}' at row {r+1}, column {c+5}")
        btn = tk.Button(root, text=val, width=4, height=1,
                        bg='black', fg='white', font=('Arial', 12),
                        command=lambda v=val: num_button_click(v))
        btn.grid(row=r+1, column=c+5, padx=2, pady=2)

log_debug("Application started")
root.mainloop()
