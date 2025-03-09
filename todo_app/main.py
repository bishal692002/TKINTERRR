# main.py - Main entry point for the To-Do application

import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import messagebox

from todo_app import ToDoApp

if __name__ == "__main__":
    try:
        # Try to import ttkthemes for a more modern look
        root = ThemedTk(theme="arc")
    except:
        # Fallback to standard Tk
        root = tk.Tk()
        messagebox.showinfo("Info", "For a better UI experience, install ttkthemes:\npip install ttkthemes")
    
    app = ToDoApp(root)
    root.mainloop()