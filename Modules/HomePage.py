from tkinter import *
from customtkinter import *

class HomePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # homepage canvas
        canvas = Canvas(self, bg="#101B3A", height=680, width=1190, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # background image
        self.background_img = PhotoImage(file="Assets/bg_hp.png")
        canvas.create_image(595.0, 340.0, image=self.background_img)

        # getting started button
        self.btn_start = PhotoImage(file="Assets/btn_start.png")
        btn_start = Button(canvas, image=self.btn_start, borderwidth=0, highlightthickness=0, 
                        command=lambda: controller.show_frame("SignInPage"), relief="flat")
        btn_start.place(x=270, y=448, width=194.0, height=64.0)
