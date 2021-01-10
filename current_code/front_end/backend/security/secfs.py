from .. import threadqueues
from passlib.hash import sha256_crypt
import os
from stat import S_IWRITE, S_IREAD
masterpassword="$5$rounds=535000$dJMrUQM9r2bsxEmX$qlH/zMQJ.P1LcnlVeHz2dP8pjsdCh2aP5FMeU7bJeX0"
helpstring="SEC CONSOLE MODE.  COMMANDS AS FOLLOWS:\n CREATE NEW PROFILE: 'newprofile'\n "
helpstring+="CHANGE PASSWORD: 'changepassword' \n HELP (THESE OPTIONS) 'help'.\n"
helpstring+="PLEASE NOTE - WHILE SECURITY FUNCTIONS ARE UNDERWAY, NORMAL REQUESTS ARE ON HOLD UNTIL SECURITY FUNCTION COMPLETED.-SEC-"

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
		i=1
	return threadqueues.secureinput.get()

def newprofile():
	adminflag=False 	
	threadqueues .secureoutput.put("please enter profile name")
	pname=wait_for_secure_input()
	threadqueues.secureoutput.put("PROFILE NAME: "+pname+". Please enter profile password")
	pps=wait_for_secure_input()
	threadqueues.secureoutput.put("please confirm password")
	ppscheck=wait_for_secure_input()
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

	if(ppscheck==pps):
		storedpassword=sha256_crypt.hash(pps)
		passwordfile = open("/media/sf_share/samaritan-VA/current_code/front_end/backend/security/keymanagement/pswds.txt", "a")
		passwordfile.write("\n"+pname+":"+storedpassword)
		passwordfile.close()
		profilelistfile=open("/media/sf_share/samaritan-VA/current_code/front_end/backend/security/profiles/profilelist.txt","a")
		if adminflag==True:privs="1011010"
		if adminflag==False:privs="0000000"
		profilelistfile.write("\n"+pname+":"+privs)
		print("profile created")

	return "nptest"
def changepassword():
	return "changepassword test"
def helpoptions():
	return helpstring


def secmain(inp):
	output=secmaindict[inp]()
	if output==None:
		output="INPUT NOT RECOGNISED.\n"+helpstring
	return output


secmaindict={
	"newprofile":newprofile,
	"changepassword":changepassword,
	"help":helpoptions

}