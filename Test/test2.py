from tkinter import *
from customtkinter import *
from datetime import datetime

set_appearance_mode("System")  # Modes: system (default), light, dark
set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = CTk()
app.geometry("400x400")

dates = ["07-01-2022", "07-02-2022", "07-03-2022", "07-04-2022", "07-05-2022", "07-06-2022",
        "07-07-2022", "07-08-2022", "07-09-2022", "07-10-2022", "07-11-2022", "07-12-2022", 
        "07-13-2022", "07-14-2022", "07-15-2022", "07-16-2022", "07-17-2022", "07-18-2022", 
        "07-19-2022", "07-20-2022", "07-21-2022", "07-22-2022", "07-23-2022", "07-24-2022",
        "07-25-2022", "07-26-2022", "07-27-2022", "07-28-2022", "07-29-2022", "07-30-2022", "07-31-2022"] 
counter = 0

def add_date():
    # employee info about name, date, time in, and time out
    emp_info = {}
    with open("Test/attendance_test.txt", "r") as file:
        lines = file.readlines()

    # writing the added info about employee
    with open("Test/attendance_test.txt", "w") as file:
        global counter
        for row in lines:
            _id, info = row.rstrip("\n").split(",")
            # if id is not equal to the passed id
            if _id != "roscoe":
                file.write(row)
                continue

            # making a dictionary with name as the key and the  
            # list of date, time in, and time out as the value  
            name, sched = info.split("|")
            emp_info[name] = []
            if sched != "":
                for _, i in enumerate(sched.split("/")):
                    emp_info[name].append(i.split(";"))

            # if it's a new month, employee info is still empty
            # so add the date today and time in to the dictionary
            temp = f"{_id},{name}|"
            emp_info[name].append([dates[counter], datetime.today().time().strftime("%H:%M")])
            for i in range(len(emp_info[name])):
                temp += emp_info[name][i][0] + ";" + emp_info[name][i][1] + "/"
            
            # rewrite the new employee info into the database
            file.write(temp.rstrip("/") + "\n")
            counter += 1


button = CTkButton(app, text="Login", command=add_date)
button.pack()

app.mainloop()
