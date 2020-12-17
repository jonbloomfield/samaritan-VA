from .. import threadqueues

helpstring="SEC CONSOLE MODE.  COMMANDS AS FOLLOWS:\n CREATE NEW PROFILE: 'newprofile'\n "
helpstring+="CHANGE PASSWORD: 'changepassword' \n HELP (THESE OPTIONS) 'help'.\n"
helpstring+="PLEASE NOTE - WHILE SECURITY FUNCTIONS ARE UNDERWAY, NORMAL REQUESTS ARE ON HOLD UNTIL SECURITY FUNCTION COMPLETED.-SEC-"

def wait_for_secure_input():
	while threadqueues.secureinput.empty():
		i=1
	return threadqueues.secureinput.get()
def newprofile(): 	
	pnameflag=0
	ppsflag=0
	threadqueues.secureoutput.put("please enter profile name")
	pname=wait_for_secure_input()
	pnameflag=1
	threadqueues.secureoutput.put("PROFILE NAME: "+pname+". Please enter profile password")
	pps=wait_for_secure_input()
	threadqueues.secureoutput.put("please confirm password")
	ppscheck=wait_for_secure_input()
	if(ppscheck==pps):
		print(pname)
		print(pps)
		print("test complete")

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