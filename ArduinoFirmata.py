import RPi.GPIO as GPIO
import time
from time import sleep
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Progressbar
import sqlite3


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# X-Direction
xDir=2
xClk=3
xExo=4
xReset=5
xCN=6

# Y-Direction
yDir=7
yClk=8
yExo=9
yReset=10
yCN=11

# Z-Direction
zDir=23
zClk=24
zExo=25
zReset=27
zCN=17

fast=500

distX=5000
GPIO.setup(xDir,GPIO.OUT)
GPIO.setup(xClk,GPIO.OUT)
GPIO.setup(xExo,GPIO.OUT)
GPIO.setup(xReset,GPIO.OUT)
GPIO.setup(xCN,GPIO.OUT)

GPIO.setup(yDir,GPIO.OUT)
GPIO.setup(yClk,GPIO.OUT)
GPIO.setup(yExo,GPIO.OUT)
GPIO.setup(yReset,GPIO.OUT)
GPIO.setup(yCN,GPIO.OUT)

GPIO.setup(zDir,GPIO.OUT)
GPIO.setup(zClk,GPIO.OUT)
GPIO.setup(zExo,GPIO.OUT)
GPIO.setup(zReset,GPIO.OUT)
GPIO.setup(zCN,GPIO.OUT)

GPIO.output(xReset,GPIO.HIGH)
GPIO.output(yReset,GPIO.HIGH)
GPIO.output(zReset,GPIO.HIGH)
GPIO.output(xCN,GPIO.HIGH)
GPIO.output(yCN,GPIO.HIGH)
GPIO.output(zCN,GPIO.HIGH)

GPIO.output(xExo,GPIO.LOW)
GPIO.output(yExo,GPIO.LOW)
GPIO.output(zExo,GPIO.LOW)

def xForward():
    GPIO.output(xDir, GPIO.LOW)
    GPIO.output(xClk, GPIO.HIGH)
    sleep(0.005)
    GPIO.output(xClk, GPIO.LOW)
def yForward():
    GPIO.output(yDir, GPIO.LOW)
    GPIO.output(yClk, GPIO.HIGH)
    sleep(0.005)
    GPIO.output(yClk, GPIO.LOW)
def zForward():
    GPIO.output(zDir, GPIO.LOW)
    GPIO.output(zClk, GPIO.HIGH)
    sleep(0.005)
    GPIO.output(zClk, GPIO.LOW)

def xBackward():
    GPIO.output(xDir, GPIO.HIGH)
    GPIO.output(xClk, GPIO.HIGH)
    sleep(0.005)
    GPIO.output(xClk, GPIO.LOW)

def yBackward():
    GPIO.output(yDir, GPIO.HIGH)
    GPIO.output(yClk, GPIO.HIGH)
    sleep(0.005)
    GPIO.output(yClk, GPIO.LOW)

def zBackward():
    GPIO.output(zDir, GPIO.HIGH)
    GPIO.output(zClk, GPIO.HIGH)
    sleep(0.005)
    GPIO.output(zClk, GPIO.LOW)

global SampleButton
def addDesign():
    Add = Tk()
    Add.title("Add Design Window")
    Add.geometry('600x400')
    Add.wm_resizable(0,0)
    AddFrame=Frame(Add,relief=RIDGE,bg="white")
    AddFrame.pack(fill=BOTH,expand=1)
    Title=Label(AddFrame,text="Design Title",font=("Times",12,"bold"),bg="white",fg="#871f78")
    Title.pack()
    Title.place(x=20,y=90)
    TitleEntry= tk.Entry(AddFrame,width=50,borderwidth=4,font=("Times",12))
    TitleEntry.pack()
    TitleEntry.place(x=120,y=90)
global TaskCompleted
TaskCompleted = 0
def L_Algorithm():
    global SampleButton
    global XLoopRange
    global YLoopRange
    global string
    global TaskCompleted
    global board
    global delay
    #for x in range(XLoopRange):
     #   board.write('x'.encode())
    #time.sleep(1)
    for x in range(XLoopRange):
        board.write('X'.encode())
    #for y in range(YLoopRange):
     #   board.write('y'.encode())
    TaskCompleted = 1
    SampleButton="NONE"
    StartMachine()
def StartMachine():
    global SampleButton
    global TaskCompleted
    global DesignFrame
    global status
    if status == "ONLINE":
        StartLabel = Label(DesignFrame, bg="white", fg="red", font=("Times", 14, "bold"))
        StartLabel.pack()
        StartLabel.place(x=200, y=25)
        StartLabel['text'] = "Machine is Working on your Design..."
        if SampleButton == "L":
            if TaskCompleted == 0:
                L_Algorithm()
        if SampleButton == "NONE":
            StartLabel['text'] = "TASK Completed Successfully!"
    else:
        tk.messagebox.showerror("System Error","Please Connect Your Arduino and Restart Me")
def I_Design():
    global SampleButton
    SampleButton = "L"
    Design_Win()
def L_Design():
    global SampleButton
    global TaskCompleted
    TaskCompleted = 0
    SampleButton = "L"
    Design_Win()
