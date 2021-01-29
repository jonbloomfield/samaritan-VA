from Crypto.Protocol.KDF import PBKDF2
from passlib.hash import sha256_crypt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

masterpassword="$5$rounds=535000$dJMrUQM9r2bsxEmX$qlH/zMQJ.P1LcnlVeHz2dP8pjsdCh2aP5FMeU7bJeX0"


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


print("please enter profile name")
pname=input()
print("please enter password")
password=input()
pnamefile="/media/sf_share/samaritan-VA/current_code/front_end/backend/security/profiles/"+pname+".txt"
try:
	profilefile=open(pnamefile,"rb")
except FileNotFoundError:
	print("error.  name or password incorrect. please try again.")
passwordfilestring="/media/sf_share/samaritan-VA/current_code/front_end/backend/security/keymanagement/pswds.txt"
passwordfile=open(passwordfilestring,"r")
lines = passwordfile.readlines()
storedpassword=""
for line in lines:
    line=line.split(":")
    if(line[0]==pname):storedpassword=line[1]
print(storedpassword)
print(passwordcheck(password,pname))
passcheck=passwordcheck(password,pname)
if passcheck==False:
	print("error.  name or password incorrect. please try again.")
salt=profilefile.read(32)
iv = profilefile.read(16)
ciphertext=profilefile.read()
profilefile.close()

key = PBKDF2(password, salt, dkLen=32) 
cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
original_data = unpad(cipher.decrypt(ciphertext), AES.block_size) # Decrypt and then up-pad the result
print(original_data)