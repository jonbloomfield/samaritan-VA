import pyttsx3;



def speak(intext):
	engine = pyttsx3.init();
	rate = engine.getProperty('rate')
	engine.setProperty('rate', rate-50) #set speak properties - defeautl is too fast
	engine.say(str(intext));
	engine.runAndWait() ;
	