def Design_Win():
    global string
    global SampleButton
    global DesignFrame
    global delay
    delay = string.get()
    delay = int(delay)

    delay = delay/10000000
    print(delay)
    ask = tk.messagebox.askquestion("Question Window","Do You Want to Start?")
    if ask == "yes":
        DesignL=Tk()
        DesignL.title("Designing Sketch")
        DesignL.geometry('700x400')
        DesignL.wm_resizable(0,0)
        DesignFrame=Frame(DesignL,bg="white")
        DesignFrame.pack(fill=BOTH,expand=1)
        infoLabel = Label(DesignFrame, bg="white", fg="red",
                          font=("Times", 14, "bold"))
        infoLabel.pack()
        infoLabel.place(x=100,y=30)
        delay = delay/1000
        rotationTime = delay*200                      #1.8 Degree Motor will take 200 bulses to complete 1 rotation of 360 degree
        check = rotationTime
        doublecheck = rotationTime
        counter = 0
        for x in range(100):
            if doublecheck >= 1:
                if doublecheck > 1:
                    doublecheck = doublecheck - 1
                    doublecheck = doublecheck/check
                    counter = counter + doublecheck
                break
            doublecheck = doublecheck + check
            counter = counter + 1
        if counter == 0:
            counter = 1/rotationTime

        TotalRotationPerSec = counter
        DistancePerSec = TotalRotationPerSec*3.3
        Dis_Sec = DistancePerSec
        DistancePerSec = str(DistancePerSec)
        TotalRotationPerSec = str(TotalRotationPerSec)
        rotationTime = str(rotationTime)
        speedLabel = Label(DesignFrame,text="Time Per Rotation ",bg = "white",fg="green",font=("Times",12,"bold"))
        speedLabel.pack()
        speedLabel.place(x=20,y=70)
        RotationTime = Label(DesignFrame,text=rotationTime+" Sec/Rotation",bg="green",fg="white",font=("Times",25,"bold"))
        RotationTime.pack()
        RotationTime.place(x=20,y=100)
        Distance = Label(DesignFrame, text="Distance Covered Per Rotation", bg="white", fg="green",
                             font=("Times", 12, "bold"))
        Distance.pack()
        Distance.place(x=20, y=150)
        DistanceCovered = Label(DesignFrame, text="3.3 mm / Rotation", bg="green", fg="white",
                         font=("Times", 25, "bold"))
        DistanceCovered.pack()
        DistanceCovered.place(x=20, y=180)

        RotationSecLabel = Label(DesignFrame, text="Total Rotations Per Second", bg="white", fg="green",
                         font=("Times", 12, "bold"))
        RotationSecLabel.pack()
        RotationSecLabel.place(x=330, y=70)
        RotationSec = Label(DesignFrame, text=TotalRotationPerSec, bg="green", fg="white",
                                font=("Times", 25, "bold"))
        RotationSec.pack()
        RotationSec.place(x=330, y=100)

        DistanceSecLabel = Label(DesignFrame, text="Distance Covered Per Second", bg="white", fg="green",
                                 font=("Times", 12, "bold"))
        DistanceSecLabel.pack()
        DistanceSecLabel.place(x=330, y=150)

        DistanceSec = Label(DesignFrame, text=DistancePerSec+" mm", bg="green", fg="white",font=("Times", 25, "bold"))
        DistanceSec.pack()
        DistanceSec.place(x=330, y=180)

        if SampleButton == "L":
            X = 10
            Y = 5
        total = X+Y
        TimeReq = 1/Dis_Sec                  #time for 1 mm
        XTime = TimeReq*X
        YTime = TimeReq*Y
        TimeReq = total*TimeReq

        TimeReqStr = str(TimeReq)
        Xstring = str(X)
        Ystring = str(Y)
        X_PlaneLabel = Label(DesignFrame,text="X-Plane Distance",bg = "white",fg="green",font = ("Times",12,"bold"))
        X_PlaneLabel.pack()
        X_PlaneLabel.place(x=20,y=230)
        X_Plane = Label(DesignFrame, text=Xstring+" mm", bg="green", fg="white",
                             font=("Times", 25, "bold"))
        X_Plane.pack()
        X_Plane.place(x=20, y=260)

        Y_PlaneLabel = Label(DesignFrame, text="Y-Plane Distance", bg="white", fg="green", font=("Times", 12, "bold"))
        Y_PlaneLabel.pack()
        Y_PlaneLabel.place(x=330, y=230)
        Y_Plane = Label(DesignFrame, text=Ystring + " mm", bg="green", fg="white",
                        font=("Times", 25, "bold"))
        Y_Plane.pack()
        Y_Plane.place(x=330, y=260)

        timeReqLabel = Label(DesignFrame,text="Total Time Required(Sec)",bg="white",fg="green",font=("Times",12,"bold"))
        timeReqLabel.pack()
        timeReqLabel.place(x=20,y=310)
        StartBtn = Button(DesignFrame, text="Start", bg="#871f78", fg="white", font=("Times", 20, "bold"),
                          command=StartMachine)
        StartBtn.pack()
        StartBtn.place(x=590, y=340)

        timeReq = Label(DesignFrame, text=TimeReqStr, fg="white", bg="green",
                             font=("Times", 25, "bold"))
        timeReq.pack()
        timeReq.place(x=20, y=340)
        global XLoopRange
        global YLoopRange
        XLoopRange = XTime/delay
        YLoopRange = YTime / delay
        XLoopRange = int(XLoopRange)
        YLoopRange = int(YLoopRange)
def Samples():
    global Startframe
    SampleFrame = LabelFrame(Startframe, relief=RIDGE, text="SAMPLE DESIGN", width=790, height=500, borderwidth=5,
                          bg="white", fg="#871f78")
    SampleFrame.pack()
    SampleFrame.place(x=100, y=50)
    DelayLabel=Label(SampleFrame,text="Step Delay (micro sec):",bg="white",fg="#871f78",font=("Times",12,"bold") )
    DelayLabel.pack()
    DelayLabel.place(x=600,y=5)
    global string
    string= StringVar()
    string.set("1")
    option = OptionMenu(SampleFrame,string,300,400,500,600,700,800,1000)
    option.pack()
    option.place(x=650,y=30)


    L = Button(SampleFrame,text="L",bg="#871f78",fg="white",font=("Times",50,"bold"),relief=FLAT,command=L_Design)
    L.pack()
    L.place(x=20,y=20)
    I = Button(SampleFrame, text="I", bg="#871f78", fg="white", font=("Times", 50, "bold"), relief=FLAT,command = I_Design)
    I.pack()
    I.place(x=140, y=20)
def Check_X_STEP(event):
    global XSTEPEntry
    global checkstatus
    global CombineBtn
    global CombineBtn_Back
    checkstatus += 1
    if checkstatus == 3:
        CombineBtn_Back['state']=NORMAL
        CombineBtn['state'] = NORMAL
    word = ""
    for i in XSTEPEntry.get():
        if i.isdigit() or i == ".":
            word += i
        else:
            pass
    XSTEPEntry.delete(0, "end")
    XSTEPEntry.insert(0, word)
def Check_Y_STEP(event):
    global YSTEPEntry
    global checkstatus
    global CombineBtn
    global CombineBtn_Back
    checkstatus += 1
    if checkstatus == 3:
        CombineBtn_Back['state'] = NORMAL
        CombineBtn['state'] = NORMAL
    word = ""
    for i in YSTEPEntry.get():
        if i.isdigit() or i == ".":
            word += i
        else:
            pass
    YSTEPEntry.delete(0, "end")
    YSTEPEntry.insert(0, word)
def CheckEntry(event):
    global CombineBtn
    global CDisEntry
    global checkstatus
    global CombineBtn_Back
    checkstatus += 1
    if checkstatus == 3:
        CombineBtn['state']=NORMAL
        CombineBtn_Back['state']=NORMAL
    word = ""
    for i in CDisEntry.get():
        if i.isdigit() or i == ".":
            word += i
        else:
            pass
    CDisEntry.delete(0,"end")
    CDisEntry.insert(0,word)
def checkEntry(event):
    global DisEntry
    global X_Forward
    global X_Back
    global Y_Forward
    global Y_Back
    global Z_Forward
    global Z_Back
    word = ""
    X_Forward['state'] = NORMAL
    X_Back['state'] = NORMAL
    Y_Forward['state'] = NORMAL
    Y_Back['state'] = NORMAL
    Z_Forward['state'] = NORMAL
    Z_Back['state'] = NORMAL
    for i in DisEntry.get():
        if i.isdigit() or i == ".":
            word += i
        else:
            pass
    DisEntry.delete(0,"end")
    DisEntry.insert(0,word)
def Update_Database():
    global X_Origin
    global Y_Origin
    global Z_Origin
    conn = sqlite3.connect("FYP_DATABASE.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Origin SET X_Origin=?,Y_Origin=? ,Z_Origin=? WHERE Sr = ?", (X_Origin,Y_Origin,Z_Origin,"1"))
    conn.commit()
    cursor.close()
    conn.close()
def X_on(event):
    X_ON()
