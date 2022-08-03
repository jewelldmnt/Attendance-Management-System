from tkinter import *
from Modules import SignInPage, HomePage, EmpAttendance, EmpTimeRecord, EmpLeaveRequest, AdmApprRequest, AdmViewEmployees

# mainframe class
class Mainframe(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        app_w = 1190
        app_h = 680
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w/2) - (app_w/2)
        y = (screen_h/2) - (app_h/2)

        self.title("Attendance Management Application")
        self.geometry(f"{app_w}x{app_h}+{int(x)}+{int(y)}")
        self.resizable(0, 0)

        # main container of all pages
        mainframe = Frame(self)
        mainframe.pack(fill=BOTH, expand=True)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        # creating the pages
        self.frames = {}
        for f in {HomePage.HomePage, SignInPage.SignInPage, EmpAttendance.EmpAttendance,
                EmpTimeRecord.EmpTimeRecord, EmpLeaveRequest.EmpLeaveRequest, 
                AdmApprRequest.AdmApprRequest, AdmViewEmployees.AdmViewEmployees}:
            page_name = f.__name__
            page = f(mainframe, self)
            page.grid(row=0, column=0, sticky="NSEW")
            self.frames[page_name] = page
        self.show_frame("SignInPage")


    # for calling the frames
    def show_frame(self, page_name):
        self.frames[page_name].tkraise()


# initialize the main window
window = Mainframe()
window.mainloop()
