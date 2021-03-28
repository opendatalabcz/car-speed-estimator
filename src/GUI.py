import cv2
from src.carSpeedEstimator import *
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk
from PIL import Image
import numpy as np

#   This class is for creating GUI
class GUI(Tk):
    def __init__(self):
        super(GUI, self).__init__()
        self.title("Car Speed Estimator")
        self.minsize(100, 100)

        self.labelFrame = ttk.LabelFrame(self, text="Video file")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)
        self.labelFrame2 = ttk.LabelFrame(self, text="Measuring Area")

        self.video_button()
        self.measuring_param()

        #   Variables for drawing lines
        self.cnt = 3
        self.line1 = False
        self.line2 = False

    def run(self):
        #   Get information about measured area
        try:
            s_line_pt1_x = int(self.s_line_pt1_x.get())
            s_line_pt1_y = int(self.s_line_pt1_y.get())
            s_line_pt2_x = int(self.s_line_pt2_x.get())
            s_line_pt2_y = int(self.s_line_pt2_y.get())
            e_line_pt1_x = int(self.e_line_pt1_x.get())
            e_line_pt1_y = int(self.e_line_pt1_y.get())
            e_line_pt2_x = int(self.e_line_pt2_x.get())
            e_line_pt2_y = int(self.e_line_pt2_y.get())
            len = int(self.len.get())
        except ValueError:
            return

        #   Load video file
        self.cap = cv2.VideoCapture(self.filename)
        start_line = [(s_line_pt1_x, s_line_pt1_y), (s_line_pt2_x, s_line_pt2_y)]
        end_line = [(e_line_pt1_x, e_line_pt1_y), (e_line_pt2_x, e_line_pt2_y)]

        #   Create estimator and run it
        estimator = CarSpeedEstimator(self.cap, start_line, end_line, len)
        estimator.run()

    def video_button(self):
        self.v_button = ttk.Button(self.labelFrame, text="Browse A File", command=self.fileDialog)
        self.v_button.grid(column=1, row=1)

    def start_button(self):
        self.s_button = Button(self, text="start", command=self.run)
        self.s_button.grid(row=10,column=0)

    def measuring_param(self):
        self.line1_txt = Label(self.labelFrame2, text="Starting Line")
        self.line1_txt.grid(column=0, columnspan=2, row=0)
        self.s_line_pt1_x = Entry(self.labelFrame2, width=10)
        self.s_line_pt1_x.grid(column=0,row=1)
        self.s_line_pt1_y = Entry(self.labelFrame2, width=10)
        self.s_line_pt1_y.grid(column=1, row=1)
        self.s_line_pt2_x = Entry(self.labelFrame2, width=10)
        self.s_line_pt2_x.grid(column=0, row=2)
        self.s_line_pt2_y = Entry(self.labelFrame2, width=10)
        self.s_line_pt2_y.grid(column=1, row=2)
        self.line1_btn = Button(self.labelFrame2, text="Create Line", command=self.draw_line1)
        self.line1_btn.grid(column=0, columnspan=2, row=3)
        self.line2_txt = Label(self.labelFrame2, text="Ending Line")
        self.line2_txt.grid(column=0, columnspan=2, row=4)
        self.e_line_pt1_x = Entry(self.labelFrame2, width=10)
        self.e_line_pt1_x.grid(column=0,row=5)
        self.e_line_pt1_y = Entry(self.labelFrame2, width=10)
        self.e_line_pt1_y.grid(column=1, row=5)
        self.e_line_pt2_x = Entry(self.labelFrame2, width=10)
        self.e_line_pt2_x.grid(column=0, row=6)
        self.e_line_pt2_y = Entry(self.labelFrame2, width=10)
        self.e_line_pt2_y.grid(column=1, row=6)
        self.line1_btn = Button(self.labelFrame2, text="Create Line", command=self.draw_line2)
        self.line1_btn.grid(column=0, columnspan=2, row=7)
        self.len_txt = Label(self.labelFrame2, text="Length")
        self.len_txt.grid(column=0, row=8)
        self.len = Entry(self.labelFrame2, width=10)
        self.len.grid(column=1, row=8)
        self.line_button = Button(self.labelFrame2, text="Show Lines", command=self.show_lines)
        self.line_button.grid(column=0, columnspan=2, row=9)

    def fileDialog(self):

        #   Choose button for video file
        self.filename = filedialog.askopenfilename(initialdir="./", title="Select A File", filetypes=
        [("video",".mp4"), ("video", ".avi")])

        #   Get first frame of video file
        self.cap = cv2.VideoCapture(self.filename)
        _, frame = self.cap.read()
        self.frame_original = frame
        self.frame_rd = True
        width = int(self.cap.get(3))
        height = int(self.cap.get(4))

        #   Switch colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #   Show first frame
        self.image = ImageTk.PhotoImage(image= Image.fromarray(frame))
        self.canvas = tkinter.Canvas(self.labelFrame, width=width, height=height)
        self.canvas.grid(column=1, row=3)
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
        self.canvas.bind("<Button 1>", self.get_cordinates)

        #   Show parameter setup and run button
        self.labelFrame2.grid(column=1, row=1, padx=20, pady=20)
        self.start_button()

    def get_cordinates(self, event):
        if self.cnt < 3:
            x, y = event.x, event.y
            if self.line1:
                if self.cnt == 1:
                    self.s_line_pt1_x.insert(0, str(x))
                    self.s_line_pt1_y.insert(0, str(y))
                else:
                    self.s_line_pt2_x.insert(0, str(x))
                    self.s_line_pt2_y.insert(0, str(y))
                    self.show_lines()
            else:
                if self.cnt == 1:
                    self.e_line_pt1_x.insert(0, str(x))
                    self.e_line_pt1_y.insert(0, str(y))
                else:
                    self.e_line_pt2_x.insert(0, str(x))
                    self.e_line_pt2_y.insert(0, str(y))
                    self.show_lines()
            self.cnt += 1

    def draw_line1(self):
        self.cnt = 1
        self.line1 = True
        self.line2 = False
        self.s_line_pt1_x.delete(0, END)
        self.s_line_pt1_y.delete(0, END)
        self.s_line_pt2_x.delete(0, END)
        self.s_line_pt2_y.delete(0, END)

    def draw_line2(self):
        self.cnt = 1
        self.line1 = False
        self.line2 = True
        self.e_line_pt1_x.delete(0, END)
        self.e_line_pt1_y.delete(0, END)
        self.e_line_pt2_x.delete(0, END)
        self.e_line_pt2_y.delete(0, END)

    def show_lines(self):
        frame = self.frame_original.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        try:
            s_line_pt1_x = int(self.s_line_pt1_x.get())
            s_line_pt1_y = int(self.s_line_pt1_y.get())
            s_line_pt2_x = int(self.s_line_pt2_x.get())
            s_line_pt2_y = int(self.s_line_pt2_y.get())
            cv2.line(frame, (s_line_pt1_x, s_line_pt1_y), (s_line_pt2_x, s_line_pt2_y), (0, 255, 0), 2)
        except ValueError:
            pass

        try:
            e_line_pt1_x = int(self.e_line_pt1_x.get())
            e_line_pt1_y = int(self.e_line_pt1_y.get())
            e_line_pt2_x = int(self.e_line_pt2_x.get())
            e_line_pt2_y = int(self.e_line_pt2_y.get())
            cv2.line(frame, (e_line_pt1_x, e_line_pt1_y), (e_line_pt2_x, e_line_pt2_y), (0, 0, 255), 2)
        except ValueError:
            pass

        self.image = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)