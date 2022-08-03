from tkinter import *
from customtkinter import *
from . import MenuFrame
from Database import Attendance


class EmpAttendance(MenuFrame.MenuFrame):
    def __init__(self, parent, controller):
        MenuFrame.MenuFrame.__init__(self, parent, controller)

        # date 
        self.date = Label(self, text="", font=("Montserrat", -18), fg="#000000", bg="#F5F5F5")
        self.date.place(x=616, y=473)

        # time in
        self.timein = Label(self, text="", font=("Montserrat", -18), fg="#000000", bg="#F5F5F5")
        self.timein.place(x=616, y=508)

        # time out
        self.timeout_txt = Label(self.canvas, text="Time out:", font=("Montserrat Bold", -18), fg="#000000", bg="#F5F5F5")
        self.timeout_txt.place(x=508, y=543)
        self.timeout = Label(self.canvas, text="", font=("Montserrat", -18), fg="#000000", bg="#F5F5F5")
        self.timeout.place(x=616, y=543)

        # confirmation
        self.confirmation = Label(self.canvas, text="", font=("Montserrat", -18), fg="#4E793A", bg="#F5F5F5")
        self.confirmation.place(x=452, y=574)

        # time out button
        self.img_timeout = PhotoImage(file="Assets/btn_timeout.png")
        self.btn_timeout = Button(self.canvas, image=self.img_timeout, borderwidth=0, highlightthickness=0,
                            command=self.record_timeout, relief="flat")


    # changing info
    def change_info(self, id):
        # changing name, id, and profile
        MenuFrame.emp_name = Attendance.get_name(id)
        self.emp_name["text"] = MenuFrame.emp_name
        self.emp_id["text"] = f"EMPLOYEE ID. {id}"
        MenuFrame.emp_id = id


    # already logged in time in
    def logged_timein(self, id):
        # check if already have time out
        if Attendance.have_timeout(id):
            self.confirmation["text"] = ""
            self.btn_timeout.place(x=480, y=533, width=253, height=80)        
        else:
            timeout = Attendance.get_timeout(id)
            self.change_timeout(timeout)

        timein_time = Attendance.get_timein(id)
        self.timein["text"] = timein_time
        MenuFrame.emp_id = id


    # record employee attendance data
    def record_timein(self, id):
        current_date, current_time = Attendance.add_timein(id)
        self.date["text"] = current_date
        self.timein["text"] = current_time
        self.confirmation["text"] = ""
        self.btn_timeout.place(x=480, y=533, width=253, height=80)
        

    # on press time out button
    def record_timeout(self):
        Attendance.change_timeout(MenuFrame.emp_id)
        timeout = Attendance.add_timeout(MenuFrame.emp_id)
        self.change_timeout(timeout)


    # change time out part
    def change_timeout(self, timeout):
        self.timeout["text"] = timeout
        self.confirmation["text"] = "You have successfully timed out."
        self.btn_timeout.place_forget()