import os
from stat import S_IREAD, S_IWRITE
from time import sleep
from Crypto.Protocol.KDF import PBKDF2
from passlib.hash import sha256_crypt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
from datetime import datetime

from .. import threadqueues

masterpassword="$5$rounds=535000$dJMrUQM9r2bsxEmX$qlH/zMQJ.P1LcnlVeHz2dP8pjsdCh2aP5FMeU7bJeX0"
helpstring="SEC CONSOLE MODE.  COMMANDS AS FOLLOWS:\n CREATE NEW PROFILE: 'newprofile'\n "
helpstring+="CHANGE PASSWORD: 'changepassword' \n HELP (THESE OPTIONS) 'help'.\n"
helpstring+="PLEASE NOTE - WHILE SECURITY FUNCTIONS ARE UNDERWAY, NORMAL REQUESTS ARE ON HOLD UNTIL SECURITY FUNCTION COMPLETED.-SEC-"
currentprofilename=""
currentprofileprivs=""
currentprofileloc=""
currentprofilecalendar=[]
profiledata=[currentprofilename,currentprofileprivs,currentprofileloc,currentprofilecalendar]



def passwordcheck(password,profilename):
	storedpassword=""
	if(profilename=="masteradmin"):
		storedpassword=masterpassword
	passwordfile = open("/media/sf_share/samaritan-VA/current_code/front_end/backend/security/keymanagement/pswds.txt", "r")
	for line in passwordfile:
		if profilename in line:
			splitline=line.split(":")
			storedpassword=splitline[1]
			break
	if storedpassword=="": return 0
	return sha256_crypt.verify(password,storedpassword)

def wait_for_secure_input():
	while threadqueues.secureinput.empty():
		sleep(0.1)
	print("secinfound")
	return threadqueues.secureinput.get()

def newprofile():
	adminflag=False
	pnameok=False
	while pnameok==False:	
		threadqueues.secureoutput.put("please enter profile name")
		pname=wait_for_secure_input()
		print(9)
		fstring="/media/sf_share/samaritan-VA/current_code/front_end/backend/security/profiles/"+pname+".txt"
		try:
			f = open(fstring,"r")
			f.close()
			return("PROFILE NAME ALREADY IN USE. PLEASE TRY AGAIN.")
		except FileNotFoundError:
			pnameok=True
	pscheckexit=0
	print("here")
	while(pscheckexit==0):
		threadqueues.secureoutput.put("PROFILE NAME: "+pname+". Please enter profile password")
		print(455)
		pps=wait_for_secure_input()
		print("here2")
		threadqueues.secureoutput.put("please confirm password")
		ppscheck=wait_for_secure_input()
		print("j")
		if(ppscheck==pps):
			pscheckexit=1
		else:
			threadqueues.secureoutput.put("ERROR. PASSWORDS DON'T MATCH. PLEASE TRY AGAIN.")
	threadqueues.secureoutput.put("Do you wish this to be an admistrative account? Y/N")
	if(wait_for_secure_input())=="Y":
		exit=1
		while(exit==1):
			threadqueues.secureoutput.put("PLEASE INPUT MASTER PASSWORD NOW")
			mspscheck=wait_for_secure_input()
			if(passwordcheck(mspscheck,"masteradmin")==True):
				threadqueues.secureoutput.put("MASTER PASSWORD ACCEPTED.")
				adminflag=True
				exit=0
			else:
				threadqueues.secureoutput.put("incorrect password please try again (Y) or make ordinary profile instead (N).")
				rexit=1
				while(rexit==1):
					response=wait_for_secure_input()
					if(response=="Y"):rexit=0
					if(response=="N"):
						rexit=0
						exit=0
					else:threadqueues.secureoutput.put("invalid input. please input Y/N.")
	print(1234)
	threadqueues.secureoutput.put("please enter default location (this can be changed later)")
	loc=wait_for_secure_input()
	storedpassword=sha256_crypt.hash(pps)
	passwordfile = open("/media/sf_share/samaritan-VA/current_code/front_end/backend/security/keymanagement/pswds.txt", "a")
	passwordfile.write("\n"+pname+":"+storedpassword)
	passwordfile.close()
	profilelistfile=open("/media/sf_share/samaritan-VA/current_code/front_end/backend/security/profiles/profilelist.txt","a")
	if adminflag==True:privs="1011010"
	if adminflag==False:privs="0000000"
	profilelistfile.write("\n"+pname+":"+privs)
	fstring="/media/sf_share/samaritan-VA/current_code/front_end/backend/security/profiles/"+pname+".txt"
	f=open(fstring,"wb")
	profilestringlist=[pname,privs,loc]
	profilestring=""
	for i in profilestringlist:
		profilestring+=(":"+i)
	salt=get_random_bytes(32)
	filekey= PBKDF2(pps, salt, dkLen=32)
	data = bytes(profilestring,"utf-8")
	cipher = AES.new(filekey, AES.MODE_CBC) # Create a AES cipher object with the key using the mode CBC
	ciphered_data = cipher.encrypt(pad(data, AES.block_size)) # Pad the input data and then encrypt
	f.write(salt)
	f.write(cipher.iv)
	f.write(ciphered_data)
	f.close()
	print("profile created")
	return "nptest"
#32 for salt
#16 for iv

def retriveprofiledata():
	Gflag=False
	if(threadqueues.guilogin.empty()==False):
		guilogin=threadqueues.guilogin.get()
		pname=guilogin[0]
		password=guilogin[1]
		Gflag=True
		guilogin=[]
	if(Gflag==False):
		threadqueues.secureoutput.put("please enter profile name")
		pname=wait_for_secure_input()
		threadqueues.secureoutput.put("please enter password")
		password=wait_for_secure_input()
	pnamefile="/media/sf_share/samaritan-VA/current_code/front_end/backend/security/profiles/"+pname+".txt"
	try:
		profilefile=open(pnamefile,"rb")
	except FileNotFoundError:
		if(Gflag==False):
			threadqueues.secureoutput.put("error.  name or password incorrect. please try again.")
		else:threadqueues.GUIflags.put("1,1")
		return
	passcheck=passwordcheck(password,pname)
	if passcheck==False:
		if(Gflag==False):
			threadqueues.secureoutput.put("error.  name or password incorrect. please try again.")
		else:threadqueues.GUIflags.put("1,1")
		return
	
	print("passtrue")
	salt=profilefile.read(32)
	iv = profilefile.read(16)
	ciphertext=profilefile.read()
	profilefile.close()
	key = PBKDF2(password, salt, dkLen=32) 
	cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
	original_data = unpad(cipher.decrypt(ciphertext), AES.block_size) # Decrypt and then up-pad the result
	print(original_data)
	global profiledata
	profiledata=original_data.decode("utf-8").split(":")
	profiledata.pop(0)
	print(profiledata[0])

	if(Gflag==False):return("login successful.  Welcome, "+currentprofilename+".")		
	else:
		(threadqueues.GUIflags.put("1,2"))	
		return False

def changepassword():
	return "changepassword test"
def helpoptions():
	return helpstring

def seccore():
	while(True):
		inp=wait_for_secure_input()
		output=secmain(inp)
		if(output!=False):
			threadqueues.secureoutput.put(output)


		
def secmain(inp):
	if inp=="":
		output="INPUT NOT RECOGNISED.\n"+helpstring
		return ""
	output=secmaindict[inp]()
	return output


secmaindict={
	"newprofile":newprofile,
	"changepassword":changepassword,
	"login":retriveprofiledata,
	"help":helpoptions

}
