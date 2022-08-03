from tkinter import *
from customtkinter import *
from . import TimeRecord, DateManip
from datetime import datetime


# print table of all employees
def create_emp_records(frame) -> None:
    # get the names, ids, and attendance info of all emp
    names = get_names()
    ids = get_ids()
    info = get_employees_info(ids)
    for i, (id, name) in enumerate(zip(ids, names)):
        # get attendance data of the employee
        data = check_empatt_info(id, info)
        # make all the label boxes of the table
        name_box = CTkLabel(frame, text=name, text_font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=214, height=56)
        name_box.grid(row=i, column=0, padx=(0, 9), pady=(0, 5))
        absent_box = CTkLabel(frame, text=str(data[0]), text_font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=125, height=56)
        absent_box.grid(row=i, column=1, padx=(0, 7), pady=(0, 5))
        tardiness_box = CTkLabel(frame, text=str(data[1]), text_font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=125, height=56)
        tardiness_box.grid(row=i, column=2, padx=(0, 7), pady=(0, 5))
        overtime_box = CTkLabel(frame, text=str(data[2]), text_font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=125, height=56)
        overtime_box.grid(row=i, column=3, padx=(0, 6), pady=(0, 5))
        undertime_box = CTkLabel(frame, text=str(data[3]), text_font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=125, height=56)
        undertime_box.grid(row=i, column=4, padx=(0, 5), pady=(0, 5))


# get all info of all employees
def get_employees_info(ids) -> dict:
    return {id:TimeRecord.get_datetime_info(id) for id in ids}
    

# get all id's
def get_ids() -> list:
    with open("Database/Attendance.txt", "r") as file:
        return list(x.split(",")[0] for x in file)


# get all names
def get_names() -> list:
    with open("Database/Attendance.txt", "r") as file:
        return list(x.split(",")[1].split("|")[0] for x in file)


# check employee attendance information
def check_empatt_info(id, info) -> list:
    abs, tds, ots, uts = 0, 0, 0, 0     # no. of absents, tardiness, overtime, and undertime
    dty = DateManip.get_date_today()    # the date today
    m = dty.month                       # the month today
    y = dty.year                        # the year today
    d = dty.day                         # the day today
    for dy in range(1, d+1):
        dt = datetime(y, m, dy).date()  # date
        sdt = dt.strftime("%m-%d-%Y")   # string version of date

        if dt.weekday() in [5, 6]: continue

        # there is a login in that date
        if info[id] != None and sdt in info[id].keys():
            ab = TimeRecord.solve_absent(info[id][sdt][0])
            if ab == "ABSENT":
                abs += 1
            else:
                td = TimeRecord.solve_tardiness(info[id][sdt][0])
                if td != "00:00": tds +=1
                if len(info[id][sdt]) == 2:
                    ot = TimeRecord.solve_overtime(info[id][sdt][1])
                    ut = TimeRecord.solve_undertime(info[id][sdt][1])
                    if ot != "00:00": ots += 1
                    elif ut != "00:00": uts += 1
            continue

        # if there is no current day, and if date today in the loop, and timespan is above 2hrs, add absent
        if info[id] == None or not sdt in info[id].keys():
            if dt != dty or TimeRecord.solve_absent(DateManip.get_strtime_today()) == "ABSENT":
                abs += 1
        
    return [abs, tds, ots, uts]