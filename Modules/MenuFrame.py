from tkinter import *
from customtkinter import *

emp_name = ""
emp_id = ""

# base class for the menus of all tabs
class MenuFrame(Frame):
    def __init__(self, parent, controller) -> None:
        Frame.__init__(self, parent)
        self.configure(bg="#26408B")

        # sign in canvas
        self.canvas = Canvas(self, bg="#8F98BB", height = 680, width = 1190, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x=0, y=0)

        # background image
        self.background_img = PhotoImage(file="Assets/bg_em_att.png")
        self.canvas.create_image(595.0, 340.0, image=self.background_img)

        # employee profile
        self.img_profile = PhotoImage(file="Assets/img_profile.png")
        self.emp_profile = Label(self, image=self.img_profile, bg="#26408B")
        self.emp_profile.place(x=150, y=28)

        # employee name
        self.emp_name = Label(self, text="", font=("Montserrat Bold", -40), fg="#F5F5F5", bg="#26408B")
        self.emp_name.place(x=370, y=85)

        # employee id
        self.emp_id = Label(self, text="", font=("Montserrat Regular", -16), fg="#DDE8EA", bg="#26408B")
        self.emp_id.place(x=370, y=137)

        # sign out button
        self.img_signout = PhotoImage(file="Assets/btn_signout.png")
        self.btn_signout = Button(self, image=self.img_signout, borderwidth=0, highlightthickness=0,
                        command=lambda: self.return_to_homepage(controller), relief="flat")
        self.btn_signout.place(x=1010, y=21, width=167, height=64)

        # attendance button
        self.img_attendance = PhotoImage(file="Assets/btn_att_red.png")
        self.btn_attendance = Button(self, image=self.img_attendance, borderwidth=0, highlightthickness=0,
                        command=lambda: self.show_attendance(controller), relief="flat")
        self.btn_attendance.place(x=0, y=232, width=394, height=55)

        # time record button
        self.img_time_rec = PhotoImage(file="Assets/btn_time_rec_orange.png")
        self.btn_time_rec = Button(self, image=self.img_time_rec, borderwidth=0, highlightthickness=0, 
                        command=lambda: self.show_time_record(controller), relief="flat")
        self.btn_time_rec.place(x=398, y=235, width=394, height=50)

        # leave request button
        self.img_leave_req = PhotoImage(file="Assets/btn_leave_req_orange.png")
        self.btn_leave_req = Button(self, image=self.img_leave_req, borderwidth=0, highlightthickness=0, 
                        command=lambda: self.show_leave_request(controller), relief="flat")
        self.btn_leave_req.place(x=796, y=235, width=394, height=50)

        # view employees button
        self.img_view_emp = PhotoImage(file="Assets/btn_view_emp_red.png")
        self.btn_view_emp = Button(self, image=self.img_view_emp, borderwidth=0, highlightthickness=0, 
                        command=lambda: self.show_view_employees(controller), relief="flat")

        # approval request button
        self.img_approval = PhotoImage(file="Assets/btn_approval_orange.png")
        self.btn_approval = Button(self, image=self.img_approval, borderwidth=0, highlightthickness=0, 
                        command=lambda: self.show_approval_request(controller), relief="flat")


    # return to home page
    def return_to_homepage(self, controller):
        controller.show_frame("HomePage")


    # show attendance tab
    def show_attendance(self, controller):
        controller.show_frame("EmpAttendance")


    # show time record tab
    def show_time_record(self, controller):
        controller.frames["EmpTimeRecord"].update_name_and_id()
        controller.frames["EmpTimeRecord"].create_record_table()
        controller.show_frame("EmpTimeRecord")


    # show leave request tab
    def show_leave_request(self, controller):
        controller.frames["EmpLeaveRequest"].update_name_and_id()
        controller.frames["EmpLeaveRequest"].check_have_req()
        controller.show_frame("EmpLeaveRequest")

    
    # show view employees tab
    def show_view_employees(self, controller):
        controller.frames["AdmViewEmployees"].create_employees_table()
        controller.show_frame("AdmViewEmployees")


    # show approval request tab
    def show_approval_request(self, controller):
        controller.frames["AdmApprRequest"].update_name_and_id()
        controller.frames["AdmApprRequest"].create_requests_table()
        controller.show_frame("AdmApprRequest")
