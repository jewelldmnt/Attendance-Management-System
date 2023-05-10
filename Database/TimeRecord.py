from tkinter import *
from customtkinter import *
from datetime import datetime, timedelta
from . import DateManip


# dictionary of timeout, overtime, and undertime widgets
boxes = {}

# change label month to current month
def change_month(lbl_month) -> None:
    current_month = DateManip.get_strmonth_today().upper()
    current_year = DateManip.get_stryear_today()
    lbl_month.configure(text=f"SUMMARY OF {current_month} {current_year}")


# create the table part
def create_record_info(frame, id) -> None:
    global boxes
    m = datetime.today().month      # the month today
    y = datetime.today().year       # the year today
    log = get_datetime_info(id)     # the logged dates of the employee

    # table ranging from first day of the month up to current day
    for d in range(1, datetime.today().day + 1):
        dt = datetime(y, m, d).date()                           # date
        sdt = dt.strftime("%m-%d-%Y")                           # string version of date
        worksched, timein, timeout,  = "8:00 - 18:00", "", ""   # default values
        tardiness, overtime, undertime = "", "", ""             # dafault values

        # check conditions for the value of each labels
        if dt.weekday() in [5, 6]:
            worksched = "REST DAY"
            timein = timeout = "-"
            tardiness = overtime = undertime = "00:00"
        elif sdt in log.keys():
            timein = solve_absent(log[sdt][0])
            tardiness = "00:00" if timein == "ABSENT" else solve_tardiness(timein)
        else:
            timein = "ABSENT"

        if timein == "ABSENT":
            timeout = "-"
            tardiness = overtime = undertime = "00:00"

        # make all the label boxes of the table
        date_box = CTkLabel(frame, text=sdt, font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=170, height=51)
        date_box.grid(row=d, column=0, padx=(0, 6), pady=(0, 5))
        work_sched_box = CTkLabel(frame, text=worksched, font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=170, height=51)
        work_sched_box.grid(row=d, column=1, padx=(0, 6), pady=(0, 5))
        timein_box = CTkLabel(frame, text=timein, font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=126, height=51)
        timein_box.grid(row=d, column=2, padx=(0, 5), pady=(0, 5))
        timeout_box = CTkLabel(frame, text=timeout, font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=126, height=51)
        timeout_box.grid(row=d, column=3, padx=(0, 6), pady=(0, 5))
        tardiness_box = CTkLabel(frame, text=tardiness, font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=126, height=51)
        tardiness_box.grid(row=d, column=4, padx=(0, 5), pady=(0, 5))
        overtime_box = CTkLabel(frame, text=overtime, font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=126, height=51)
        overtime_box.grid(row=d, column=5, padx=(0, 6), pady=(0, 5))
        undertime_box = CTkLabel(frame, text=undertime, font=("Montserrat Regular", -16), text_color="#101B3A",
                        fg_color="#D1D5E7", bg_color="#F5F5F5", width=126, height=51)
        undertime_box.grid(row=d, column=6, padx=(0, 5), pady=(0, 5))
        boxes[sdt] = [timeout_box, overtime_box, undertime_box]

        # configure the widgets for timeout, overtime, and undertime
        if timein != "ABSENT" and sdt in log.keys() and len(log[sdt]) == 2:
            timeout = log[sdt][1]
            overtime = solve_overtime(timeout)
            undertime = solve_undertime(timeout)
            boxes[sdt][0].text_label.configure(text=timeout)
            boxes[sdt][1].text_label.configure(text=overtime)
            boxes[sdt][2].text_label.configure(text=undertime)


# get number of dates
def get_no_of_dates(id) -> int:
    return len(get_datetime_info(id))


# get all the date, timein, and timeout of an employee
def get_datetime_info(id) -> dict|None:
    with open("Database/Attendance.txt", "r") as file:
        for row in file:
            _id, info = row.split(",")
            if _id == id: 
                datetime_list = info.split("|")[1].rstrip("\n").split("/")
                if datetime_list == [""]:
                    datetime_list = info.rstrip("\n").split("|")[1]
                break
            
        if datetime_list == [""]:
            return None

        dic = {}
        for datetime in datetime_list:
            d = datetime.split(";")
            if len(d) == 3:
                dic[d[0]] = [d[1], d[2]]
            else:
                dic[d[0]] = [d[1]]
        return dic


# solve absent
def solve_absent(strtime) -> str:
    temp_date1 = datetime.strptime(strtime, "%H:%M")
    temp_date2 = datetime.strptime("8:00", "%H:%M")

    # not late
    if temp_date1 <= temp_date2:
        return strtime
    
    # late by how much time
    t = (temp_date1 - temp_date2)
    if t.seconds // 60 >= 120:
        return "ABSENT"
    else:
        return strtime


# solve tardiness
def solve_tardiness(strtime) -> str:
    temp_date1 = datetime.strptime(strtime, "%H:%M")
    temp_date2 = datetime.strptime("8:00", "%H:%M")

    # not late
    if temp_date1 <= temp_date2:
        return "00:00"
    
    # late by how much time
    t = (temp_date1 - temp_date2)
    if t.seconds // 60 >= 15:
        return (datetime(1, 1, 1) + (t - timedelta(minutes=15))).strftime("%H:%M")
    else:
        return "00:00"


# solve overtime
def solve_overtime(strtime) -> str:
    temp_date1 = datetime.strptime(strtime, "%H:%M")
    temp_date2 = datetime.strptime("18:00", "%H:%M")
    
    # not overtime
    if temp_date1 <= temp_date2:
        return "00:00"

    # overtime by how much time
    t = (temp_date1 - temp_date2)
    if t.seconds // 60 >= 60:
        return (datetime(1, 1, 1) + (t - timedelta(hours=1))).strftime("%H:%M")
    else:
        return "00:00"


# solve undertime
def solve_undertime(strtime) -> str:
    temp_date1 = datetime.strptime(strtime, "%H:%M")
    temp_date2 = datetime.strptime("18:00", "%H:%M")

    # not undertime
    if temp_date1 >= temp_date2:
        return "00:00"

    # undertime by how much time
    t = (temp_date2 - temp_date1)
    if t.seconds // 60 >= 10:
        return (datetime(1, 1, 1) + (t - timedelta(minutes=10))).strftime("%H:%M")
    else:
        return "00:00"
    