def X_ON():
    global board
    global TimeDelay
    global DisEntry
    global StopBtn
    global ButtenPressed
    global Entry_Box
    global Set_Position
    global ValueEntry
    Update_Origin()
    Update_Database()
    if Entry_Box == "Empty":
        value = int(Set_Position)
    elif Entry_Box == "None":
        value = int(ValueEntry.get())
    else:
        value = int(DisEntry.get())
    steps = value * 137
    for x in range(steps):
        if ButtenPressed == "X_Forward":
            xForward()
        elif ButtenPressed == "Y_Forward":
            yForward()
        elif ButtenPressed == "Z_Forward":
            zForward()
        else:
            pass
        if ButtenPressed == "X_Back":
            xBackward()
        elif ButtenPressed == "Y_Back":
            yBackward()
        elif ButtenPressed == "Z_Back":
            zBackward()
        else:
            pass
def X_FORWARD_Pressed():
    global ButtenPressed
    global DisEntry
    global X_Origin
    global Entry_Box
    error = 0
    if Entry_Box == "None":
        Entry_Box = "Value"
        for i in DisEntry.get():
            if i.isdigit() or i == ".":
                pass
            else:
                error = 1
    global status
    if status != "OFFLINE":
        if error == 0:
            origin = float(X_Origin) + float(DisEntry.get())
            if origin <= 100:
                X_Origin = str(origin)
                ButtenPressed = "X_Forward"
                X_ON()
            else:
                tk.messagebox.showerror("ERROR OCCURED", "Maximum distance u can cover is " + str(100 - float(Y_Origin)))
        else:
            tk.messagebox.showerror("ERROR OCCURED", "PLEASE ENTER A VALID DISTANCE")
    else:
        tk.messagebox.showerror("SYSYEM ERROR","COMPUTER IS NOT CONNECTED")
def Y_BACK_Pressed():
    global ButtenPressed
    global Y_Origin
    global DisEntry
    error = 0
    global Entry_Box
    Entry_Box = "Value"
    for i in DisEntry.get():
        if i.isdigit() or i == ".":
            pass
        else:
            error = 1
    global status
    if status == "OFFLINE":
        error = 1
    if error == 0:
        origin = float(Y_Origin) - float(DisEntry.get())
        if origin >= 0:
            Y_Origin = str(origin)
            ButtenPressed = "Y_Back"
            X_ON()
        else:
            tk.messagebox.showerror("ERROR OCCURED", "Maximum distance u can cover is " + Y_Origin)
    else:
        tk.messagebox.showerror("ERROR OCCURED", "PLEASE ENTER A VALID DISTANCE")
def X_BACK_Pressed():
    global ButtenPressed
    global X_Origin
    global DisEntry
    error = 0
    global Entry_Box
    Entry_Box = "Value"
    for i in DisEntry.get():
        if i.isdigit() or i == ".":
            pass
        else:
            error = 1
    global status
    if status != "OFFLINE":
        if error == 0:
            origin = float(X_Origin) - float(DisEntry.get())
            if origin >= 0:
                X_Origin = str(origin)
                ButtenPressed = "X_Back"
                X_ON()
            else:
                tk.messagebox.showerror("ERROR OCCURED", "Maximum distance u can cover is " + X_Origin)
        else:
            tk.messagebox.showerror("ERROR OCCURED", "PLEASE ENTER A VALID DISTANCE")
    else:
        tk.messagebox.showerror("SYSTEM ERROR", "COMPUTER IS NOT CONNECTED")
def Y_FORWARD_Pressed():
    global ButtenPressed
    global Y_Origin
    global DisEntry
    error = 0
    global Entry_Box
    Entry_Box = "Value"
    for i in DisEntry.get():
        if i.isdigit() or i == ".":
            pass
        else:
            error = 1
    global status
    if status != "OFFLINE":
        if error == 0:
            origin = float(Y_Origin) + float(DisEntry.get())
            if origin < 200:
                Y_Origin = str(origin)
                ButtenPressed = "Y_Forward"
                X_ON()
            else:
                tk.messagebox.showerror("ERROR OCCURED", "Maximum distance u can cover is " + str(200-int(Y_Origin)))
        else:
            tk.messagebox.showerror("ERROR OCCURED", "PLEASE ENTER A VALID DISTANCE")
    else:
        tk.messagebox.showerror("SYSTEM ERROR","COMPUTER IS NOT CONNECTED")
def Z_FORWARD_Pressed():
    global ButtenPressed
    global Z_Origin
    global DisEntry
    error = 0
    global Entry_Box
    Entry_Box = "Value"
    for i in DisEntry.get():
        if i.isdigit() or i == ".":
            pass
        else:
            error = 1
    global status
    if status != "OFFLINE":
        if error == 0:
            origin = float(Z_Origin) + float(DisEntry.get())
            if origin <= 53:
                Z_Origin = str(origin)
                ButtenPressed = "Z_Forward"
                X_ON()
            else:
                tk.messagebox.showerror("ERROR OCCURED", "Maximum distance u can cover is " + str(50 - float(Z_Origin)))
        else:
            tk.messagebox.showerror("ERROR OCCURED", "PLEASE ENTER A VALID DISTANCE")
    else:
        tk.messagebox.showerror("SYSTEM ERROR", "COMPUTER IS NOT CONNECTED")
def Z_BACK_Pressed():
    global ButtenPressed
    global Z_Origin
    global DisEntry
    error = 0
    global Entry_Box
    Entry_Box = "Value"
    for i in DisEntry.get():
        if i.isdigit() or i == ".":
            pass
        else:
            error = 1
    global status
    if status != "OFFLINE":
        if error == 0:
            origin = float(Z_Origin) - float(DisEntry.get())
            if origin >= 0:
                Z_Origin = str(origin)
                ButtenPressed = "Z_Back"
                X_ON()
            else:
                tk.messagebox.showerror("ERROR OCCURED", "Maximum distance u can cover is " + Z_Origin)
        else:
            tk.messagebox.showerror("ERROR OCCURED", "PLEASE ENTER A VALID DISTANCE")
    else:
        tk.messagebox.showerror("SYSTEM ERROR", "COMPUTER IS NOT CONNECTED")
def CombineOper():
    global XSTEPEntry
    global YSTEPEntry
    global CDisEntry
    global board
    global CombineDir
    global X_Origin
    global Y_Origin
    global Z_Origin
    error = 0
    global Entry_Box
    for i in CDisEntry.get():
        if i.isdigit() or i == ".":
            pass
        else:
            error = 1
    if error == 0:
        if Entry_Box != "Empty":
            xfactor = 1
            yfactor = 1
            value = float(CDisEntry.get())
            xvalue = float(XSTEPEntry.get())
            yvalue = (float(YSTEPEntry.get()))
        else:
            xfactor = 1
            yfactor = 1
            xvalue = float(X_Origin)
            yvalue = float(Y_Origin)
            value = float(X_Origin) + float(Y_Origin)
        value = int(value) * 137
        xvalue = float(xvalue * 137)
        yvalue = yvalue * 137
        xplay = ''
        yplay = ''
        for i in range(value):
            for x in range(xfactor):
                if xvalue != 0:
                    if CombineDir == "FORWARD":
                        xForward()
                    if CombineDir == "REVERSE":
                        xBackward()
                    xvalue = xvalue - 1
                for y in range(yfactor):
                    if yvalue != 0:
                        if CombineDir == "FORWARD":
                            yForward()
                        if CombineDir == "REVERSE":
                            yBackward()
                        yvalue = yvalue - 1


def CombineBack():
    global CombineDir
    global Entry_Box
    Entry_Box = "Value"
    CombineDir = "REVERSE"
    CombineOper()

