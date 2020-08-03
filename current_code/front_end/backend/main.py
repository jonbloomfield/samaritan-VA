print('startup begun.\nBeginning brain import')
import brain
print('brain import complete.\n importing speech recognition systems.')
import speechrec
print('speech recognition systems ready.  Commencing main loop.')
import lists



def main_loop():

	speech='greetings admin'
	brain.tts(speech)
	lists.outputlist.append(speech)
	man_flag=True
	while(True):
		while(lists.inputlist!=[]):
			inp=raw_input()
			#inp=lists.inputlist.pop(0)
			if inp=="MANUAL":
				print("MANUAL MODE ON. TO EXIT MANUAL MODE, TYPE 'MANUAL OFF'")
				man_flag=True
			if inp=="MANUAL OFF":
				man_flag=False
			if inp=="DEBUG":
				debug.debugaccess()
			else:
				output=brain.brain(inp)
				print(1,output,1)
				lists.outputlist.append(str(output))
main_loop()