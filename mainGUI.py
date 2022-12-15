import pyvisa
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from scipy import fftpack

from distutils.cmd import Command
from turtle import position
import numpy as np   ### mathematic library
import matplotlib.pyplot as plt  ### generate figure
import matplotlib.animation as animation   ### plot graph wiht real time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg ## add figures onto GUI


font1=("Arial",20)
 
fig=plt.figure()
ax1=fig.add_subplot(211)
ax2=fig.add_subplot(212)

# device define
def findDevice():
    ins=pyvisa.ResourceManager()
    ins_list=ins.list_resources()
    global oscil, DC
    for i in ins_list:
        device=ins.open_resource(str(i))
        idn=device.query("*IDN?")
        if idn[0]=="T":
            oscil=device
        if idn[0]=="R":
            DC=device

class mainControl:
    def __init__(self):
        findDevice()
        global CH 
        CH=ch.get()
        oscil.write(f"DATa:SOUrce {CH}")
        oscil.write("WFMInpre:ENCdg BINary")

    def openDC(self):
        filePath=r"C:\Users\kritt\NSCproject\DCcontrol.py"
        exec(open(filePath).read())

# animation graph
    def animate(self,i):

        samp_rate=oscil.query("WFMOutpre:RECOrdlength?")
        samp_rate=int(samp_rate)
        horiScale=float(oscil.query("HORizontal:SCAle?"))

        dt=15*horiScale/samp_rate
        data_unscale = oscil.query_binary_values("CURVe?",datatype='b')
        y_resolution=float(oscil.query("WFMOutpre:YMUlt?"))
        t_resolution=float(oscil.query("WFMOutpre:XINcr?"))
        x = range(0, len(data_unscale))
        data_scale=np.dot(data_unscale,y_resolution)
        t=np.dot(x,t_resolution)

        curve = fftpack.fft(data_scale)
        amp=np.sqrt((curve.real**2)+(curve.imag**2))
        amp /= len(data_scale) / 2
        freq=np.linspace(0,len(data_scale),len(data_scale))

        xf=fftpack.fftfreq(samp_rate,dt)[:samp_rate//2]
        ax1.cla()
        ax2.cla()
        ax1.set_title("Raw graph")
        ax1.plot(t,data_scale)
        ax2.set_title("Fourier graph")
        ax2.plot(xf, 2.0/samp_rate * np.abs(curve[0:samp_rate//2]),color="#ffba08")
        fig.tight_layout(pad=5.0)
        ax1.set_xlabel("Time",fontsize=10)
        ax1.set_ylabel("Amplitude", fontsize=10)
        ax2.set_xlabel("Frequency",fontsize=10)
        ax2.set_ylabel("Amplitude", fontsize=10)
        ax2.set_xlim(0,10000)

    def ani(self):
        global ani
        ani=animation.FuncAnimation(fig,self.animate,interval=200,repeat=True)

    pause = True
    def pause_animation(self):
        self.ani()
        if self.pause==True:
            ani.pause()
            self.pause = False
        else:
            ani.resume()
            self.pause = True

    def query(self,data):
        info=oscil.query(f":{data}? {CH}")
        info=info.replace("\n","")
        
        try:
            info=float(info)
            info=round(info,2)
        except ValueError:
            pass

    def statusCH(self):
        global chanel
        chanel=["CH1","CH2","CH3","CH4"]
        for i in status_list:
            if i==CH:
                self.write(f"SELect:{i} ON")
                onChanel=CH
            else:
                self.write(f"SELect:{i} OFF")

        labelCH.config(f"Chanel {onChanel} ON")

        
# GUI Section
mainWindow=tk.Tk()
mainWindow.title("Control")
mainWindow.geometry("1920x1080")

def quitRoot(callback=None):
    mainWindow.destroy()
    return

mainWindow.bind("<Escape>",quitRoot)

# variable
ch=tk.StringVar(mainWindow,"CH4")

mainCont=mainControl()

# Interface
menubar=tk.Menu(mainWindow)
DeviceControl=tk.Menu(menubar)
# DeviceControl.add_command(label="Oscilloscope",command=None)
DeviceControl.add_command(label="DC Supply",command=mainCont.openDC)
DeviceControl.add_separator()
DeviceControl.add_command(label="Exit",command=mainWindow.quit)
menubar.add_cascade(label="Control Device", menu=DeviceControl)

refresh=tk.Menu(menubar)
refresh.add_command(label="Re-connect devices",command=findDevice)
menubar.add_cascade(label="Refresh", menu=refresh)

mainWindow.config(menu=menubar)

label_frame=tk.Frame(mainWindow,height=100)

header=tk.Label(label_frame, text="Graph for voltage mesured and fourier transformation graph",height=3,width=1080,bg="#c6ac8f",font=("Arial",15)).pack(side="top",fill="both",pady=20,expand=True)
label_frame.pack(side="top")

# Select chanel to display buttons
radiobuttonFrm=tk.Frame(mainWindow)
ch1=tk.Radiobutton(radioFrm,text="CH1",variable=ch,value="CH1").pack(side="left")
ch2=tk.Radiobutton(radioFrm,text="CH2",variable=ch,value="CH2").pack(side="left")
ch3=tk.Radiobutton(radioFrm,text="CH3",variable=ch,value="CH3").pack(side="left")
ch4=tk.Radiobutton(radioFrm,text="CH3",variable=ch,value="CH4").pack(side="left")
tk.Button(radioFrm,text="ON/OFF Chanel",command=mainCont.statusCH,bd=2,width=15,height=2,bg="#f5ebe0").pack(side="left",padx=15)
radioFrm.pack(side="top",pady=15)

labelCH=tk.Label(mainWindow)
labelCH.pack(side="top")
mainCont.statusCH()


graph_frame=tk.Frame(mainWindow)

canvas = FigureCanvasTkAgg(fig, master=mainWindow)
canvas.get_tk_widget().pack(side='top',ipadx=100,ipady=50)
onButton=tk.Button(graph_frame,text="On/Off Animation",command=mainCont.pause_animation).pack(side="top")
graph_frame.pack(side="top")


mainWindow.mainloop()
oscil.close()
# DC.close()