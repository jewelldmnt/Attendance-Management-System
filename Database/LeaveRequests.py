from tkinter import *
from customtkinter import *
from . import DateManip
from os import path


# list of all requests frames and renmoved requests
requests = []
removed = []

# record the request
def record_request(id, name, start, end, reason) -> None:
    s = DateManip.convert_to_strdate(start)
    e = DateManip.convert_to_strdate(end)
    duration = s + ";" + e
    with open("Database/LeaveRequests.txt", "a") as file:
        file.write(f"{id}|{name}|{duration}|{reason}")
        # 1004|a|7/20/2022;7/26/2022|I want to leave.


# create frames for the requests list
def create_requests_list(frame) -> None:
    reqs = get_employee_reqs()
    for i in range(count())[::-1]:
        # getting the info
        _id, _name, d, _reason = reqs[i].rstrip("\n").split("|")
        _duration = ' - '.join(x for x in d.split(";"))
        # create the frame of the req
        f = Frame(frame, width=842, height=306, bg="#F5F5F5")
        f.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0))
        # request number part
        req = CTkLabel(f, text=f"Request #{i + 1}", fg_color="#26408B", bg_color="#F5F5F5", width=820,
                        height=36, text_font=("Montserrat Bold", -16), justify=LEFT)
        req.text_label.place(x=10, y=5)
        req.grid(row=1, column=1, columnspan=2, pady=2)
        # employee id part
        id = CTkLabel(f, text="Employee ID.", fg_color="#A6AFD5", bg_color="#F5F5F5", width=150,
                        height=37, text_color="Black", text_font=("Montserrat Bold", -16))
        id.grid(row=2, column=1, pady=2)
        id_bx = CTkLabel(f, text=_id, fg_color="#D1D5E7", bg_color="#F5F5F5", width=661,
                        height=37, text_color="Black", text_font=("Montserrat Regular", -16))
        id_bx.text_label.place(x=10, y=5)
        id_bx.grid(row=2, column=2, padx=(9, 0), pady=2)
        # name part
        nm = CTkLabel(f, text="Name", fg_color="#A6AFD5", bg_color="#F5F5F5", width=150,
                        height=37, text_color="Black", text_font=("Montserrat Bold", -16))
        nm.grid(row=3, column=1, pady=2)
        nm_bx = CTkLabel(f, text=_name, fg_color="#D1D5E7", bg_color="#F5F5F5", width=661,
                        height=37, text_color="Black", text_font=("Montserrat Regular", -16))
        nm_bx.text_label.place(x=10, y=5)
        nm_bx.grid(row=3, column=2, padx=(9, 0), pady=2)
        # duration part
        dur = CTkLabel(f, text="Duration", fg_color="#A6AFD5", bg_color="#F5F5F5", width=150,
                        height=37, text_color="Black", text_font=("Montserrat Bold", -16))
        dur.grid(row=4, column=1, pady=2)
        dur_bx = CTkLabel(f, text=_duration, fg_color="#D1D5E7", bg_color="#F5F5F5", width=661,
                        height=37, text_color="Black", text_font=("Montserrat Regular", -16))
        dur_bx.text_label.place(x=10, y=5)
        dur_bx.grid(row=4, column=2, padx=(9, 0), pady=2)
        # reason part
        rsn = CTkLabel(f, text="Reason", fg_color="#A6AFD5", bg_color="#F5F5F5", width=150,
                        height=74, text_color="Black", text_font=("Montserrat Bold", -16))
        rsn.grid(row=5, column=1, pady=2)
        rsn_fr = CTkFrame(f, fg_color="#D1D5E7", bg_color="#F5F5F5")
        rsn_fr.grid(row=5, column=2, padx=(8, 0), pady=2)
        rsn_bx = Text(rsn_fr, width=58, height=3, bg="#D1D5E7", fg="black", bd=0, wrap=WORD, font=("Montserrat Regular", -16))
        rsn_bx.insert(INSERT, _reason)
        rsn_bx.configure(state="disabled")
        rsn_bx.pack(pady=2, padx=9)
        # store the frame in the list
        requests.append(f)
    # reverse the list
    requests.reverse()


# remove request frame
def remove_request_frame(ind, id) -> None:
    # destroy the frame for the removed request
    requests[ind].destroy()
    requests.pop(ind)
    removed.append(id)
    # adjust numbering of request no.
    for r in range(ind, len(requests)):
        requests[r].children["!ctklabel"].text_label["text"] = f"Request #{ind+1}"
        ind += 1


# remove request of employee
def remove_request(id) -> None:
    with open("Database/LeaveRequests.txt", "r") as file:
        lines = file.readlines()

    # rewriting the leave requests list without the remove request
    with open("Database/LeaveRequests.txt", "w") as file:
        for line in lines:
            _id = line.split("|")[0]
            if id != _id:
                file.write(line)


# get leave requests count in database
def txt_count() -> int:
    with open("Database/LeaveRequests.txt", "r") as file:
        return len(file.readlines())


# count number of requests
def count() -> int:
    count = 0
    if path.getsize("Database/LeaveRequests.txt") == 0:
        return count
    
    # don't count the requests that have already been decided
    with open("Database/LeaveRequests.txt", "r") as file:
        for line in file:
            _id = line.rstrip('\n').split("|")[0]
            if not _id in removed:
                count += 1
        return count

    
# get the request of every employee
def get_employee_reqs() -> list[str]:
    with open("Database/LeaveRequests.txt", "r") as file:
        return file.readlines()


# get the request info of the employee
def get_request_info(id) -> list|None:
    with open("Database/LeaveRequests.txt", "r") as file:
        for line in file:
            _id, _, duration, reason = line.rstrip("\n").split("|")
            if _id == id:
                return [duration, reason]
    return None