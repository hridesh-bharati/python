import tkinter as tk
from tkinter import ttk

def style_widgets():
    # Change ttk button style to look more Bootstrap-like
    style = ttk.Style()
    style.configure("TButton",
                    padding=6,
                    relief="flat",
                    background="#5bc0de",
                    font=("Helvetica", 12))

root = tk.Tk()
root.title("Bootstrap Style in Tkinter")

style_widgets()

button = ttk.Button(root, text="Bootstrap-style Button")
button.pack(padx=10, pady=10)

root.mainloop()
