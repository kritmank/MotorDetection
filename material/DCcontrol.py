import tkinter as tk
from tkinter import messagebox
import pyvisa
from playsound import playsound
import os, subprocess


# Function
def findDevice():
    ins=pyvisa.ResourceManager()
    ins_list=ins.list_resources()
    global DC
    for i in ins_list:
        device=ins.open_resource(str(i))
        idn=device.query("*IDN?")
        if idn[0]=="R":
            DC=device

# Class and Function
class DCcontrol:

    def __init__(self):
        findDevice()
        global CH
        CH=ch.get()
    
    def findPath(self,filename):
        cwd=os.getcwd()
        filepath=os.path.abspath(os.path.join(cwd, filename))
        return filepath

    def playSelect(self):
        filepath=self.findPath("Audio/jump.wav")
        playsound(filepath)

    def playSubmit(self):
        filepath=self.findPath("Audio/select2.wav")
        playsound(filepath)

    def query(self,data):
        info=DC.query(f":{data}? {CH}")
        info=info.replace("\n","")
        
        try:
            info=float(info)
            info=round(info,2)
        except ValueError:
            pass

        return info

    def SelectCH(self):
        select=f"Now selecting Chanel {CH}"
        chanel=f"INST {CH}"
        labelCH.config(text=select)
        DC.write(chanel)
        self.playSelect() 

    def StatusCH(self):
        status=self.query("OUTP")
        
        if status=="ON":
            DC.write(f":OUTP {CH},OFF")
            status="OFF"

        elif status=="OFF":
            DC.write(f":OUTP {CH},ON")
            status="ON"

        text=f"Your {CH} status is {status}"
        print(text)
        labelCHst.config(text=text)  
        self.playSubmit()

    def FindChanelStatus(self):
        status=self.query("OUTP")
        text=f"Your {CH} status is {status}"    
        labelCHst.config(text=text)

    def setStatus(self,data,label):
        status=self.query(f"OUTP:{data}")

        if status=="ON":
            DC.write(f":{data} {CH},OFF")
            status="OFF"

        elif status=="OFF":
            DC.write(f":{data} {CH},ON")
            status="ON"

        text=f"Your {CH} {data} is {status}"
        label.config(text=text) 

    def setOVP(self):
        self.setStatus("OVP",labelOVP)

    def setOCP(self):
        self.setStatus("OCP",labelOCP)

    def ShowInfo(self):
        volt_info=self.query("VOLT")
        curr_info=self.query("CURR")
        voltP_info=self.query(":VOLT:PROT")
        currP_info=self.query(":CURR:PROT")

        VoltLabel.config(text=str(volt_info))
        CurrLabel.config(text=str(curr_info))
        VoltPLabel.config(text=str(voltP_info))
        CurrPLabel.config(text=str(currP_info))

    def SetControl(self):
        volt_data=float(volt.get())
        curr_data=float(curr.get())
        voltPT_data=float(voltPT.get())
        currPT_data=float(currPT.get())

        text_v=f":VOLT {volt_data}"
        text_c=f":CURR {curr_data}"
        text_vp=f":VOLT:PROT {voltPT_data}"
        text_cp=f":CURR:PROT {currPT_data}"

        DC.write(text_v)
        DC.write(text_c)
        DC.write(text_cp)
        DC.write(text_vp)
        
        self.ShowInfo()
        self.playComplete()


# Create window
DcWindow=tk.Tk()
DcWindow.geometry("800x1080")
DcWindow.title("DC Supply Control")

def quitRoot(callback=None):
    DcWindow.destroy()
    return

DcWindow.bind("<Escape>",quitRoot)

# variable
ch=tk.StringVar(DcWindow,"CH1")
DCcont=DCcontrol()

# Frame
headerFrm=tk.Frame(DcWindow)
tk.Label(headerFrm,text="DC Supply Control System",height=3,width=1080,bg="#c6ac8f",font=("Arial",15)).pack(side="top",fill="both",pady=20,expand=True)
headerFrm.pack(side="top")

contentFrm=tk.Frame(DcWindow)

# Select chanel radio buttons
radioFrm=tk.Frame(contentFrm)
ch1=tk.Radiobutton(radioFrm,text="CH1",variable=ch,value="CH1",command=DCcont.SelectCH).pack(side="left")
ch2=tk.Radiobutton(radioFrm,text="CH2",variable=ch,value="CH2",command=DCcont.SelectCH).pack(side="left")
ch3=tk.Radiobutton(radioFrm,text="CH3",variable=ch,value="CH3",command=DCcont.SelectCH).pack(side="left")
tk.Button(radioFrm,text="On/Off Chanel",command=DCcont.StatusCH,bd=2,width=15,height=2,bg="#f5ebe0").pack(side="left",padx=15)
radioFrm.pack(side="top",pady=15)

