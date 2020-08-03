#!/usr/bin/python3

import tkinter as tk 
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
import threading

 


class samaritanapp():
	coreinit=False
	corerunning=False
	top = tk.Tk()
	corephoto = PhotoImage(file=r"startcore.png")
	corestartedphoto=PhotoImage(file=r"corestarted.png")
	corepausedphoto=PhotoImage(file=r"corepaused.png")
	def __init__(self):
		logoimg = tk.Image("photo", file="logo.png")
		self.top.tk.call('wm','iconphoto',self.top._w,logoimg)	#main win setup
		self.top.title('SAMARITAN')
		self.initstart()
		self.top.mainloop()


	def initstart(self):
		
		self.debugbutton=tk.Button(text="DEBUG",font=("Courier", 44))
		self.corebuttonstart=tk.Button(text='test',image=self.corephoto)
		self.corebuttonstart.config(command=lambda:self.iscoreon())
		self.testbutton=tk.Button(text="TEST",font=("Courier", 44))
		self.documentationbutton=tk.Button(text="DOCUMENTATION",font=("Courier", 44))
		self.safequitbutton=tk.Button(text="safe-quit",font=("Courier", 44))
		self.debugbutton.grid(row=0,column=0,columnspan=2)
		self.corebuttonstart.grid(row=0,column=2,columnspan=2)
		self.testbutton.grid(row=0,column=4,columnspan=2)
		self.documentationbutton.grid(row=1,column=0,columnspan=3)
		self.safequitbutton.grid(row=1,column=3,columnspan=3)

	def coreframinit(self):
		self.corewindow = tk.Toplevel(width=1000,height=700)	#make core window
		self.corewindow.geometry('13000x7000')
		minput = tk.StringVar(value='')
		maininput= tk.Entry(self.corewindow, textvariable = minput,font=("Courier", 10),width=80)
		cpureadings=tk.Label(self.corewindow,text="cpureadings",font=("Courier", 44))
		wifireadings=tk.Label(self.corewindow,text="wifireadings",font=("Courier", 44))
		corereadings=tk.Label(self.corewindow,text="corereadings",font=("Courier", 44))
		#outputframe=tk.Frame()

		myscroll = tk.Scrollbar(self.corewindow)
		mainoutput = tk.Text(self.corewindow,wrap="word", yscrollcommand=myscroll.set,font=("Courier", 10),height=45,width=100)

		webdata=tk.Label(self.corewindow,text="web/data",font=("Courier", 44))
		logiccmd=tk.Label(self.corewindow,text="logic cmd",font=("Courier", 44))
		
		maininput.grid(row=0,column=0,columnspan=2,pady=(150, 400))
		corereadings.grid(row=0,column=2,columnspan=3)
		myscroll.grid(column=2,row=1,sticky="ns",rowspan=2)
		mainoutput.grid(row=1,column=0,columnspan=1,rowspan=2)
		myscroll.config(command=mainoutput.yview)
		#wifireadings.grid(row=0,column=3,columnspan=1)
		webdata.grid(row=1,column=3,rowspan=2,columnspan=2)
		logiccmd.grid(row=2,column=3,columnspan=2)
		#self.startcore()


		self.corewindow.protocol("WM_DELETE_WINDOW", self.corewinclose)
	def corewinclose(self):
		self.coreinit=False
		self.corerunning=False
		self.corebuttonstart.config(image=self.corephoto)
		self.corewindow.destroy()


	def iscoreon(self):
		if self.coreinit==False:
			self.coreframinit()
			self.coreinit=True
			self.corerunning=True
			self.corebuttonstart.config(image=self.corestartedphoto)
			self.startcore()
			return
		if self.corerunning==True:
			print("core paused")
			self.corerunning=False
			self.corebuttonstart.config(image=self.corepausedphoto)
			return
		if self.corerunning==False:
			print("core resumed")
			self.corebuttonstart.config(image=self.corestartedphoto)
			self.corerunning=True

	def startcore(self):
		from backend import main
		corethread=threading.Thread(target=main.main_loop,daemon=True)

samaritan=samaritanapp()
#def threadmanager():



