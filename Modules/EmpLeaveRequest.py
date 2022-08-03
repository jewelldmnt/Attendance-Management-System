from tkinter import *
from tkinter import ttk
from customtkinter import *
from tkcalendar import DateEntry
from Database import DateManip, LeaveRequests
from . import MenuFrame


# global variables
status = {}

# class for changing date entry border
class BorderedDateEntry(DateEntry):
    def __init__(self, root, bordercolor, borderthickness=1, background="#D1D5E7", foreground='black', *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        # Styles must have unique image, element, and style names to create
        # multiple instances. winfo_id() is good enough
        e_id = self.winfo_id()
        img_name = f'entryBorder{e_id}'
        element_name = f'bordercolor{e_id}'
        self.style_name = f'bcEntry{e_id}.DateEntry'
        self.fg = foreground
        self.bd = borderthickness
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.img = PhotoImage(img_name, width=self.width, height=self.height)
        self.img.put(bordercolor, to=(0, 0, self.width, self.height))
        self.img.put(background, to=(borderthickness, borderthickness, self.width - borderthickness, self.height - borderthickness))

        self.style = ttk.Style()
        self.style.element_create(element_name, 'image', img_name, sticky='nsew', border=borderthickness)
        self.style.layout(self.style_name, [(f'Entry.{element_name}', {'children': 
                                    [('Entry.padding', {'children': 
                                        [('Entry.textarea', {'sticky': 'nsew'})], 'sticky': 'nsew'})], 'sticky': 'nsew'})])
        self.style.configure(self.style_name, background=background, foreground=foreground)
        self.config(mindate=DateManip.get_date_today(), font=("Montserrat Regular", 12), width=25, style=self.style_name)


    def configure_entry(self, background="#D1D5E7", _state="normal"):
        self.img.put(background, to=(0, 0, self.width, self.height))
        self.img.put(background, to=(self.bd, self.bd, self.width - 1, self.height - 1))
        self.style.configure(self.style_name, background=background, foreground=self.fg)
        self.config(state=_state)
        

# class for the employee leave request tab frame
class EmpLeaveRequest(MenuFrame.MenuFrame):
    def __init__(self, parent, controller) -> None:
        MenuFrame.MenuFrame.__init__(self, parent, controller)
        self.configure_frame()

        # make the entry for start date
        frame_sd = CTkFrame(self, fg_color="#D1D5E7", bg_color="#F5F5F5")
        frame_sd.place(x=296, y=386)
        self.start_date = BorderedDateEntry(frame_sd, bordercolor="#D1D5E7")
        self.start_date.pack(padx=10)

        # make the entry for end date
        frame_ed = CTkFrame(self, fg_color="#D1D5E7", bg_color="#F5F5F5")
        frame_ed.place(x=704, y=386)
        self.end_date = BorderedDateEntry(frame_ed, bordercolor="#D1D5E7")
        self.end_date.pack(padx=10)

        # make the entry for reason
        frame_reason = CTkFrame(self, fg_color="#D1D5E7", bg_color="#F5F5F5")
        frame_reason.place(x=296, y=427)
        self.text_reason = Text(frame_reason, width=99, height=6, bg="#D1D5E7", bd=0, wrap=WORD, font="Lucida 10")
        self.text_reason.pack(pady=6, padx=6.5)

        # status label
        self.lbl_status = Label(self, text="Status:", bg="#F5F5F5", font=("Montserrat Regular", -16))        
        self.status_img = Label(self)

        # submit button
        self.img_submit = PhotoImage(file="Assets/btn_submit.png")
        self.btn_submit = Button(self.canvas, image=self.img_submit, borderwidth=0, highlightthickness=0,
                        command=self.submit_req, relief="flat")
        self.btn_submit.place(x=880, y=528, width=128, height=55)

        # new request button
        self.img_new_req = PhotoImage(file="Assets/btn_new_req.png")
        self.btn_new_req = Button(self.canvas, image=self.img_new_req, borderwidth=0, highlightthickness=0,
                        command=self.new_request, relief="flat")


    # configure time record frame
    def configure_frame(self) -> None:
        # configure background image
        self.background_img = PhotoImage(file="Assets/bg_lr.png")
        self.canvas.create_image(595.0, 340.0, image=self.background_img)

        # configure attendance button
        self.img_attendance = PhotoImage(file="Assets/btn_att_orange.png")
        self.btn_attendance["image"] = self.img_attendance
        self.btn_attendance.place_configure(y=235, height=50)
        
        # configure time record button
        self.img_time_rec = PhotoImage(file="Assets/btn_time_rec_orange.png")
        self.btn_time_rec["image"] = self.img_time_rec
        self.btn_time_rec.place_configure(y=235, height=50)

        # configure leave request button
        self.img_leave_req = PhotoImage(file="Assets/btn_leave_req_red.png")
        self.btn_leave_req["image"] = self.img_leave_req
        self.btn_leave_req.place_configure(y=232, height=55)


    # update the name and id part
    def update_name_and_id(self) -> None:
        # configure employee name and id
        self.emp_name["text"] = MenuFrame.emp_name
        self.emp_id["text"] = f"EMPLOYEE ID. {MenuFrame.emp_id}"


    # on click submit button
    def submit_req(self):
        status[MenuFrame.emp_id] = "pending"

        # for the status
        self.img_status = PhotoImage(file="Assets/img_pending.png")
        self.status_img["image"] = self.img_status
        self.place_status()

        # disabling the reason and dates
        self.configure_entries("disabled", "gray")

        # record the request
        default_msg = "I want to leave for the time being."
        s = self.start_date.get_date()
        e = self.end_date.get_date()
        r = self.text_reason.get(1.0, END)
        r = default_msg if r == "" else r
        LeaveRequests.record_request(MenuFrame.emp_id, MenuFrame.emp_name, s, e, r)


    # new request button
    def new_request(self):
        LeaveRequests.remove_request(MenuFrame.emp_id)
        LeaveRequests.removed.remove(MenuFrame.emp_id)
        self.reset_to_original()
        

    # check if have request already
    def check_have_req(self):
        self.reset_to_original()

        # if employee already submitted one, output his/her req on screen
        if LeaveRequests.txt_count() > 0:
            r_info = LeaveRequests.get_request_info(MenuFrame.emp_id)
            if r_info != None:
                # place the info to the entries
                start, end = r_info[0].split(";")
                reason = r_info[1]
                self.start_date.set_date(DateManip.convert_to_datetime(start))
                self.end_date.set_date(DateManip.convert_to_datetime(end))
                self.text_reason.insert(INSERT, reason)
                self.configure_entries("disabled", "gray")
                self.check_status()
        

    # check status
    def check_status(self):
        if status[MenuFrame.emp_id] == "approved":
            self.img_status = PhotoImage(file="Assets/img_approved.png")
            self.status_img["image"] = self.img_status
            self.btn_new_req.place(x=473, y=599, width=284, height=55)
        elif status[MenuFrame.emp_id] == "declined":
            self.img_status = PhotoImage(file="Assets/img_declined.png")
            self.status_img["image"] = self.img_status
            self.btn_new_req.place(x=473, y=599, width=284, height=55)
        else:
            self.img_status = PhotoImage(file="Assets/img_pending.png")
            self.status_img["image"] = self.img_status
            
        self.place_status()


    # diable entries
    def configure_entries(self, _state, _fg):
        self.text_reason.configure(state=_state, foreground=_fg)
        self.start_date.configure_entry(_state=_state)
        self.end_date.configure_entry(_state=_state)

    
    # place status label
    def place_status(self):
        self.status_img.place(x=870, y=542)
        self.lbl_status.place(x=803, y=544)
        self.btn_submit.place_forget()


    # reset to orginal
    def reset_to_original(self):
        self.configure_entries("normal", "black")
        self.start_date.set_date(DateManip.get_date_today())
        self.end_date.set_date(DateManip.get_date_today())
        self.text_reason.delete(1.0, END)
        self.status_img.place_forget()
        self.lbl_status.place_forget()
        self.btn_new_req.place_forget()
        self.btn_submit.place(x=880, y=528, width=128, height=55)