import tkinter as tk
from tkinter import messagebox
import pyvisa
from playsound import playsound
import os, subprocess


# Function
def findDevice():
    ins=pyvisa.ResourceManager()
    ins_list=ins.list_resources()
    global oscil
    for i in ins_list:
        device=ins.open_resource(str(i))
        idn=device.query("*IDN?")
        if idn[0]=="R":
            DC=device

def findPath(self,filename):
    cwd=os.getcwd()
    filepath=os.path.abspath(os.path.join(cwd, filename))
    return filepath


# Class and Function
class oscilControl:

    def __init__(self):
        findDevice()
        global CH
        CH=ch.get()

    def playSelect(self):
        filepath=findPath("material/audio/jump.wav")
        playsound(filepath)

    def playSubmit(self):
        filepath=findPath("material/audio/select2.wav")
        playsound(filepath)

    def queryCH(self,data):
        info=oscil.query(f"{CH}:{data}?")
        info=info.replace("\n","")
        
        try:
            info=float(info)
            info=round(info,2)
        except ValueError:
            pass
        
        return info

    def query(self,data):
        info=oscil.query(f"{data}?")
        info=info.replace("\n","")
        
        try:
            info=float(info)
            info=round(info,2)
        except ValueError:
            pass
        
        return info

    def SelectCH(self):
        select=f"Now selecting Chanel {CH}"
        labelCH.config(text=select)
        self.playSelect() 

    def StatusCH(self):
        global chanel
        chanel=["CH1","CH2","CH3","CH4"]
        for i in chanel:
            if i==CH:
                self.write(f"SELect:{i} ON")
                onChanel=CH
            else:
                self.write(f"SELect:{i} OFF")

        labelCHst.config(f"Chanel {onChanel} ON")
        
        self.playSelect()

    def ShowInfo(self):

        scale_info=self.queryCH("SCAle")
        position_info=self.queryCH("POSition")
        horiScale_info=self.query("HORizontal:SCAle")
        horiInterval_info=self.query("WFMInpre:XINcr")
        verticalScale_info=self.query("WFMInpre:YMUlt")

        scaleLabel.config(text=str(scale_info))
        positionLabel.config(text=str(position_info))
        horiScaleLabel.config(text=str(horiScale_info))
        horiIntervalLabel.config(text=str(horiInterval_info))
        verticalScaleLabel.config(text=str(verticalScale_info))

    def SetControl(self):
        scale_data=float(scale.get())
        position_data=float(position.get())
        horiScale_data=float(horiScale.get())
        horiInterval_data=float(horiInterval.get())
        verticalScale_data=float(verticalScale.get())

        def SetValue(type,value):
            text=f"{type} {value}"
            oscil.write(text)
        
        def SetValueCH(type,value):
            text=f"{CH}:{type} {value}"
            oscil.write(text)

        SetValueCH("SCAle",scale_data)    
        SetValueCH("POSition",position_data)    
        SetValue("HORizontal:SCAle",horiScale_data)    
        SetValue("WFMInpre:XINcr",horiInterval_data)    
        SetValue("WFMInpre:YMUlt",verticalScale_data)    

        self.ShowInfo()
        self.playComplete()

# Create window
oscilWindow=tk.Tk()
oscilWindow.geometry("800x1080")
oscilWindow.title("DC Supply Control")
oscilWindow.iconbitmap(findPath("material/picture/oscil.ico"))

def quitRoot(callback=None):
    oscilWindow.destroy()
    return

oscilWindow.bind("<Escape>",quitRoot)

# variable
ch=tk.StringVar(oscilWindow,"CH1")
oscilCont=oscilControl()

# Frame
headerFrm=tk.Frame(oscilWindow)
tk.Label(headerFrm,text="Oscilloscope Control System",height=3,width=1080,bg="#c6ac8f",font=("Arial",15)).pack(side="top",fill="both",pady=20,expand=True)
headerFrm.pack(side="top")

contentFrm=tk.Frame(oscilWindow)

# Select chanel radio buttons
radioFrm=tk.Frame(contentFrm)
ch1=tk.Radiobutton(radioFrm,text="CH1",variable=ch,value="CH1",command=oscilCont.SelectCH).pack(side="left")
ch2=tk.Radiobutton(radioFrm,text="CH2",variable=ch,value="CH2",command=oscilCont.SelectCH).pack(side="left")
ch3=tk.Radiobutton(radioFrm,text="CH3",variable=ch,value="CH3",command=oscilCont.SelectCH).pack(side="left")
tk.Button(radioFrm,text="On/Off Chanel",command=oscilCont.StatusCH,bd=2,width=15,height=2,bg="#f5ebe0").pack(side="left",padx=15)
radioFrm.pack(side="top",pady=15)