def CombineForward():
    global CombineDir
    CombineDir = "FORWARD"
    CombineOper()
def PenPosition():
    global Z_Origin
    global Set_Position
    global ButtenPressed
    global Entry_Box
    ans = tk.messagebox.askquestion("System Confirmation","Do you really want to set Z Axis at Pen Position?")
    if ans == "yes":
        Entry_Box = "Empty"
        if float(Z_Origin) != 53.0:
            Set_Position = 53 - float(Z_Origin)
            if Set_Position > 0:
                ButtenPressed = "Z_Forward"
            else:
                ButtenPressed = "Z_Back"
            Z_Origin = str(float(Z_Origin) + float(Set_Position))
            X_ON()
        else:
            tk.messagebox.showinfo("System Notification", "Z Axis is already at Pen Position")
def ZerosPosition():
    global X_Origin
    global Y_Origin
    global Z_Origin
    global Set_Position
    global ButtenPressed
    global Entry_Box
    global CombineDir
    Entry_Box = "Empty"
    if float(Z_Origin) != 0:
        Set_Position = float(Z_Origin)
        ButtenPressed = "Z_Back"
        Z_Origin = "0"
        X_ON()
    if float(X_Origin) != 0 and float(Y_Origin) != 0:
        CombineDir = "REVERSE"
        CombineOper()
    elif float(X_Origin) != 0:
        Set_Position = float(X_Origin)
        ButtenPressed = "X_Back"
        X_Origin = "0"
        X_ON()
    elif float(Y_Origin) != 0:
        Set_Position = float(Y_Origin)
        ButtenPressed = "Y_Back"
        Y_Origin = "0"
        X_ON()
def DoneFunc():
    global DisData
    global OperationData
    global Sr
    global ButtenPressed
    global Set_Position
    global Entry_Box
    global DesignFrame
    global X_Origin
    global Y_Origin
    global Z_Origin
    x = 0
    y = 0
    z = 0
    ZerosPosition()
    Entry_Box = "Empty"
    progress_var = DoubleVar()
    progress = Progressbar(DesignFrame, orient=HORIZONTAL, length=300,variable=progress_var, mode='determinate',maximum = 100)
    progress.pack()
    progress.place(x=600, y=550)
    value = 100/Sr
    for i in range(Sr):
        progress_var.set(value*i)
        if OperationData[i] == "X-Forward":
            ButtenPressed = "X_Forward"
            Set_Position = DisData[i]
            x = x + float(Set_Position)
            X_Origin = x
            X_ON()
        if OperationData[i] == "Y-Forward":
            ButtenPressed = "Y_Forward"
            Set_Position = DisData[i]
            y = y + float(Set_Position)
            Y_Origin = y
            X_ON()
        if OperationData[i] == "Z-Down":
            ButtenPressed = "Z_Forward"
            Set_Position = DisData[i]
            z = z + float(Set_Position)
            Z_Origin = z
            X_ON()
        if OperationData[i] == "X-Reverse":
            ButtenPressed = "X_Back"
            Set_Position = DisData[i]
            x = x - float(Set_Position)
            X_Origin = x
            X_ON()
        if OperationData[i] == "Y-Reverse":
            ButtenPressed = "Y_Back"
            Set_Position = DisData[i]
            y = y - float(Set_Position)
            Y_Origin = y
            X_ON()
        if OperationData[i] == "Z-Up":
            ButtenPressed = "Z_Back"
            Set_Position = DisData[i]
            z = z - float(Set_Position)
            Z_Origin = z
            X_ON()
def Draw_Lines():
    global DesignFrame
    global ValueEntry
    global canvas
    global x_origin
    global y_origin
    global X_Origin
    global Y_Origin
    global ButtenPressed
    global pen_set
    global NoteLabel
    global Draw_Status
    xfactor = 3.5
    yfactor = 2
    if pen_set == 1:
        Draw_Status = "Draw"
        if ButtenPressed == "X-Forward":
            xvalue = float(x_origin) - float(ValueEntry.get())
            x_origin_set = float(xvalue) * xfactor + 10
            y_origin_set = float(y_origin) * yfactor + 10
            xLength = float(ValueEntry.get()) * xfactor
            length = x_origin_set + xLength
            canvas.create_line(x_origin_set, y_origin_set, length, y_origin_set, fill="white")

        elif ButtenPressed == "X-Reverse":
            xvalue = float(x_origin) + float(ValueEntry.get())
            x_origin_set = float(xvalue) * xfactor + 10
            y_origin_set = float(y_origin) * yfactor + 10
            xLength = float(ValueEntry.get()) * xfactor
            length = x_origin_set - xLength
            print(x_origin_set, y_origin_set, length)
            canvas.create_line(length, y_origin_set, x_origin_set, y_origin_set, fill="white")

        elif ButtenPressed == "Y-Forward":
            yvalue = float(y_origin) - float(ValueEntry.get())
            y_origin_set = float(yvalue) * yfactor + 10
            x_origin_set = float(x_origin) * xfactor + 10
            yLength = float(ValueEntry.get()) * yfactor
            y_length = y_origin_set + yLength
            canvas.create_line(x_origin_set, y_origin_set, x_origin_set, y_length, fill="white")

        elif ButtenPressed == "Y-Reverse":
            yvalue = float(y_origin) + float(ValueEntry.get())
            print(y_origin)
            y_origin_set = float(yvalue) * yfactor + 10
            x_origin_set = float(x_origin) * xfactor + 10
            yLength = float(ValueEntry.get()) * yfactor
            y_length = y_origin_set - yLength
            print(x_origin_set, y_origin_set, y_length)
            canvas.create_line(x_origin_set, y_origin_set, x_origin_set, y_length, fill="white")
        else:
            Draw_Status = "Move"
    else:
        Draw_Status = "Move"
        NoteLabel['text'] = "NOTE: Set Z-Pen Position or Bring Z down to 53mm to start drawing your Design"
        NoteLabel['fg'] = "red"
def Update_Table():
    global Paiddata
    global Sr
    global ComboData
    global ValueEntry
    global OperationData
    global DisData
    global Draw_Status
    OperationData.append(ComboData)
    DisData.append(ValueEntry.get())
    Sr += 1
    Paiddata.insert("", "end", tags="Frycook", text="", value=(str(Sr), ComboData, ValueEntry.get(),Draw_Status))

