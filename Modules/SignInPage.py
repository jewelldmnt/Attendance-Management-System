from tkinter import *
from customtkinter import *
from Database import AccountCheck as check, Attendance
from . import MenuFrame


# global variables
admin_id = {"1919": ["k", "Head Manager"], "0606": ["z", "Chief Executive Officer"]}

class SignInPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg="#DDE8EA")

        # sign in canvas
        canvas = Canvas(self, bg = "#101B3A", height = 680, width = 1190, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x=0, y=0)

        # background image
        self.background_img = PhotoImage(file="Assets/bg_sip.png")
        canvas.create_image(595.0, 342.0, image=self.background_img)

        # login button
        self.img_login = PhotoImage(file="Assets/btn_login.png")
        btn_login = Button(canvas, image=self.img_login, borderwidth=0, highlightthickness=0, 
                        command=lambda: self.login(controller), relief="flat")
        btn_login.place(x=519.0, y=541.0, width=155.0, height=50.0)

        # email entry and error message
        self.var_email = StringVar()
        self.var_email.trace("w", self.reset_email_error)
        self.entry_email = CTkEntry(self, textvariable=self.var_email, text_color="Black", border_width=1, 
                            border_color="#DDE8EA", fg_color="#DDE8EA", bg_color="#26408B", corner_radius=20)
        self.entry_email.place(x=445.0, y=357.0, width=300.0, height=45.0)
        self.error_email = Label(self, text="", font=("LexendDeca", -12), fg="#FF2F36", bg="#26408B")
        self.error_email.place(x=456, y=407, height=9)

        # password entry error message
        self.var_password = StringVar()
        self.var_password.trace("w", self.reset_password_error) 
        self.entry_password = CTkEntry(self, textvariable=self.var_password, show="*", text_color="Black", border_width=1, 
                            border_color="#DDE8EA", fg_color="#DDE8EA", bg_color="#26408B", corner_radius=20)
        self.entry_password.place(x=445.0, y=460.0, width=300.0, height=45.0)
        self.error_password = Label(self, text="", font=("LexendDeca", -12), fg="#FF2F36", bg="#26408B")
        self.error_password.place(x=456, y=510, height=9)

        # show/hide password button
        self.count = 0
        self.img_show = PhotoImage(file="Assets/btn_show.png")
        self.img_hide = PhotoImage(file="Assets/btn_hide.png")
        self.btn_show_hide = Button(self, image=self.img_show, borderwidth=0, highlightthickness=0,
                            command=self.show_or_hide_pass, relief="flat")
        self.btn_show_hide.place(x=700.0, y=472.0, width=28, height=23)


    # show or hide password
    def show_or_hide_pass(self):
        if self.count == 0:
            self.btn_show_hide["image"] = self.img_hide
            self.entry_password.config(show="")
        else:
            self.btn_show_hide["image"] = self.img_show
            if self.entry_password.get() != "":
                self.entry_password.config(show="*")
                
        self.count = 1 if self.count == 0 else 0


    # login button clicked
    def login(self, controller):
        email = self.entry_email.get()
        password = self.entry_password.get()
        self.clear_entries()

        # checking empty entries
        if email == password == "":
            self.entry_email.config(border_color="Red")
            self.entry_password.config(border_color="Red")
            self.error_email["text"] = self.error_password["text"] = "This field is required!"
        elif email == "":
            self.entry_email.configure(border_color="Red")
            self.error_email["text"] = "This field is required!"
        elif password == "":
            self.entry_password.configure(border_color="Red")
            self.error_password["text"] = "This field is required!"
        else:
            self.check_signin(email, password, controller)


    # checking sign in attempt
    def check_signin(self, em, pwd, controller):
        ret = check.signin(em, pwd)

        if ret == "Account does not exist":
            self.entry_email.configure(border_color="Red")
            self.error_email["text"] = "Account does not exist!"
        elif ret == "Incorrect Password":
            self.entry_password.configure(border_color="Red")
            self.error_password["text"] = "Incorrect Password!"
        elif ret in ["1919", "0606"]:
            self.admin_signin(controller, ret)
        else: 
            self.employee_signin(controller, ret)


    # admin sign in
    def admin_signin(self, controller, id):
        MenuFrame.emp_name = admin_id[id][0]
        MenuFrame.emp_id = admin_id[id][1]
        controller.frames["AdmViewEmployees"].update_name_and_id()
        controller.frames["AdmViewEmployees"].create_employees_table()
        controller.show_frame("AdmViewEmployees")


    # employee sign in
    def employee_signin(self, controller, id):
        # reset daily logins of everyone if new day
        if Attendance.is_new_day():
            Attendance.reset_daily_login()
            Attendance.reset_timeout()
        
        # check if logged user have not yet logged in
        if Attendance.have_daily_login(id):
            controller.frames["EmpAttendance"].record_timein(id)
        else:
            controller.frames["EmpAttendance"].logged_timein(id)

        # change name and id to the one who logged in
        controller.frames["EmpAttendance"].change_info(id)
        controller.show_frame("EmpAttendance")


    # clear entries
    def clear_entries(self):
        self.entry_email.delete(0, END)
        self.entry_password.delete(0, END)


    # resets email border and error
    def reset_email_error(self, *_):
        self.entry_email.configure(border_color="#DDE8EA")
        self.error_email.configure(text="")


    # resets password border and error
    def reset_password_error(self, *_):
        self.entry_password.configure(border_color="#DDE8EA")
        self.error_password.configure(text="")    