labelCH=tk.Label(contentFrm)
labelCH.pack(side="top")

labelCHst=tk.Label(contentFrm)
labelCHst.pack(side="top")

oscilCont.SelectCH()
oscilCont.StatusCH()


# Input control DC supply
entry1Frm=tk.Frame(contentFrm)
tk.Label(entry1Frm,text="Scale",width=20).pack(side="left")
scale=tk.Entry(entry1Frm,width=50,justify="right")
scale.pack(side="left")
entry1Frm.pack(side="top",pady=5)

entry2Frm=tk.Frame(contentFrm)
tk.Label(entry2Frm,text="Position",width=20).pack(side="left")
position=tk.Entry(entry2Frm,width=50,justify="right")
position.pack(side="left")
entry2Frm.pack(side="top",pady=5)

entry3Frm=tk.Frame(contentFrm)
tk.Label(entry3Frm,text="Horizontal Scale",width=20).pack(side="left")
horiScale=tk.Entry(entry3Frm,width=50,justify="right")  
horiScale.pack(side="left")
entry3Frm.pack(side="top",pady=5)

entry4Frm=tk.Frame(contentFrm)
tk.Label(entry4Frm,text="Horizontal Interval",width=20).pack(side="left")
horiInterval=tk.Entry(entry4Frm,width=50,justify="right")
horiInterval.pack(side="left")
entry4Frm.pack(side="top",pady=5)

entry5Frm=tk.Frame(contentFrm)
tk.Label(entry5Frm,text="Vertical Scale",width=20).pack(side="left")
verticalScale=tk.Entry(entry5Frm,width=50,justify="right")
verticalScale.pack(side="left")
entry5Frm.pack(side="top",pady=5)

tk.Button(contentFrm,text="SET",command=oscilCont.SetControl,width=15).pack(side="top",pady=10)

# Info Vertical Scale
infoScaleFrm=tk.Frame(contentFrm)
tk.Label(infoScaleFrm,text="Vertical Scale value",width=20).pack(side="left")
scaleLabel=tk.Label(infoScaleFrm,bg="#e3d5ca")
scaleLabel.pack(side="left",ipadx=30,padx=10)
tk.Label(infoScaleFrm,text="V").pack(side="left")
infoScaleFrm.pack(side="top",pady=10)

# Info Vertical Position
infoPositionFrm=tk.Frame(contentFrm)
tk.Label(infoPositionFrm,text="Vertical Position value",width=20).pack(side="left")
positionLabel=tk.Label(infoPositionFrm,bg="#e3d5ca")
positionLabel.pack(side="left",ipadx=30,padx=10)
tk.Label(infoPositionFrm,text="V").pack(side="left")
infoPositionFrm.pack(side="top",pady=5)

# Info Horizontal Scale
infoHoriScaleFrm=tk.Frame(contentFrm)
tk.Label(infoHoriScaleFrm,text="Horizontal Scale value",width=20).pack(side="left")
horiScaleLabel=tk.Label(infoHoriScaleFrm,bg="#e3d5ca")
horiScaleLabel.pack(side="left",ipadx=30,padx=10)
tk.Label(infoHoriScaleFrm,text="V").pack(side="left")
infoHoriScaleFrm.pack(side="top",pady=10)

# Info Horizontal Interval
infoHoriIntervalFrm=tk.Frame(contentFrm)
tk.Label(infoHoriIntervalFrm,text="Y-axis Waveform Interval",width=20).pack(side="left")
horiIntervalLabel=tk.Label(infoHoriIntervalFrm,bg="#e3d5ca")
horiIntervalLabel.pack(side="left",ipadx=30,padx=10)
tk.Label(infoHoriIntervalFrm,text="V").pack(side="left")
infoHoriIntervalFrm.pack(side="top",pady=5)

# Info Vertical Position
infoVerticalScaleFrm=tk.Frame(contentFrm)
tk.Label(infoVerticalScaleFrm,text="X-axis Waveform Scale",width=20).pack(side="left")
verticalScaleLabel=tk.Label(infoVerticalScaleFrm,bg="#e3d5ca")
verticalScaleLabel.pack(side="left",ipadx=30,padx=10)
tk.Label(infoVerticalScaleFrm,text="V").pack(side="left")
infoVerticalScaleFrm.pack(side="top",pady=5)


oscilCont.ShowInfo()
contentFrm.pack(side="top",expand=True,fill="both")





oscilWindow.mainloop()