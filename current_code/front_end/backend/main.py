print('startup begun.\nBeginning brain import')
from . import brainfs
print('brain import complete.\n importing speech recognition systems.')
from . import speechrec
print('speech recognition systems ready.  Commencing main loop.')
from . import lists
from . import threadqueues
from .security import secfs

def main_loop():
	pauseflag=1
	startflag=1
	while(True):
		while not threadqueues.eventqueue.empty():
			eventinput=threadqueues.eventqueue.get()
			if(eventinput==1):
				pauseflag=0
			elif(eventinput==0):
				pauseflag==1
		if (startflag==1 and pauseflag==0):
			speech='greetings admin'
			brainfs.tts(speech)
			threadqueues.outputqueue.put(speech)
			man_flag=True
			startflag=0
		while(pauseflag==0):
			while not threadqueues.secureinput.empty():
				inp=threadqueues.secureinput.get()
				output=secfs.secmain(inp)
				threadqueues.secureoutput.put(output)
			while not threadqueues.inputqueue.empty():
				inp=threadqueues.inputqueue.get()
				print(inp)
				#inp=lists.inputlist.pop(0)
				if inp=="MANUAL":
					threadqueues.outputqueue.put("MANUAL MODE ON. TO EXIT MANUAL MODE, TYPE 'MANUAL OFF'")
					man_flag=True
				if inp=="MANUAL OFF":
					man_flag=False
				if inp=="DEBUG":
					debug.debugaccess()
				else:
					print(inp)
					output=brainfs.brain(inp)
					output=output+"\n"
					threadqueues.outputqueue.put(output)
					brainfs.tts(output)
