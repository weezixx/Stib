import tkinter as tk

import time

def clock():
    now = time.strftime("%H:%M:%S")
    label.configure(text=now)
    root.after(1000, clock)


root = tk.Tk()

label = tk.Label(text="", font=('Helvetica', 48), fg='red')
label.pack()
clock()
root.mainloop() # the window is now displayed