def Add_Operation_Fun():
    global ValueEntry
    global DoneButton
    global Y_Origin
    global Z_Origin
    global X_Origin
    global SingleCombo
    global BiCombo
    global DCombo
    global Operation
    global ComboData
    global Sr
    global OperationData
    global DisData
    global x_origin
    global y_origin
    global z_origin
    global SinglCheck
    global DoubleCheck
    global DCheck
    global AddButton
    global ButtenPressed
    global pen_set
    global NoteLabel
    error = 0
    for i in ValueEntry.get():
        if i.isdigit() or i == ".":
            pass
        else:
            error = 1
    if error == 0:
        if Operation == "Single":
            if SingleCombo.get() == "X-Forward":
                origin = 100 - int(ValueEntry.get())
                if origin >= 0:
                    x_origin = int(ValueEntry.get()) + x_origin
                    if x_origin <= 100:
                        ComboData = SingleCombo.get()
                        ButtenPressed = "X-Forward"
                        Draw_Lines()
                        Update_Table()
                    else:
                        tk.messagebox.showerror("INVALID DISTANCE", "Entered Value exceeds X Machine Maximum Length")
                else:
                    tk.messagebox.showerror("INVALID DISTANCE","Entered Value exceeds X Machine Maximum Length. You can enter upto "+str(100-int(X_Origin)))
            if SingleCombo.get() == "X-Reverse":
                origin = 100 - int(ValueEntry.get())
                if origin > 0:
                    if x_origin != 0:
                        x_origin = x_origin - float(ValueEntry.get())
                        if x_origin >= 0:
                            ComboData = SingleCombo.get()
                            ButtenPressed = "X-Reverse"
                            Draw_Lines()
                            Update_Table()
                        else:
                            tk.messagebox.showerror("INVALID DISTANCE",
                                                    "Entered Value exceeds X Machine Maximum Length")
                    else:
                        tk.messagebox.showerror("INVALID DISTANCE", "Ther is no reverse space available")
                else:
                    tk.messagebox.showerror("INVALID DISTANCE","Entered Value exceeds X Machine Maximum Length. You can enter upto "+str(int(X_Origin)))
            if SingleCombo.get() == "Y-Forward":
                origin = 200 - float(ValueEntry.get())
                if origin >= 0:
                    y_origin = float(ValueEntry.get()) + y_origin
                    if y_origin <= 200:
                        ComboData = SingleCombo.get()
                        ButtenPressed = "Y-Forward"
                        Draw_Lines()
                        Update_Table()
                    else:
                        tk.messagebox.showerror("INVALID DISTANCE", "Enter Value exceeds X Machine Maximum Length")
                else:
                    tk.messagebox.showerror("INVALID DISTANCE","Enter Value exceeds X Machine Maximum Length. You can enter upto "+str(200-int(Y_Origin)))
            if SingleCombo.get() == "Y-Reverse":
                origin = 200 - int(ValueEntry.get())
                if origin >= 0:
                    if y_origin != 0:
                        y_origin = y_origin - float(ValueEntry.get())
                        if y_origin >= 0:
                            ComboData = SingleCombo.get()
                            ButtenPressed = "Y-Reverse"
                            Draw_Lines()
                            Update_Table()
                        else:
                            tk.messagebox.showerror("INVALID DISTANCE", "Enter Value exceeds Y Machine Maximum Length")
                    else:
                        tk.messagebox.showerror("INVALID DISTANCE", "There is no available space for Y-Reverse")
                else:
                    tk.messagebox.showerror("INVALID DISTANCE","Enter Value exceeds Y Machine Maximum Length. You can enter upto"+str(int(Y_Origin)))
            if SingleCombo.get() == "Z-Up":
                origin = 53 - int(ValueEntry.get())
                if origin >= 0:
                    if z_origin != 0:
                        z_origin = z_origin - float(ValueEntry.get())
                        if z_origin >= 0:
                            ComboData = SingleCombo.get()
                            ButtenPressed = "Z-Reverse"
                            Draw_Lines()
                            Update_Table()
                    else:
                        tk.messagebox.showerror("INVALID DISTANCE", "Enter Value exceeds Z Machine Maximum Length")
                else:
                    tk.messagebox.showerror("INVALID DISTANCE",
                                            "Enter Value exceeds Z Machine Maximum Length. You can enter upto " + str(Z_Origin))
            if SingleCombo.get() == "Z-Down":
                origin = 53 - int(ValueEntry.get())
                if origin >= 0:
                    z_origin = float(ValueEntry.get()) + z_origin
                    if z_origin <= 53:
                        ComboData = SingleCombo.get()
                        ButtenPressed = "Z-Forward"
                        Draw_Lines()
                        Update_Table()
                    else:
                        tk.messagebox.showerror("INVALID DISTANCE", "Enter Value exceeds Z Machine Maximum Length")
                else:
                    tk.messagebox.showerror("INVALID DISTANCE",
                                            "Enter Value exceeds Z Machine Maximum Length. You can enter upto " + str(
                                                200 - float(Y_Origin)))

            if SingleCombo.get() == "Set Origin" or SingleCombo.get() == "Set Center" or SingleCombo.get() =="Z-Pen Position":
                ComboData = SingleCombo.get()
                Update_Table()
            SingleCombo['state'] = DISABLED
        Update_Design_Origin()
        SinglCheck['state'] = NORMAL
        DoubleCheck['state'] = NORMAL
        DCheck['state'] = NORMAL
        ValueEntry.delete(0,"end")
        ValueEntry['state'] = DISABLED
        AddButton['state'] = DISABLED
        DoneButton['state'] = NORMAL
        if z_origin == 53:
            pen_set = 1
            NoteLabel['text'] = "Z-Axis Has been now set to draw/drill your design"
            NoteLabel['fg'] = "green"
        else:
            pen_set = 0
    else:
        tk.messagebox.showerror("INVALID ENTRY","Please Enter Valid length")
def Check_Fun():
    global SingleCombo
    global SinglCheck
    global DoubleCheck
    global DCheck
    global ValueEntry
    global Operation
    Operation = "Single"
    if SinglCheck.state() == ('active', 'focus', 'selected', 'hover'):
        SingleCombo['state'] = "readonly"
        SinglCheck['text'] = "Disable Single Operation"
        ValueEntry['state'] = NORMAL
        DCheck['state'] = DISABLED
        DoubleCheck['state'] = DISABLED
        ValueEntry.focus()
    else:
        ValueEntry['state'] = DISABLED
        DCheck['state'] = NORMAL
        DoubleCheck['state'] = NORMAL
        SingleCombo['state'] = DISABLED
        SinglCheck['text'] = "Enable Single Operation"
def Check_Double_Fun():
    global BiCombo
    global SinglCheck
    global DoubleCheck
    global DCheck
    global ValueEntry
    global Operation
    Operation = "Double"
    if DoubleCheck.state() == ('active', 'focus', 'selected', 'hover'):
        BiCombo['state'] = "readonly"
        DoubleCheck['text'] = "Disable Double Operation"
        ValueEntry['state'] = NORMAL
        DCheck['state'] = DISABLED
        SinglCheck['state'] = DISABLED
        ValueEntry.focus()
    else:
        ValueEntry['state'] = DISABLED
        DCheck['state'] = NORMAL
        SinglCheck['state'] = NORMAL
        BiCombo['state'] = DISABLED
        DoubleCheck['text'] = "Enable Double Operation"
def Check_Design_Fun():
    global DCombo
    global SinglCheck
    global DoubleCheck
    global DCheck
    global Operation
    Operation = "Design"
    if DCheck.state() == ('active', 'focus', 'selected', 'hover'):
        DCombo['state'] = "readonly"
        DCheck['text'] = "Disable Designs"
        DoubleCheck['state'] = DISABLED
        SinglCheck['state'] = DISABLED
    else:
        DoubleCheck['state'] = NORMAL
        SinglCheck['state'] = NORMAL
        DCombo['state'] = DISABLED
        DCheck['text'] = "Enable Designs"
def value_Active(event):
    global AddButton
    AddButton['state'] = NORMAL
