import cv2
import tkinter as tk
from tkinter import filedialog
from PictureObjectDetection import object_detection

videoFile = ""
detection = object_detection()

def addApp():
    file = filedialog.askopenfile(initialdir="./Data", title="Select File")
    global videoFile
    videoFile = file.name

def runDetection():
    print(videoFile)
    cap = cv2.VideoCapture(videoFile)
    n = 0
    while cap.isOpened():
        n = n + 1
        ret, frame = cap.read()
        if n == 10:
            n = 0
            frame = detection.detect_objects(frame, 0.6, True)

            cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows
    cap.release()

#Creating root
root = tk.Tk()
canvas = tk.Canvas(root, height=300, width=300, bg="snow2")
canvas.pack()

#Add Button
openFile = tk.Button(root, text="Choose Video", padx=10, pady=5, fg="black", command=addApp)
openFile.pack()

#Add Button
RunButton = tk.Button(root, text="Run", padx=10, pady=5, fg="black", command=runDetection)
RunButton.pack()

#Run GUI
root.mainloop()
