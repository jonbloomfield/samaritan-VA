import speech_recognition as sr# obtain audio from the microphone  
r = sr.Recognizer() 
def inspeak():
	with sr.Microphone() as source:
		print("Seeay something!")
		audio = r.listen(source)  
   
 	# recognize speech using Sphinx  
	try:
		print('j')
		return r.recognize_sphinx(audio) 
	except sr.UnknownValueError:
		print("Sphinx could not understand audio")  
	except sr.RequestError as e:
		print("Sphinx error; {0}".format(e)) 