def Update_Design_Origin():
    global x_origin
    global y_origin
    global z_origin
    global xOriginEntry
    global yOriginEntry
    global zOriginEntry
    xOriginEntry['state'] = NORMAL
    yOriginEntry['state'] = NORMAL
    zOriginEntry['state'] = NORMAL
    xOriginEntry.delete(0,"end")
    yOriginEntry.delete(0, "end")
    zOriginEntry.delete(0, "end")
    xOriginEntry.insert(0,str(x_origin))
    yOriginEntry.insert(0, str(y_origin))
    zOriginEntry.insert(0, str(z_origin))
    xOriginEntry['state'] = "readonly"
    yOriginEntry['state'] = "readonly"
    zOriginEntry['state'] = "readonly"
def CreateDesignWin():
    global OperationData
    global DisData
    global Sr
    global x_origin
    global y_origin
    global z_origin
    global pen_set
    pen_set = 0
    x_origin = 0
    y_origin = 0
    z_origin = 0
    Sr = 0
    DisData = []
    OperationData = []
    DesignRoot = Tk()
    DesignRoot.title("LOGICAL DESIGN WINDOW BY MUBASHIR CO.")
    DesignRoot.geometry("1000x600")
    DesignRoot.wm_resizable(0,0)
    global DesignFrame
    DesignFrame = Frame(DesignRoot,bg="white",relief = RIDGE)
    DesignFrame.pack(fill=BOTH, expand=1)
    HeadFrame = LabelFrame(DesignFrame,bg="white",width=550,height=70)
    HeadFrame.pack()
    HeadFrame.place(x=25,y=10)
    HeadLabel=Label(HeadFrame,text="CREATE CUSTOM DESIGN (CCD)",bg="white",fg="gray",font=("Times 20 bold"))
    HeadLabel.pack()
    HeadLabel.place(x=50,y=10)
    BodyFrame=LabelFrame(DesignFrame,text="CREATE DESIGN",bg="white",fg="#871f78",width=550,height=500)
    BodyFrame.pack()
    BodyFrame.place(x=25,y=90)
    SingleLabel=Label(BodyFrame,text="UNI-DIRECTIONAL:",bg="white",fg="black",font=("Times 12 bold"))
    SingleLabel.pack()
    SingleLabel.place(x=20,y=20)
    global SingleCombo
    SingleCombo = ttk.Combobox(BodyFrame, width = 20,state=DISABLED, font=("Times 12 bold"),values = ["X-Forward","X-Reverse","Y-Forward","Y-Reverse",
                                                                                       "Z-Up","Z-Down"])
    SingleCombo.pack()
    SingleCombo.place(x=180,y=20)
    SingleCombo.current(1)
    global SinglCheck
    SinglCheck = ttk.Checkbutton(BodyFrame,command = Check_Fun,)
    SinglCheck.pack()
    SinglCheck.place(x=380,y=25)
    SinglCheck['text'] = "Enable Single Operation"

    MultiLabel = Label(BodyFrame, text="Bi-DIRECTIONAL:", bg="white", fg="black", font=("Times 12 bold"))
    MultiLabel.pack()
    MultiLabel.place(x=20, y=60)
    global BiCombo
    BiCombo = ttk.Combobox(BodyFrame, width=20, state=DISABLED, font=("Times 12 bold"),
                               values=["X-Forward, Y-Forward", "X-Reverse, Y-Forward", "X-Forward, Y-Reverse","X-Reverse, Y-Reverse"])
    BiCombo.pack()
    BiCombo.place(x=180, y=60)
    BiCombo.current(1)
    global DoubleCheck
    DoubleCheck = ttk.Checkbutton(BodyFrame, command=Check_Double_Fun, )
    DoubleCheck.pack()
    DoubleCheck.place(x=380, y=65)
    DoubleCheck['text'] = "Enable Double Operation"

    DLabel = Label(BodyFrame, text="ADD DESIGNS:", bg="white", fg="black", font=("Times 12 bold"))
    DLabel.pack()
    DLabel.place(x=20, y=100)
    global DCombo
    DCombo = ttk.Combobox(BodyFrame, width=20, state=DISABLED, font=("Times 12 bold"),
                           values=["Z-Pen Position","Set Origin","Set Center"])
    DCombo.pack()
    DCombo.place(x=180, y=100)
    DCombo.current(0)
    global DCheck
    DCheck = ttk.Checkbutton(BodyFrame, command=Check_Design_Fun, )
    DCheck.pack()
    DCheck.place(x=380, y=105)
    DCheck['text'] = "Enable Designs"

    ValueLabel = Label(BodyFrame,text="ENTER VALUE (mm):",bg="white",fg="black",font=("Times 12 bold"))
    ValueLabel.pack()
    ValueLabel.place(x=20,y=140)
    global ValueEntry
    ValueEntry = Entry(BodyFrame,width= 10,font=("Times 12 bold"),bg="white",borderwidth = 4,state=DISABLED)
    ValueEntry.pack()
    ValueEntry.place(x=180,y=140)
    ValueEntry.bind("<KeyPress>",value_Active)
    global AddButton
    AddButton = Button(BodyFrame,text="ADD",bg="#871f78",fg="white",font=("Times 12"),state=DISABLED,command=Add_Operation_Fun)
    AddButton.pack()
    AddButton.place(x=300,y=140)
    global DoneButton
    DoneButton = Button(BodyFrame, text="DONE", bg="#871f78", fg="white", font=("Times 12"), state=DISABLED,command=DoneFunc)
    DoneButton.pack()
    DoneButton.place(x=350, y=140)
    global DelButton
    DelButton = Button(BodyFrame, text="DELETE", bg="gray", fg="white", font=("Times 12"), state=DISABLED)
    DelButton.pack()
    DelButton.place(x=440, y=140)
    TableFrame = Frame(BodyFrame, width=100, height=10)
    TableFrame.pack()
    TableFrame.place(x=20, y=180)
    scroll = ttk.Scrollbar(TableFrame, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill=Y)

    Treestyle = ttk.Style()
    Treestyle.theme_use("default")
    Treestyle.configure("Treeview", background="silver", foreground="blue", fieldbackground="silver", rowheight=35,
                        relief="flat", font=("Times 16 bold"))
    global Paiddata
    Paiddata = ttk.Treeview(TableFrame, columns=(1, 2, 3, 4), show="headings", style="Treeview",
                            yscrollcommand=scroll)

    Paiddata.heading(1, text="Sr#")
    Paiddata.column(1, width=50)
    Paiddata.heading(2, text="OPERATION")
    Paiddata.column(2, width=250)
    Paiddata.heading(3, text="DISTANCE")
    Paiddata.column(3, width=100)
    Paiddata.heading(4, text="STATUS")
    Paiddata.column(4, width=100)
    # tags
    Paiddata.tag_configure("Treeview", background="black", foreground="white", font=("Times 12"))
    Paiddata.pack()
    scroll.config(command=Paiddata.yview)
    global canvas
    canvas = Canvas(DesignFrame, width=350, height=400, bg="black")
    canvas.pack()
    canvas.place(x=600, y=5)
    global NoteLabel
    NoteLabel = Label(BodyFrame,bg="white",wraplength=500,font=("Times 12 bold"))
    NoteLabel.pack()
    NoteLabel.place(x=20,y=420)
    OriginFrame = LabelFrame(DesignFrame,width = 360,height=100,bg="white",fg="gray",text="COORDINATES")
    OriginFrame.pack()
    OriginFrame.place(x=600,y=420)
    xLabel = Label(OriginFrame,text="X-Machine",bg="white",fg="black",font=("Times 12"))
    xLabel.pack()
    xLabel.place(x=20,y=10)
    yLabel = Label(OriginFrame, text="Y-Machine", bg="white", fg="black", font=("Times 12"))
    yLabel.pack()
    yLabel.place(x=120, y=10)
    zLabel = Label(OriginFrame, text="Z-Machine", bg="white", fg="black", font=("Times 12"))
    zLabel.pack()
    zLabel.place(x=220, y=10)
    global xOriginEntry
    global yOriginEntry
    global zOriginEntry
    xOriginEntry = Entry(OriginFrame,width = 8,bg="white",font=("Times 12"),borderwidth = 4)
    xOriginEntry.pack()
    xOriginEntry.place(x=20,y=40)
    yOriginEntry = Entry(OriginFrame, width=8, bg="white", font=("Times 12"), borderwidth=4)
    yOriginEntry.pack()
    yOriginEntry.place(x=120, y=40)
    zOriginEntry = Entry(OriginFrame, width=8, bg="white", font=("Times 12"), borderwidth=4)
    zOriginEntry.pack()
    zOriginEntry.place(x=220, y=40)
    Update_Design_Origin()
