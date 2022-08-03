from tkinter import *
from customtkinter import *
from . import MenuFrame, EmpLeaveRequest as emp_lr
from Database import LeaveRequests


class AdmApprRequest(MenuFrame.MenuFrame):
    def __init__(self, parent, controller) -> None:
        MenuFrame.MenuFrame.__init__(self, parent, controller)
        self.configure(bg="#101B3A")
        self.configure_frame()
        
        # no requests
        self.no_req = Label(self, text="No requests", bg="#101B3A", fg="#F5F5F5", font=("Montserrat Bold", -40))

        # frame for all requests
        self.c = 0
        self.req_frames = CTkFrame(self, fg_color="#F5F5F5", bg_color="#101B3A")
        self.req_frames.columnconfigure(0, weight=1)

        # buttons approve and decline
        self.img_approve = PhotoImage(file="Assets/btn_approve.png")
        self.btn_approve = Button(self.req_frames, image=self.img_approve, borderwidth=0, highlightthickness=0, 
                        command=lambda: self.req_verdict("approved"), relief="flat", width=114, height=40)
        self.btn_approve.grid(row=1, column=1, pady=10)

        self.img_decline = PhotoImage(file="Assets/btn_decline.png")
        self.btn_decline = Button(self.req_frames, image=self.img_decline, borderwidth=0, highlightthickness=0, 
                        command=lambda: self.req_verdict("declined"), relief="flat", width=114, height=40)
        self.btn_decline.grid(row=1, column=2, pady=10, padx=(0, 20))

        # next and previous buttons
        self.img_next = PhotoImage(file="Assets/btn_next.png")
        self.btn_next = Button(self, image=self.img_next, borderwidth=0, highlightthickness=0, 
                        command=self.show_next_req, relief="flat")

        self.img_prev = PhotoImage(file="Assets/btn_prev.png")
        self.btn_prev = Button(self, image=self.img_prev, borderwidth=0, highlightthickness=0, 
                        command=self.show_prev_req, relief="flat")


    # configure frame
    def configure_frame(self):
        # configure background image
        self.background_img = PhotoImage(file="Assets/bg_ar.png")
        self.canvas.create_image(595.0, 340.0, image=self.background_img)

        # configure employees buttons
        self.btn_attendance.place_forget()
        self.btn_time_rec.place_forget()
        self.btn_leave_req.place_forget()

        # configure admin buttons
        self.img_view_emp = PhotoImage(file="Assets/btn_view_emp_orange.png")
        self.btn_view_emp["image"] = self.img_view_emp
        self.btn_view_emp.place(x=0, y=235, width=593, height=50)
        self.img_approval = PhotoImage(file="Assets/btn_approval_red.png")
        self.btn_approval["image"] = self.img_approval
        self.btn_approval.place(x=597, y=232, width=593, height=55)


    # update name and id
    def update_name_and_id(self):
        self.emp_name["text"] = MenuFrame.emp_name
        self.emp_id["text"] = MenuFrame.emp_id


    # creating the requests table list
    def create_requests_table(self):
        if LeaveRequests.count() == 0:
            self.no_req.place(x=463, y=456)
            self.req_frames.place_forget()
            self.btn_next.place_forget()
            self.btn_prev.place_forget()
            return
        
        # create frames for the requests list
        if LeaveRequests.count() > 1:
            self.no_req.place_forget()
            self.btn_next.place(x=1104, y=452, width=30, height=60)

        self.req_frames.place(x=175, y=335)
        LeaveRequests.create_requests_list(self.req_frames)


    # show next request
    def show_next_req(self):
        self.c += 1
        LeaveRequests.requests[self.c].tkraise()
        self.btn_prev.place(x=50, y=452, width=30, height=60)
        self.check_index()


    # show previous request
    def show_prev_req(self):
        self.c -= 1
        LeaveRequests.requests[self.c].tkraise()
        self.btn_next.place(x=1104, y=452, width=30, height=60)
        self.check_index()

        
    # approve the request
    def req_verdict(self, verdict):
        emp_id = LeaveRequests.requests[self.c].children["!ctklabel3"].text
        emp_lr.status[emp_id] = verdict
        LeaveRequests.remove_request_frame(self.c, emp_id)
        self.c = 0 if self.c == 0 else self.c-1
        self.check_index()

    
    # check index for next and previous buttons
    def check_index(self):
        if LeaveRequests.count() == 0:
            self.no_req.place(x=463, y=456)
            self.req_frames.place_forget()
            return

        if LeaveRequests.count() == 1:
            self.btn_next.place_forget()
            self.btn_prev.place_forget()
            return

        if self.c == 0:
            self.btn_prev.place_forget()
            self.btn_next.place(x=1104, y=452, width=30, height=60)
            return

        if self.c == LeaveRequests.count()-1:
            self.btn_next.place_forget()
            self.btn_prev.place(x=50, y=452, width=30, height=60)
            return
