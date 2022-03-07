import getpass
import hashlib
from quopri import decodestring

id = ""
pw = ""

id = getpass.getpass(prompt = "Enter student ID number: ")
pw = getpass.getpass(prompt = "Enter password: ")
print("\ninput")
print(id)
print(pw)

# encode
id = id.encode(encoding = 'UTF-8')
pw = pw.encode(encoding = 'UTF-8')
print("\nbytes")
print(id)
print(pw)


m = hashlib.sha256()
m.update(id)
m.update(pw)
m.digest()
print("digest = ", m.digest())


# decode
id = id.decode('utf8', 'strict')
pw = pw.decode('utf8', 'strict')
print("\ndecoded")
print(id)
print(pw)

#send m somehow