def Panel():
    global Startframe
    global ButtenPressed
    global checkstatus
    global CombineDir
    global Entry_Box
    Entry_Box = "None"
    CombineDir = ""
    checkstatus = 0
    ButtenPressed = ""
    PanelFrame = LabelFrame(Startframe, relief=RIDGE, text="CONTROL PANEL", width=790, height=500, borderwidth=5,
                             bg="white", fg="#871f78")
    PanelFrame.pack()
    PanelFrame.place(x=100, y=50)
    OnPenButton = Button(PanelFrame,text="Z-Pen Position",wraplength=80,font=("Times 12"),fg="white",image=penIcon,compound=TOP,bg="#871f78",command=PenPosition,width = 60)
    OnPenButton.pack()
    OnPenButton.place(x=710,y=10)
    ZeroButton = Button(PanelFrame,wraplength=80, text="Set Zero Position", font=("Times 12"), fg="white", image=ZeroPosition, compound=TOP,
                         bg="#871f78", command=ZerosPosition, width=60)
    ZeroButton.pack()
    ZeroButton.place(x=710, y=120)
    SingleFrame = LabelFrame(PanelFrame,relief=RIDGE,width=320,height=400,borderwidth=5,bg="white",fg="#871f78")
    SingleFrame.pack()
    SingleFrame.place(x=10,y=10)
    Y_Frame = LabelFrame(PanelFrame, relief=RIDGE, width=320, height=400, borderwidth=5, bg="white",
                         fg="#871f78")
    Y_Frame.pack()
    Y_Frame.place(x=380, y=10)
    Title = Label(SingleFrame, text="Enter Distance (mm): ", bg="white", fg="black", font=("Times", 12,"bold"))
    Title.pack()
    Title.place(x=10, y=10)
    global DisEntry
    DisEntry = tk.Entry(SingleFrame, borderwidth=5, width=12, font=("Times", 14), bg="white", fg="black")
    DisEntry.pack()
    DisEntry.place(x=160, y=10)
    DisEntry.focus_force()
    DisEntry.bind("<KeyPress>", checkEntry)
    CTitle = Label(Y_Frame, text="Enter Distance (mm): ", bg="white", fg="black", font=("Times", 12, "bold"))
    CTitle.pack()
    CTitle.place(x=10, y=10)
    global CDisEntry
    CDisEntry = tk.Entry(Y_Frame, borderwidth=5, width=12, font=("Times", 14), bg="white", fg="black")
    CDisEntry.pack()
    CDisEntry.place(x=160, y=10)
    CDisEntry.focus_force()
    CDisEntry.bind("<KeyPress>", CheckEntry)
    XStep = Label(Y_Frame, text="Enter X-STEP(mm): ", bg="white", fg="black", font=("Times", 12, "bold"))
    XStep.pack()
    XStep.place(x=10, y=40)
    global XSTEPEntry
    XSTEPEntry = tk.Entry(Y_Frame, borderwidth=5, width=12, font=("Times", 14), bg="white", fg="black")
    XSTEPEntry.pack()
    XSTEPEntry.place(x=160, y=40)
    XSTEPEntry.focus_force()
    XSTEPEntry.bind("<KeyPress>", Check_X_STEP)
    YStep = Label(Y_Frame, text="Enter Y-STEP(mm): ", bg="white", fg="black", font=("Times", 12, "bold"))
    YStep.pack()
    YStep.place(x=10, y=80)
    global YSTEPEntry
    YSTEPEntry = tk.Entry(Y_Frame, borderwidth=5, width=12, font=("Times", 14), bg="white", fg="black")
    YSTEPEntry.pack()
    YSTEPEntry.place(x=160, y=80)
    YSTEPEntry.focus_force()
    YSTEPEntry.bind("<KeyPress>", Check_Y_STEP)
    global X_Forward
    global X_Back
    global Y_Forward
    global Y_Back
    global Z_Forward
    global Z_Back
    X_Forward = Button(SingleFrame, text="X-FORWARD", bg="#871f78",width=20, fg="white", font=("Times", 12, "bold"),command=X_FORWARD_Pressed,state = DISABLED)
    X_Forward.pack()
    X_Forward.place(x=50, y=60)
    X_Back = Button(SingleFrame, text="X-REVERSE", bg="#871f78", width=20, fg="white", font=("Times", 12, "bold"),
                       command=X_BACK_Pressed,state = DISABLED)
    X_Back.pack()
    X_Back.place(x=50, y=100)
    Y_Forward = Button(SingleFrame, text="Y-REVERSE", bg="#871f78", width=20, fg="white", font=("Times", 12, "bold"),
                       command=Y_BACK_Pressed,state = DISABLED)
    Y_Forward.pack()
    Y_Forward.place(x=50, y=180)
    Y_Back = Button(SingleFrame, text="Y-FORWARD", bg="#871f78", width=20, fg="white", font=("Times", 12, "bold"),
                       command=Y_FORWARD_Pressed,state = DISABLED)
    Y_Back.pack()
    Y_Back.place(x=50, y=140)
    Z_Forward = Button(SingleFrame, text="Z-DOWN", bg="#871f78", width=20, fg="white", font=("Times", 12, "bold"),
                       command=Z_FORWARD_Pressed, state=DISABLED)
    Z_Forward.pack()
    Z_Forward.place(x=50, y=220)
    Z_Back = Button(SingleFrame, text="Z-UP", bg="#871f78", width=20, fg="white", font=("Times", 12, "bold"),
                    command=Z_BACK_Pressed, state=DISABLED)
    Z_Back.pack()
    Z_Back.place(x=50, y=260)

    global CombineBtn
    global CombineBtn_Back
    CombineBtn = Button(Y_Frame,text="COMBINE FORWARD: X-Y",bg="gray",fg="white",width = 25,font=("Times 14 bold"),state=DISABLED,command=CombineForward)
    CombineBtn.pack()
    CombineBtn.place(x=10,y=140)
    CombineBtn_Back = Button(Y_Frame, text="COMBINE REVERSE: X-Y", bg="gray",width = 25, fg="white", font=("Times 14 bold"),
                        state=DISABLED, command=CombineBack)
    CombineBtn_Back.pack()
    CombineBtn_Back.place(x=10, y=180)
