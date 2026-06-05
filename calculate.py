
import tkinter as tk

def press_key(char):
    
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + str(char))

def clear():
    entry.delete(0, tk.END)
    entry.insert(tk.END, "0")

def calculate():
    try:
        expression = entry.get()
        
         
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")


root = tk.Tk()
root.title("Калькулятор")
root.geometry("300x400")
root.resizable(False, False)

entry = tk.Entry(root, font=("Arial", 20), justify="right", bd=10, insertwidth=4, width=14)
entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
entry.insert(0, "0")

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

btn_frame = tk.Frame(root)
btn_frame.pack()

i = 0
for row in range(4):
    for col in range(4):
        text = buttons[i]
        if text == '=':
            action = calculate
        else:
            action = lambda x=text: press_key(x) if entry.get() != "0" or x in ['+', '-', '*', '/', '.'] else [entry.delete(0, tk.END), entry.insert(tk.END, x)]
            
        tk.Button(btn_frame, text=text, font=("Arial", 14), width=5, height=2, command=action).grid(row=row, column=col, padx=5, pady=5)
        i += 1


tk.Button(root, text="C", font=("Arial", 14), width=23, height=1, command=clear).pack(pady=5)

root.mainloop()




