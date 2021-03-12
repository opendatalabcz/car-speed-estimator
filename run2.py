import cv2
from src.carSpeedEstimator import *
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk
from PIL import Image
import numpy as np

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Car Speed Estimator")
        self.minsize(640, 400)

        self.labelFrame = ttk.LabelFrame(self, text="Video file")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)

        self.labelFrame2 = ttk.LabelFrame(self, text="Measuring Area")
        self.labelFrame2.grid(column=1, row=1, padx=20, pady=20)

        self.video_button()
        self.start_button()
        self.measuring_param()
        self.rd = False
        self.frame_rd = False

    def create_lines(self):
        s_line_pt1_x = int(self.s_line_pt1_x.get())
        s_line_pt1_y = int(self.s_line_pt1_y.get())
        s_line_pt2_x = int(self.s_line_pt2_x.get())
        s_line_pt2_y = int(self.s_line_pt2_y.get())
        e_line_pt1_x = int(self.e_line_pt1_x.get())
        e_line_pt1_y = int(self.e_line_pt1_y.get())
        e_line_pt2_x = int(self.e_line_pt2_x.get())
        e_line_pt2_y = int(self.e_line_pt2_y.get())
        frame = self.frame_original.copy()
        cv2.line(frame, (s_line_pt1_x, s_line_pt1_y), (s_line_pt2_x, s_line_pt2_y), (0, 255, 0), 2)
        cv2.line(frame, (e_line_pt1_x, e_line_pt1_y), (e_line_pt2_x, e_line_pt2_y), (0, 0, 255), 2)
        self.image = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)

    def run(self):
        if self.rd:
            s_line_pt1_x = int(self.s_line_pt1_x.get())
            s_line_pt1_y = int(self.s_line_pt1_y.get())
            s_line_pt2_x = int(self.s_line_pt2_x.get())
            s_line_pt2_y = int(self.s_line_pt2_y.get())
            e_line_pt1_x = int(self.e_line_pt1_x.get())
            e_line_pt1_y = int(self.e_line_pt1_y.get())
            e_line_pt2_x = int(self.e_line_pt2_x.get())
            e_line_pt2_y = int(self.e_line_pt2_y.get())
            len = int(self.len.get())
            estimator = CarSpeedEstimator(self.cap, [(s_line_pt1_x, s_line_pt1_y), (s_line_pt2_x, s_line_pt2_y)]
                                          , [(e_line_pt1_x, e_line_pt1_y), (e_line_pt2_x, e_line_pt2_y)], len)
            estimator.run()

    def video_button(self):
        self.v_button = ttk.Button(self.labelFrame, text="Browse A File", command=self.fileDialog)
        self.v_button.grid(column=1, row=1)

    def start_button(self):
        self.s_button = Button(self, text="start", command=self.run)
        self.s_button.grid(row=10,column=0)

    def validate(self):
        try:
            int(self.s_line_pt1_x.get())
            int(self.s_line_pt1_y.get())
            int(self.s_line_pt2_x.get())
            int(self.s_line_pt2_y.get())
            int(self.e_line_pt1_x.get())
            int(self.e_line_pt1_y.get())
            int(self.e_line_pt2_x.get())
            int(self.e_line_pt2_y.get())
            int(self.len.get())
            if self.frame_rd:
                self.rd = True
                self.create_lines()
        except ValueError:
            print("bad input")

    def measuring_param(self):
        self.line1_txt = Label(self.labelFrame2, text="Starting Line")
        self.line1_txt.grid(column=0, row=0)
        self.s_line_pt1_x = Entry(self.labelFrame2)
        self.s_line_pt1_x.grid(column=0,row=1)
        self.s_line_pt1_y = Entry(self.labelFrame2)
        self.s_line_pt1_y.grid(column=1, row=1)
        self.s_line_pt2_x = Entry(self.labelFrame2)
        self.s_line_pt2_x.grid(column=0, row=2)
        self.s_line_pt2_y = Entry(self.labelFrame2)
        self.s_line_pt2_y.grid(column=1, row=2)
        self.line2_txt = Label(self.labelFrame2, text="Ending Line")
        self.line2_txt.grid(column=0, row=3)
        self.e_line_pt1_x = Entry(self.labelFrame2)
        self.e_line_pt1_x.grid(column=0,row=4)
        self.e_line_pt1_y = Entry(self.labelFrame2)
        self.e_line_pt1_y.grid(column=1, row=4)
        self.e_line_pt2_x = Entry(self.labelFrame2)
        self.e_line_pt2_x.grid(column=0, row=5)
        self.e_line_pt2_y = Entry(self.labelFrame2)
        self.e_line_pt2_y.grid(column=1, row=5)
        self.len_txt = Label(self.labelFrame2, text="Length")
        self.len_txt.grid(column=0, row=6)
        self.len = Entry(self.labelFrame2)
        self.len.grid(column=1, row=6)
        self.line_button = Button(self.labelFrame2, text="Create Lines", command=self.validate)
        self.line_button.grid(column=0, row=7)

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir="./", title="Select A File", filetypes=
        [("video",".mp4"), ("video", ".avi")])

        self.cap = cv2.VideoCapture(self.filename)
        _, frame = self.cap.read()
        self.frame_original = frame
        self.frame_rd = True
        width = int(self.cap.get(3))
        height = int(self.cap.get(4))
        self.image = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas = tkinter.Canvas(self.labelFrame, width=width, height=height)
        self.canvas.grid(column=1, row=3)
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)

root = Root()
root.mainloop()



