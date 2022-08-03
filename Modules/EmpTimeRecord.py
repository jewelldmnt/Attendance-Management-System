from tkinter import *
from customtkinter import *
from . import MenuFrame
from Database import TimeRecord


class EmpTimeRecord(MenuFrame.MenuFrame):
    def __init__(self, parent, controller) -> None:
        MenuFrame.MenuFrame.__init__(self, parent, controller)
        self.configure_frame()

        self.mf = CTkFrame(self, fg_color="#F5F5F5", bg_color="#101B3A")
        self.mf.place(x=35, y=340)


    # configure time record frame
    def configure_frame(self) -> None:
        # configure background image
        self.background_img = PhotoImage(file="Assets/bg_tr.png")
        self.canvas.create_image(595.0, 340.0, image=self.background_img)

        # configure attendance button
        self.img_attendance = PhotoImage(file="Assets/btn_att_orange.png")
        self.btn_attendance["image"] = self.img_attendance
        self.btn_attendance.place_configure(y=235, height=50)
        
        # configure time record button
        self.img_time_rec = PhotoImage(file="Assets/btn_time_rec_red.png")
        self.btn_time_rec["image"] = self.img_time_rec
        self.btn_time_rec.place_configure(y=232, height=55)

        # configure leave request button
        self.img_leave_req = PhotoImage(file="Assets/btn_leave_req_orange.png")
        self.btn_leave_req["image"] = self.img_leave_req
        self.btn_leave_req.place_configure(y=235, height=50)
        

    # update the name and id part
    def update_name_and_id(self) -> None:
        # configure employee name and id
        self.emp_name["text"] = MenuFrame.emp_name
        self.emp_id["text"] = f"EMPLOYEE ID. {MenuFrame.emp_id}"
    

    # creating the record table part
    def create_record_table(self) -> None:
        # making the table frame
        self.frame = Frame(self.mf, bg="#F5F5F5")
        self.frame.grid(row=0, column=0, padx=2, pady=2)
        self.frame.rowconfigure(0, minsize=6)

        # frame to have space to the top
        self.top_part = Frame(self.frame, width=1055, height=120, bg="#F5F5F5")
        self.top_part.grid(row=1, column=0)
        self.create_classification_part()

        # making the canvas for the scrollbar
        self.table_canvas = Canvas(self.frame, width=1055, height=168, bg="#F5F5F5", highlightthickness=0)
        self.table_canvas.grid(row=2, column=0, padx=(50, 0), pady=(5, 10))

        # making the scrollbar of the canvas
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL, command=self.table_canvas.yview)
        self.scrollbar.grid(row=1, column=5, sticky="nse", rowspan=2)
        
        # configuring the canvas scrollbar properties
        self.table_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.table_canvas.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))

        # making a window inside a canvas in the main frame
        self.table_frame = Frame(self.table_canvas, width=1055, height=320, bg="#F5F5F5")
        self.table_canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # changing the month
        TimeRecord.change_month(self.label_month)

        # creating table part
        TimeRecord.create_record_info(self.table_frame, MenuFrame.emp_id)


    # create the classification on the top part
    def create_classification_part(self) -> None:
        self.label_month = CTkLabel(self.top_part, text="", text_font=("Montserrat Bold", -24), 
                                    bg_color="#F5F5F5", fg_color="#26408B", width=1010, height=45)
        self.label_month.grid(row=0, column=0, columnspan=7, pady=8)
        date = CTkLabel(self.top_part, text="DATE", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=170, height=56)
        date.grid(row=1, column=0)
        work_sched = CTkLabel(self.top_part, text="WORK SCHED", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=170, height=56)
        work_sched.grid(row=1, column=1)
        timein = CTkLabel(self.top_part, text="TIME IN", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=126, height=56)
        timein.grid(row=1, column=2)
        timeout = CTkLabel(self.top_part, text="TIME OUT", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=126, height=56)
        timeout.grid(row=1, column=3)
        tardiness = CTkLabel(self.top_part, text="TARDINESS", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=126, height=56)
        tardiness.grid(row=1, column=4)
        overtime = CTkLabel(self.top_part, text="OVERTIME", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=126, height=56)
        overtime.grid(row=1, column=5)
        undertime = CTkLabel(self.top_part, text="UNDERTIME", text_font=("Montserrat Bold", -16), text_color="#101B3A",
                        fg_color="#A6AFD5", bg_color="#F5F5F5", width=126, height=56)
        undertime.grid(row=1, column=6)
