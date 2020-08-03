#DEBUG 
import hashlib
import sqlite3 as lite
import getpass
def debugaccess():
	try:
		conn=lite.connect('userdb.db')
		cur=conn.cursor()
	except lite.Error, e:
		print "Error {}:".format(e.args[0])


	while(True):
		print("enter username")
		uname=str(raw_input())
		sh = hashlib.sha1()
		sh.update(uname)
		hash_value = str(sh.hexdigest())
		print(hash_value)
		
		cur.execute('''SELECT EXISTS(SELECT 1 FROM USERS WHERE UNAME=?)''',(hash_value,))
		rows=cur.fetchall()
		rows=rows[0][0]
		print(rows)
		if(rows!=0):
			print('welcome '+uname)
			ps=getpass.getpass("Enter your password: ")
			print(ps)
			sh.update(ps)
			hash_value = sh.hexdigest()
			print(hash_value)
			cur.execute('''SELECT EXISTS(SELECT 1 FROM USERS WHERE PSWD=?)''',(hash_value,))
			rows=cur.fetchall()
			print(rows)
			rows=rows[0][0]
			if(rows!=0):
				print('ACCESS GRANTED.  WELCOME TO DEBUG MODE.')
				debugmain()
				return 0
			elif (rows ==0): print("PASSWORD ERROR")
		elif (rows==0):
			print("USERNAME ERROR")
	

	conn.close()


def debugmain():
	while(True):
		print("DEBUG MODE V.02. PLEASE SELECT OPTIONS.")
		print("TO EDIT WORK DATABASE TYPE 'EDIT WORD DATABASE' OR PRESS 1.")
		print("To ALTER FUNCTIONS, PLEASE PRESS 2 OR TYPE 'ALTER PRIMARY FUNCTION'")
		print("TO SEARCH FOR FUNCTION/CODE, TYPE 'SEARCH' OR PRESS 3")
		print("TO CHECK DIAGNOSTICS, PRESS 4 OR TYPE 'DIAGNOSTICS'.")
		print("TO EXIT DEBUG MODE, TYPE 'EXIT DEBUG OR ENTER 0'")
		userin=str(raw_input())
		if(userin=='0' or userin=='EXIT DEBUG'):
			return 0
		try:
			userin=int(userin)
			intflag=True
		except:
			intflag=False
		if intflag==False:
			switcher = {
				'EDIT WORD DATABASE': EDIT_WORD_DB,
				'ALTER PRIMARY FUNCTION': ALTER_CODE,
				'SEARCH': SEARCH,
				}
			# Get the function from switcher dictionary
			func = switcher.get(userin, lambda: "Invalid operation")
			print func()
		elif intflag==True:
			switcher = {
				1: EDIT_WORD_DB,
				2: ALTER_CODE,
				3: SEARCH,
				}
			# Get the function from switcher dictionary
			func = switcher.get(userin, lambda: "Invalid operation")
			print func()



	


def EDIT_WORD_DB():
    return "January"
 
def ALTER_CODE	():
    return "February"
 
def SEARCH():
    return "March"
 
 


debugaccess()