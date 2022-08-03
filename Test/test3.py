from tkinter import *
from customtkinter import *
from tkcalendar import DateEntry
from datetime import datetime, date

set_appearance_mode("System")  # Modes: system (default), light, dark
set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = CTk()
root.geometry("500x500")

m = datetime.today().month
y = datetime.today().year

for d in range(1, 32):
    print(datetime(y, m, d).date())

print(datetime.today().day)

root.mainloop()