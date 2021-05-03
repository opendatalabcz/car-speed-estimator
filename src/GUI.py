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

        #   Variables for drawing lines
        self.point_cnt = 3
        self.line = IntVar()
        self.param_visible = False

        self.labelFrame = ttk.LabelFrame(self, text="Video file")
        self.labelFrame.grid(column=0, row=1, rowspan=30, padx=20, pady=20)
        self.labelFrame2 = ttk.LabelFrame(self, text="Measuring Area")
        self.labelFrame2.grid(column=1, row=1, rowspan=30,padx=20, pady=20)

        self.canvas = tkinter.Canvas(self.labelFrame, width=1000, height=700)
        self.canvas.grid(column=1, row=3)

        self.video_button()
        self.setup_measuring_params()
        self.start_button()
        self.warning_label()

    def run(self):

        #   Try load video file
        try:
            cap = cv2.VideoCapture(self.filename)
        except AttributeError:
            self.w_label['text'] = "no video file"
            return

        #   Try get information about Starting line
        try:
            s_line_pt1_x = int(self.s_line_pt1_x.get())
            s_line_pt1_y = int(self.s_line_pt1_y.get())
            s_line_pt2_x = int(self.s_line_pt2_x.get())
            s_line_pt2_y = int(self.s_line_pt2_y.get())
            start_line = [(s_line_pt1_x, s_line_pt1_y), (s_line_pt2_x, s_line_pt2_y)]
        except ValueError:
            self.w_label['text'] = "missing starting line"
            return

        #   Try get information about Ending line
        try:
            e_line_pt1_x = int(self.e_line_pt1_x.get())
            e_line_pt1_y = int(self.e_line_pt1_y.get())
            e_line_pt2_x = int(self.e_line_pt2_x.get())
            e_line_pt2_y = int(self.e_line_pt2_y.get())
            end_line = [(e_line_pt1_x, e_line_pt1_y), (e_line_pt2_x, e_line_pt2_y)]
        except ValueError:
            self.w_label['text'] = "missing ending line"
            return

        #   Try get information about length of measuring area
        try:
            length = int(self.len.get())
        except ValueError:
            self.w_label['text'] = "missing length"
            return

        #   Clear warning label
        self.w_label['text'] = ""

        #   Create estimator and run it
        estimator = CarSpeedEstimator(cap, start_line, end_line, length)
        estimator.run()

    def video_button(self):
        self.v_button = ttk.Button(self.labelFrame, text="Browse A File", command=self.fileDialog)
        self.v_button.grid(column=1, row=1)

    def warning_label(self):
        self.w_label = Label(self, text="")
        self.w_label.grid(row=25, column=1)

    def start_button(self):
        self.s_button = Button(self, text="start", command=self.run, width=10)
        self.s_button.grid(row=24, column=1)

    #   Creates class variables for measuring area
    def setup_measuring_params(self):

        #   Starting line parameters
        self.line1_txt = Label(self.labelFrame2, text="Starting Line")
        self.line1_x_txt = Label(self.labelFrame2, text="X")
        self.line1_y_txt = Label(self.labelFrame2, text="Y")
        self.s_line_pt1_x = Entry(self.labelFrame2, width=10)
        self.s_line_pt1_y = Entry(self.labelFrame2, width=10)
        self.s_line_pt2_x = Entry(self.labelFrame2, width=10)
        self.s_line_pt2_y = Entry(self.labelFrame2, width=10)
        self.line1_btn = Radiobutton(self.labelFrame2, text="Draw", indicatoron=0, bg='green', fg='white',
                                     variable=self.line, value=1, command=self.draw_line1)

        #   Ending line parameters
        self.line2_txt = Label(self.labelFrame2, text="Ending Line")
        self.line2_x_txt = Label(self.labelFrame2, text="X")
        self.line2_y_txt = Label(self.labelFrame2, text="Y")
        self.e_line_pt1_x = Entry(self.labelFrame2, width=10)
        self.e_line_pt1_y = Entry(self.labelFrame2, width=10)
        self.e_line_pt2_x = Entry(self.labelFrame2, width=10)
        self.e_line_pt2_y = Entry(self.labelFrame2, width=10)
        self.line2_btn = Radiobutton(self.labelFrame2, text="Draw", indicatoron=0, bg='blue', fg='white',
                                     variable=self.line, value=2, command=self.draw_line2)

        #   length parameters
        self.len_txt = Label(self.labelFrame2, text="Length(m)")
        self.len = Entry(self.labelFrame2, width=10)

        #   create buttons
        self.line_button = Button(self.labelFrame2, text="Show Lines", command=self.show_lines)
        self.show_param_btn = Button(self.labelFrame2, text="Show Detail", command=self.show_details)

        self.show_measuring_params()

    #   Default show of class variables
    def show_measuring_params(self):
        self.line1_txt.grid(column=0, columnspan=2, row=0)
        self.line1_btn.grid(column=0, columnspan=2, row=4)
        self.line2_txt.grid(column=0, columnspan=2, row=5)
        self.line2_btn.grid(column=0, columnspan=2, row=9)
        self.len_txt.grid(column=0, row=10)
        self.len.grid(column=1, row=10)
        self.show_param_btn.grid(column=0, columnspan=2, row=13)

    def fileDialog(self):

        #   Choose button for video file
        self.filename = filedialog.askopenfilename(initialdir="./", title="Select A File", filetypes=
        [("video", ".mp4"), ("video", ".avi")])

        #   Get first frame of video file
        cap = cv2.VideoCapture(self.filename)
        _, frame = cap.read()
        self.frame_original = frame
        width = int(cap.get(3))
        height = int(cap.get(4))

        #   Switch colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #   Show first frame
        self.create_canvas(width, height, frame)

    def create_canvas(self, width, height, image):
        self.deform = [1, 1]
        if width < 1000:
            c_width = width
        else:
            c_width = 1000
            self.deform[0] = 1000 / width
        if height < 700:
            c_height = height
        else:
            c_height = 700
            self.deform[1] = 700 / height

        dim = (c_width, c_height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        self.image = ImageTk.PhotoImage(image=Image.fromarray(image))

        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
        self.canvas.bind("<Button 1>", self.get_cordinates)

    def get_cordinates(self, event):
        if self.point_cnt < 3:
            x, y = event.x, event.y
            x = int(x / self.deform[0])
            y = int(y / self.deform[1])
            if self.line.get() == 1:
                if self.point_cnt == 1:
                    self.s_line_pt1_x.insert(0, str(x))
                    self.s_line_pt1_y.insert(0, str(y))
                else:
                    self.s_line_pt2_x.insert(0, str(x))
                    self.s_line_pt2_y.insert(0, str(y))
                    self.show_lines()
            if self.line.get() == 2:
                if self.point_cnt == 1:
                    self.e_line_pt1_x.insert(0, str(x))
                    self.e_line_pt1_y.insert(0, str(y))
                else:
                    self.e_line_pt2_x.insert(0, str(x))
                    self.e_line_pt2_y.insert(0, str(y))
                    self.show_lines()
            self.point_cnt += 1

    def draw_line1(self):
        self.point_cnt = 1
        self.s_line_pt1_x.delete(0, END)
        self.s_line_pt1_y.delete(0, END)
        self.s_line_pt2_x.delete(0, END)
        self.s_line_pt2_y.delete(0, END)

    def draw_line2(self):
        self.point_cnt = 1
        self.e_line_pt1_x.delete(0, END)
        self.e_line_pt1_y.delete(0, END)
        self.e_line_pt2_x.delete(0, END)
        self.e_line_pt2_y.delete(0, END)

    def show_lines(self):

        try:
            frame = self.frame_original
        except AttributeError:
            self.w_label['text'] = "no video file"
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        shape = frame.shape
        dim = (int(shape[1] * self.deform[0]), int(shape[0] * self.deform[1]))
        frame = cv2.resize(frame, dim)

        self.line.set(0)

        try:
            s_line_pt1_x = int(int(self.s_line_pt1_x.get()) * self.deform[0])
            s_line_pt1_y = int(int(self.s_line_pt1_y.get()) * self.deform[1])
            s_line_pt2_x = int(int(self.s_line_pt2_x.get()) * self.deform[0])
            s_line_pt2_y = int(int(self.s_line_pt2_y.get()) * self.deform[1])
            self.canvas.line1 = cv2.line(frame, (s_line_pt1_x, s_line_pt1_y),
                                         (s_line_pt2_x, s_line_pt2_y), (0, 180, 0), 2)
        except ValueError:
            pass

        try:
            e_line_pt1_x = int(int(self.e_line_pt1_x.get()) * self.deform[0])
            e_line_pt1_y = int(int(self.e_line_pt1_y.get()) * self.deform[1])
            e_line_pt2_x = int(int(self.e_line_pt2_x.get()) * self.deform[0])
            e_line_pt2_y = int(int(self.e_line_pt2_y.get()) * self.deform[1])
            self.canvas.line2 = cv2.line(frame, (e_line_pt1_x, e_line_pt1_y),
                                         (e_line_pt2_x, e_line_pt2_y), (0, 0, 255), 2)
        except ValueError:
            pass

        self.image = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)

    def show_details(self):
        self.param_visible = not self.param_visible
        if self.param_visible:
            self.s_line_pt1_x.grid(column=0, row=2)
            self.s_line_pt1_y.grid(column=1, row=2)
            self.s_line_pt2_x.grid(column=0, row=3)
            self.s_line_pt2_y.grid(column=1, row=3)
            self.e_line_pt1_x.grid(column=0, row=7)
            self.e_line_pt1_y.grid(column=1, row=7)
            self.e_line_pt2_x.grid(column=0, row=8)
            self.e_line_pt2_y.grid(column=1, row=8)
            self.line1_x_txt.grid(column=0, row=1)
            self.line1_y_txt.grid(column=1, row=1)
            self.line2_x_txt.grid(column=0, row=6)
            self.line2_y_txt.grid(column=1, row=6)
            self.line_button.grid(column=0, columnspan=2, row=12)
        else:
            self.s_line_pt1_x.grid_forget()
            self.s_line_pt1_y.grid_forget()
            self.s_line_pt2_x.grid_forget()
            self.s_line_pt2_y.grid_forget()
            self.e_line_pt1_x.grid_forget()
            self.e_line_pt1_y.grid_forget()
            self.e_line_pt2_x.grid_forget()
            self.e_line_pt2_y.grid_forget()
            self.line1_x_txt.grid_forget()
            self.line1_y_txt.grid_forget()
            self.line2_x_txt.grid_forget()
            self.line2_y_txt.grid_forget()
            self.line_button.grid_forget()
        return