labelCH=tk.Label(contentFrm)
labelCH.pack(side="top")

labelCHst=tk.Label(contentFrm)
labelCHst.pack(side="top")

DCcont.SelectCH()
DCcont.FindChanelStatus()

# Device Data
OVPst=DC.query(f":OUTP:OVP? {CH}")
OVPst=OVPst.replace("\n","")
OCPst=DC.query(f":OUTP:OCP? {CH}")
OCPst=OCPst.replace("\n","")

# Input control DC supply
entry1Frm=tk.Frame(contentFrm)
tk.Label(entry1Frm,text="Voltage set",width=20).pack(side="left")
volt=tk.Entry(entry1Frm,width=50,justify="right")
volt.insert(0,0.0)
volt.pack(side="left")
entry1Frm.pack(side="top",pady=5)

entry2Frm=tk.Frame(contentFrm)
tk.Label(entry2Frm,text="Current set",width=20).pack(side="left")
curr=tk.Entry(entry2Frm,width=50,justify="right")
curr.insert(0,0.0)
curr.pack(side="left")
entry2Frm.pack(side="top",pady=5)

entry3Frm=tk.Frame(contentFrm)
tk.Label(entry3Frm,text="Voltage Protection set",width=20).pack(side="left")
voltPT=tk.Entry(entry3Frm,width=50,justify="right")
voltPT.insert(0,1.0)   
voltPT.pack(side="left")
entry3Frm.pack(side="top",pady=5)

entry4Frm=tk.Frame(contentFrm)
tk.Label(entry4Frm,text="Current Protection set",width=20).pack(side="left")
currPT=tk.Entry(entry4Frm,width=50,justify="right")
currPT.insert(0,1.0)
currPT.pack(side="left")
entry4Frm.pack(side="top",pady=5)

tk.Button(contentFrm,text="SET",command=DCcont.SetControl,width=15).pack(side="top",pady=10)

protectionFrm=tk.Frame(contentFrm)
tk.Button(protectionFrm,text="On/Off Over Voltage Protection(OVP)",command=DCcont.setOVP).pack(side="left",padx=10,pady=10)
tk.Button(protectionFrm,text="On/Off Over Current Protection(OCP)",command=DCcont.setOCP).pack(side="left",padx=10,pady=10)
protectionFrm.pack(side="top")

statFrm=tk.Frame(contentFrm)
labelOVP=tk.Label(statFrm,text=f"Your {CH} OVP is {OVPst}")
labelOVP.pack(side="left",padx=10)
labelOCP=tk.Label(statFrm,text=f"Your {CH} OCP is {OCPst}")
labelOCP.pack(side="left")
statFrm.pack(side="top",padx=10)

# StatOCP()
# StatOVP()

# Info Volt Current
infoVoltFrm=tk.Frame(contentFrm)
tk.Label(infoVoltFrm,text="Voltage value",width=20).pack(side="left")
VoltLabel=tk.Label(infoVoltFrm,bg="#e3d5ca")
VoltLabel.pack(side="left",ipadx=30,padx=10)
tk.Label(infoVoltFrm,text="V").pack(side="left")
infoVoltFrm.pack(side="top",pady=10)

infoCurrFrm=tk.Frame(contentFrm)
tk.Label(infoCurrFrm,text="Current value",width=20).pack(side="left")
CurrLabel=tk.Label(infoCurrFrm,bg="#e3d5ca")
CurrLabel.pack(side="left",ipadx=30,padx=10)
tk.Label(infoCurrFrm,text="V").pack(side="left")
infoCurrFrm.pack(side="top",pady=5)

# Info OVP OCP
infoOVPFrm=tk.Frame(contentFrm)
tk.Label(infoOVPFrm,text="Voltage Protection value",width=20).pack(side="left")
VoltPLabel=tk.Label(infoOVPFrm,bg="#e3d5ca")
VoltPLabel.pack(side="left",ipadx=30,padx=10)
tk.Label(infoOVPFrm,text="V").pack(side="left")
infoOVPFrm.pack(side="top",pady=10)

infoOCPFrm=tk.Frame(contentFrm)
tk.Label(infoOCPFrm,text="Current Protection value",width=20).pack(side="left")
CurrPLabel=tk.Label(infoOCPFrm,bg="#e3d5ca")
CurrPLabel.pack(side="left",ipadx=30,padx=10)
tk.Label(infoOCPFrm,text="V").pack(side="left")
infoOCPFrm.pack(side="top",pady=5)

DCcont.ShowInfo()
contentFrm.pack(side="top",expand=True,fill="both")





DcWindow.mainloop()