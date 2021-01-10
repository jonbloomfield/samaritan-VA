from passlib.hash import sha256_crypt
def newprofile(): 	
    toredpassword=sha256_crypt.hash("haroldfinch")
    print(toredpassword)
newprofile()