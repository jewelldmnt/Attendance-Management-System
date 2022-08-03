from tkinter import *
from customtkinter import *

set_appearance_mode("System")  # Modes: system (default), light, dark
set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

def clear():
    print(entry.get())
    entry.delete(0, END)

app = CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

entry = CTkEntry(app, placeholder_text="Enter something here")
entry.pack()

button = CTkButton(app, text="Clear entry", command=clear)
button.pack()

label = CTkLabel(app, text="Date:", text_font=("Montserrat", -15))
label.pack()

app.mainloop()
