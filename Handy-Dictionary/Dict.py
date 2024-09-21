from PyDictionary import PyDictionary
from tkinter import *
from tkinter import ttk

def meanings():
    word = entry.get()
    dictionary=PyDictionary()
    meaning = dictionary.meaning(word)
    if meaning:
        result.set(meaning)
    else:
        result.set("Meaning not found")


root=Tk()
root.geometry("540x360")
root.title("Python-Dictionary")

frame = ttk.Frame(root, padding=10)
frame.grid()

entry=ttk.Entry(frame)
entry.grid(column=0,row=1)

search_button = ttk.Button(frame, text="Search", command=meanings)
search_button.grid(column=1, row=1)

result = StringVar()

result_label = ttk.Label(frame, textvariable=result, wraplength=300)
result_label.grid(column=0, row=2, columnspan=2)

root.mainloop()