def Update_Origin():
    global xPosEntry
    global yPosEntry
    global zPosEntry
    global X_Origin
    global Y_Origin
    global Z_Origin
    xPosEntry['state'] = NORMAL
    yPosEntry['state'] = NORMAL
    zPosEntry['state'] = NORMAL
    xPosEntry.delete(0,"end")
    yPosEntry.delete(0, "end")
    zPosEntry.delete(0, "end")
    xPosEntry.insert(0,X_Origin)
    yPosEntry.insert(0, Y_Origin)
    zPosEntry.insert(0, Z_Origin)
    xPosEntry['state']="readonly"
    yPosEntry['state'] = "readonly"
    zPosEntry['state'] = "readonly"
def Start():
    global status
    global frame
    frame.destroy()
    global Startframe
    global Window
    Window = "Start"
    Startframe = Frame(root, relief=RIDGE, bg="white", )
    Startframe.pack(fill=BOTH, expand=1)

    statusLabel1 = Label(Startframe, text="Status:   ", bg="white", fg="#871f78", font=("Times", 12, "bold"))
    statusLabel1.pack()
    statusLabel1.place(x=770, y=20)
    statusTag1 = Label(Startframe, text=status, bg="white", font=("Times", 12, "bold"))
    statusTag1.pack()
    statusTag1.place(x=820, y=20)
    if status == "OFFLINE":
        statusTag1['fg'] = "red"
    else:
        statusTag1['fg'] = "green"

    Title = Label(Startframe,text="CNC MILLING MACHINE CONTROL PANEL",bg="white",fg="#871f78",font=("Times",18,"bold"))
    Title.pack()
    Title.place(x=240,y=20)
    tabFrame = LabelFrame(Startframe,relief=RIDGE,text="WELCOME TO BOARD",width = 790, height = 500,borderwidth=5,bg="white",fg="#871f78")
    tabFrame.pack()
    tabFrame.place(x=100,y=50)
    sample = Button(Startframe,text="SAMPLES",image=SampleIcon,compound=TOP,bg="#871f78",fg="white",font=("Times",12,"bold"),border=0,relief=FLAT,command=Samples)
    sample.pack()
    sample.place(x=10,y=50)
    ControlPanel = Button(Startframe, text="CONTROL",image=ControlIcon,compound=TOP, bg="#871f78", fg="white", font=("Times", 12, "bold"), border=0,
                    relief=FLAT, command=Panel)
    ControlPanel.pack()
    ControlPanel.place(x=10, y=150)
    CreateBtn = Button(Startframe, text="Create Desing",image=CreateIcon,compound=TOP, bg="#871f78", fg="white", font=("Times 12 bold"), border=0,
                       relief=FLAT,command = CreateDesignWin)
    CreateBtn.pack()
    CreateBtn.place(x=10, y=250)
    OriginFrame = LabelFrame(Startframe,text="Origin",bg="white",fg="gray",width = 90,height = 195)
    OriginFrame.pack()
    OriginFrame.place(x=5,y=355)
    xLabel = Label(OriginFrame,text="X_Position",bg="white",fg="gray",font=("Times 10"))
    xLabel.pack()
    xLabel.place(x=10,y=10)
    yLabel = Label(OriginFrame, text="Y_Position", bg="white", fg="gray", font=("Times 10"))
    yLabel.pack()
    yLabel.place(x=10, y=60)
    zLabel = Label(OriginFrame, text="Z_Position", bg="white", fg="gray", font=("Times 10"))
    zLabel.pack()
    zLabel.place(x=10, y=110)
    global xPosEntry
    global yPosEntry
    global zPosEntry
    xPosEntry = Entry(OriginFrame,width = 7,font=("Times 12"),bg="white",borderwidth = 4)
    xPosEntry.pack()
    xPosEntry.place(x=10,y=35)
    yPosEntry = Entry(OriginFrame, width=7, font=("Times 12"), bg="white", borderwidth=4)
    yPosEntry.pack()
    yPosEntry.place(x=10, y=85)
    zPosEntry = Entry(OriginFrame, width=7, font=("Times 12"), bg="white", borderwidth=4)
    zPosEntry.pack()
    zPosEntry.place(x=10, y=135)
    Update_Origin()
    BackBtn = Button (Startframe,text="Back",bg="white",compound=LEFT,image=BackButton,command=Start_Frame,relief = FLAT)
    BackBtn.pack()
    BackBtn.place(x=5,y=560)


root = Tk()
root.title("CNC MILLING MACHINE DESKTOP APPLICATION")
root.geometry('900x600')
root.wm_resizable(0,0)
global board
global status
status = "ONLINE"

def Start_Frame():
    global frame
    global Window
    global Startframe
    if Window == "Start":
        Startframe.destroy()
        Window = "NONE"
    frame = Frame(root, relief=RIDGE, bg="white", )
    frame.pack(fill=BOTH, expand=1)
    Front = Label(frame, image=LogoImg, relief=FLAT, border=0, )
    Front.pack(side=TOP)
    Front.place(x=100, y=100)

    statusLabel = Label(frame, text="Status:   ", bg="white", fg="#871f78", font=("Times", 12, "bold"))
    statusLabel.pack()
    statusLabel.place(x=700, y=20)
    start = Button(frame, text="Initialize", bg="#871f78", font=("Times", 15, "bold"), fg="white", relief=FLAT,
                   border=5, command=Start)
    start.pack()
    start.place(x=400, y=400)

    global statusTag
    statusTag = Label(frame, bg="white", font=("Times", 12, "bold"))
    statusTag.pack()
    statusTag.place(x=770, y=20)
LogoImg = PhotoImage(file="hiclipart.png")
ControlIcon = PhotoImage(file = "settings-11-48.png")
SampleIcon = PhotoImage(file = "briefcase-4-48.png")
BackButton = PhotoImage(file="arrow-96-32.png")
redo = PhotoImage(file="redo-2-24.png")
penIcon = PhotoImage(file="edit-6-32.png")
ZeroPosition = PhotoImage(file="emoticon-37-32.png")
CreateIcon = PhotoImage (file="MillingIcon.png")
global Window
Window = "NONE"
Start_Frame()

def DataBase():
    global X_Origin
    global Y_Origin
    global Z_Origin
    conn = sqlite3.connect("FYP_DATABASE.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Origin(Sr TEXT, X_Origin TEXT, Y_Origin TEXT, Z_Origin TEXT)")
    #cursor.execute("INSERT INTO Origin(Sr, X_Origin, Y_Origin, Z_Origin) VALUES (?,?,?,?)",("1","0","0","0"))
    cursor.execute("SELECT X_Origin,Y_Origin ,Z_Origin FROM Origin WHERE Sr = ?",("1"))
    i = cursor.fetchone()
    X_Origin = i[0]
    Y_Origin = i[1]
    Z_Origin = i[2]
    conn.commit()
    cursor.close()
    conn.close()
DataBase()

Make_Connection()

mainloop()




