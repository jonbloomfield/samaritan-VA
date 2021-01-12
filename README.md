This is Samaritan, a virtual assistant I'm working on in python.  This project is partly functionality, part portfolio, and to practise my coding and project management.

Currently, there are 3 main parts to Samaritan: The core, the GUI and the modules.
The core encompasses the actual lexical analysis and categorisation of natural input, and the extrapolation of commands, before transferring control and parameter to the relevant module.
The GUI is written in tkinter, and currently provides basic functionality for input and output as well as some minor debugging, as it allows the back end modules to be loaded before the main loop.
the modules give Samaritan its primary functionality, and range from weather, to time, Wikipedia queries, and general chat.

PREREQUISITES: 
-	Python3
-	CMUSphinx
-	NLTK toolkit
-	Porterstemmer
-	speech_recognition
-	passlib

Samaritan can use offline speech recognition and TTS (although this is not implemented in the GUI) but works better with manual input.
To use Samaritan (one all perquisites are installed), run “samaritan.py” from the folder “frontend”.  **note: I’ve only designed it to run on my machine so if anyone actual tries to run it and has problems let me know and I’ll update this/help you out. **
The screen should come up with a GUI with a large “START CORE” button.  This will set to core to start running.  Once pressed, another GUI window will open with an input and output textbox.  You can input your query, and the output will appear in the output box (and it will speak it out!)
In future builds, a mic button for voice input or even an Alexa/google style “on word” may be implemented.

Commands:
-	WEATHER:

	-	What is the weather today?
	-	Will there be (insert weather type) today?
	-	What is the temperature today?
	-	Etc
-	TIME/DATE
	-	What is the time
	-	What is the date?
-	GENERAL:
	-	Who am i? 
	-	Who are you?
	-	Couple of other little bits
-	WIKIPEDIA:
	-	Define X
	-	Give me a summary/summarise X

CURRENTLY IN DEV:
-	News module
-	Profiles/users
-	Security privileges
-	Saved preferences for users.
-	Big general chat update/engine overhaul
-	Reminders/alarms/notes etc

For full documentation, check the management folder of this project.
