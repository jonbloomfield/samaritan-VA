#!/usr/bin/python3

import tkinter as tk 
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
import threading
from backend import threadqueues
from backend.security.secfs import profiledata
 


class samaritanapp():
	coreinit=False
	corerunning=False	#core flags that determine what image shows on start screen
	top = tk.Tk()	#root window init
	corewindow = tk.Toplevel(width=500,height=400)	#make core window
	corewindow.geometry('1300x700')
	corewindow.withdraw()	#make core window invisible til needed



	#imgs init
	corephoto = PhotoImage(file="startcore.png")
	corephoto = corephoto.subsample(2,2)	#image to big, half size
	corestartedphoto=PhotoImage(file=r"corestarted.png")
	corestartedphoto = corestartedphoto.subsample(2,2)
	corepausedphoto=PhotoImage(file=r"corepaused.png")
	corepausedphoto = corepausedphoto.subsample(2,2)

	# make startscreen widgets
	debugbutton=tk.Button(text="DEBUG",font=("Courier", 24))
	corebuttonstart=tk.Button(text='test',image=corephoto)
	testbutton=tk.Button(text="TEST",font=("Courier", 24))
	documentationbutton=tk.Button(text="DOCUMENTATION",font=("Courier", 44))
	safequitbutton=tk.Button(text="safe-quit",font=("Courier", 24))

	#make corescreen widgets

	def getmaintext(event):	#funct to get text of entry bar on enter key pressed
		text=event.widget.get()
		threadqueues.inputqueue.put(event.widget.get())	
		event.widget.delete(0,END)	#blank entry box

	def getsecuretext(event):	#funct to get text of secure input bar on enter key pressed
		text=event.widget.get()
		threadqueues.secureinput.put(text)
		event.widget.delete(0,END)	#blank entry box

	def donothing(self):
		x=1


	minput = StringVar() 
	maininput= tk.Entry(corewindow,textvariable=minput,font=("Courier", 10),width=80)
	maininput.bind('<Return>',getmaintext)

	cpureadings=tk.Label(corewindow,text="cpureadings",font=("Courier", 24))                 
	wifireadings=tk.Label(corewindow,text="wifireadings",font=("Courier", 24))
	corereadings=tk.Label(corewindow,text="corereadings",font=("Courier", 24))
	outputframe=tk.Frame(corewindow)
	mainoutputscroll = tk.Scrollbar(corewindow)	#make output scollable
	mainoutput = tk.Text(corewindow,wrap="word",state='disabled', yscrollcommand=mainoutputscroll.set,font=("Courier", 10),height=20,width=100)
	webdata=tk.Label(corewindow,text="web/data",font=("Courier", 44))
	logiccmd=tk.Label(corewindow,text="logic cmd",font=("Courier", 44))
	secureterminalscroll=tk.Scrollbar(corewindow)
	secureterminal= tk.Text(corewindow,wrap="word",state='disabled',yscrollcommand=secureterminalscroll.set,font=("Courier", 10),height=20,width=100,background="black")
	secinp = StringVar() 
	secureinputbox= tk.Entry(corewindow,textvariable=secinp,font=("Courier", 10),width=80)
	secureinputbox.bind('<Return>',getsecuretext)

	def __init__(self):
		logoimg = tk.Image("photo", file="logo.png")
		self.top.tk.call('wm','iconphoto',self.top._w,logoimg)	#main win setup
		self.top.title('SAMARITAN')
		self.initstart()
		#init app functs
		self.updatecorelabels()

		self.loginwindow=None

		self.menubar = Menu(self.corewindow)
		filemenu = Menu(self.menubar, tearoff=0)
		filemenu.add_command(label="profile", command=self.createloginwindow)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.corewindow.quit)
		self.menubar.add_cascade(label="File", menu=filemenu)
		helpmenu = Menu(self.menubar, tearoff=0)
		helpmenu.add_command(label="Help Index", command=self.donothing)
		helpmenu.add_command(label="About...", command=self.donothing)
		self.menubar.add_cascade(label="Help", menu=helpmenu)
		self.corewindow.config(menu=self.menubar)

		self.top.mainloop()

	def createloginwindow(self):
		try:
			if(self.loginwindow.state()) == "normal":
				self.loginwindow.lift()
				return
		except:print(0)

		self.loginwindow=tk.Toplevel(width=200,height=200)
		self.logintext=tk.Label(self.loginwindow,text="login with name/password to access customised features.")
		self.loginname = StringVar() 
		self.loginnameinput= tk.Entry(self.loginwindow,textvariable=self.loginname,font=("Courier", 10),width=80)
		self.loginpassword=StringVar()
		self.loginpasswordinput=tk.Entry(self.loginwindow,textvariable=self.loginpassword,show="*",font=("Courier", 10),width=80)
		self.logintext.pack()
		self.loginnameinput.pack()
		self.loginpasswordinput.pack()
		self.loginbutton=tk.Button(self.loginwindow,text="LOGIN",command=lambda:self.login())
		self.loginbutton.pack()
	def logout(self):
		threadqueues.secureinput.put("logout")
		self.loginnameinput.config(state="enabled")
		self.loginpasswordinput.config(state="enabled")
		self.logintext.config(text="login with name/password to access customised features.")
		self.loginbutton.config(text="LOGIN",command=self.login)
	def login(self):
		pname=self.loginnameinput.get()
		password=self.loginpasswordinput.get()
		self.loginnameinput.delete(0,END)
		self.loginpasswordinput.delete(0,END)
		threadqueues.guilogin.put([pname,password])
		threadqueues.secureinput.put("login")
	def loginfail(self):
		self.logintext.config(text="ERROR. PASSWORD OR NAME INCORRECT. PLEASE TRY AGAIN")
	def loginsucess(self):
		from backend.security.secfs import profiledata
		self.loginnameinput.config(state="disabled")
		self.loginpasswordinput.config(state="disabled")
		print(profiledata[0])
		self.logintext.config(text="Logged in as "+profiledata[0])
		self.loginbutton.config(text="LOGOUT",command=self.logout)

	def updatecorelabels(self):
		if(self.corerunning==True):
			if not threadqueues.secureoutput.empty():
				secandname="SECUREOUTPUT@"+profiledata[0]+":"
				outputtext="SECUREOUTPUT@"+profiledata[0]+":"+threadqueues.secureoutput.get()
				self.secureterminal.config(state="normal")
				number=self.secureterminal.index("end")[:-1]+str(len(secandname)-1)
				starttagpoint=self.secureterminal.index("end")
				self.secureterminal.insert("end","\n")
				self.secureterminal.insert("end",outputtext)		#funct to update output
				self.secureterminal.tag_add("tag"+starttagpoint,starttagpoint,number)
				self.secureterminal.tag_config("tag"+starttagpoint,foreground="red")
				self.secureterminal.tag_add("tagtext"+starttagpoint,number,self.secureterminal.index("end"))
				self.secureterminal.tag_config("tagtext"+starttagpoint,foreground="white")
				self.secureterminal.config(state="disabled")
			if not threadqueues.outputqueue.empty():
				outputtext=threadqueues.outputqueue.get()
				self.mainoutput.config(state="normal")
				self.mainoutput.insert("end","\n")
				self.mainoutput.insert("end",outputtext)		#funct to update output
				self.mainoutput.config(state="disabled")
			if not threadqueues.GUIflags.empty():
				GUIflag=threadqueues.GUIflags.get()
				self.GUIflagdict[GUIflag](self)



		self.top.after(100,self.updatecorelabels) #make sure update funct runs again



	def initstart(self):
		self.corebuttonstart.config(command=lambda:self.iscoreon())
		self.debugbutton.grid(row=0,column=0,columnspan=2)
		self.corebuttonstart.grid(row=0,column=2,columnspan=2)			#grid startup screen
		self.testbutton.grid(row=0,column=4,columnspan=2)
		self.documentationbutton.grid(row=1,column=0,columnspan=3)
		self.safequitbutton.grid(row=1,column=3,columnspan=3)

	def coreframinit(self):
		self.corewindow.deiconify()
		self.maininput.grid(row=0,column=0,columnspan=2,pady=(10, 0))
		self.corereadings.grid(row=0,column=2,columnspan=3)
		self.mainoutputscroll.grid(column=2,row=1,sticky="ns",rowspan=1)
		self.mainoutput.grid(row=1,column=0,columnspan=1,rowspan=1)			#grid corescreen
		self.mainoutputscroll.config(command=self.mainoutput.yview)
		self.wifireadings.grid(row=0,column=3,columnspan=1)
		self.webdata.grid(row=1,column=3,rowspan=2,columnspan=2)
		self.logiccmd.grid(row=2,column=3,columnspan=2)
		self.secureterminal.grid(row=2,column=0,columnspan=2,pady=(10,0),rowspan=1)
		self.secureterminalscroll.grid(column=2,row=2,sticky="ns",rowspan=1)
		self.secureterminalscroll.config(command=self.secureterminal.yview)
		self.secureinputbox.grid(column=0,row=3,rowspan=3)
		self.corewindow.protocol("WM_DELETE_WINDOW", self.corewinclose)
	
	def corewinclose(self):
		self.coreinit=False
		self.corerunning=False	#funct if corewin closed
		threadqueues.eventqueue.put(0)
		self.corebuttonstart.config(image=self.corephoto)
		self.corewindow.withdraw()	#corewin invisible


	def iscoreon(self):
		if self.coreinit==False:
			self.coreframinit()
			self.coreinit=True 			#if core not running, set flags to running, chage start photo, send message to corethread to unpause
			self.corerunning=True
			self.corebuttonstart.config(image=self.corestartedphoto)
			threadqueues.eventqueue.put(1)
			return
		if self.corerunning==True:	#pause core
			print("core paused")
			self.corerunning=False
			self.corebuttonstart.config(image=self.corepausedphoto)
			return
		if self.corerunning==False:
			print("core resumed")	#unpause core
			self.corebuttonstart.config(image=self.corestartedphoto)
			self.corerunning=True
	GUIflagdict={
	"1,1":loginfail,
	"1,2":loginsucess,
	"2,1":alarm,
	"2,2":eventremind

	}
		


	
def corethreadstart():
	from backend import main 	#core thrad
	main.main_loop()
def secthreadstart():
	from backend.security import secfs
	secfs.seccore()
corethread=threading.Thread(target=corethreadstart)
corethread.start()
secthread=threading.Thread(target=secthreadstart)
secthread.start()
samaritan=samaritanapp() # start frontendself.corewindow.deiconify()