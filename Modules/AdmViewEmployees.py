from tkinter import *
from customtkinter import *
from . import MenuFrame
from Database import TimeRecord, ViewEmployees

class AdmViewEmployees(MenuFrame.MenuFrame):
    def __init__(self, parent, controller) -> None:
        MenuFrame.MenuFrame.__init__(self, parent, controller)
        self.configure_frame()
        
        self.mf = CTkFrame(self, fg_color="#F5F5F5", bg_color="#101B3A")
        self.mf.place(x=213, y=330)


    # configure frame
    def configure_frame(self):
        # configure background image
        self.background_img = PhotoImage(file="Assets/bg_ve.png")
        self.canvas.create_image(595.0, 340.0, image=self.background_img)

        # configure employees buttons
        self.btn_attendance.place_forget()
        self.btn_time_rec.place_forget()
        self.btn_leave_req.place_forget()

        # configure admin buttons
        self.img_view_emp = PhotoImage(file="Assets/btn_view_emp_red.png")
        self.btn_view_emp["image"] = self.img_view_emp
        self.btn_view_emp.place(x=0, y=232, width=593, height=55)
        self.img_approval = PhotoImage(file="Assets/btn_approval_orange.png")
        self.btn_approval["image"] = self.img_approval
        self.btn_approval.place(x=597, y=235, width=593, height=50)


    # update name and id
    def update_name_and_id(self):
        self.emp_name["text"] = MenuFrame.emp_name
        self.emp_id["text"] = MenuFrame.emp_id


    # create tables for employees
    def create_employees_table(self):
        # making the table frame
        self.frame = Frame(self.mf, bg="#F5F5F5")
        self.frame.grid(row=0, column=0, padx=2, pady=2)
        self.frame.rowconfigure(0, minsize=6)

        # frame to have space to the top
        self.top_part = Frame(self.frame, width=764, height=140, bg="#F5F5F5")
        self.top_part.grid(row=1, column=0)
        self.create_classification_part()

        # making the canvas for the scrollbar
        self.table_canvas = Canvas(self.frame, width=764, height=180, bg="#F5F5F5", highlightthickness=0)
        self.table_canvas.grid(row=2, column=0, padx=(22, 0), pady=(5, 10))

        # making the scrollbar of the canvas
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL, command=self.table_canvas.yview)
        self.scrollbar.grid(row=1, column=5, sticky="nse", rowspan=2)
        
        # configuring the canvas scrollbar properties
        self.table_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.table_canvas.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))

        # making a window inside a canvas in the main frame
        self.table_frame = Frame(self.table_canvas, width=764, height=180, bg="#F5F5F5")
        self.table_canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # changing the month
        TimeRecord.change_month(self.label_month)

        # create record table of employees
        ViewEmployees.create_emp_records(self.table_frame)

    
    # create the classification on the top part
    def create_classification_part(self) -> None:
        self.label_month = CTkLabel(self.top_part, text="", text_font=("Montserrat Bold", -24),
                                    bg_color="#F5F5F5", fg_color="#26408B", width=742, height=45)
        self.label_month.grid(row=0, column=0, columnspan=7, pady=8)
        name = CTkLabel(self.top_part, text="NAME", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=214, height=56)
        name.grid(row=1, column=0, padx=3.5)
        absent = CTkLabel(self.top_part, text="ABSENT", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=125, height=56)
        absent.grid(row=1, column=1, padx=3.5)
        tardiness = CTkLabel(self.top_part, text="TARDINESS", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=125, height=56)
        tardiness.grid(row=1, column=2, padx=3.5)
        overtime = CTkLabel(self.top_part, text="OVERTIME", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=125, height=56)
        overtime.grid(row=1, column=3, padx=3)
        undertime = CTkLabel(self.top_part, text="UNDERTIME", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=125, height=56)
        undertime.grid(row=1, column=4, padx=3)