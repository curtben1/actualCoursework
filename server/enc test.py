import socket
from threading import *
import SQLreader as sql
import pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from bcrypt import gensalt


usernamePlain = input("what is the username: ")
pwordPlain = input("what is the password: ")
salt = gensalt()
message = pwordPlain + str(salt)
message = pickle.dumps(message) 

with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )
encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
request = (1,"sign up",[usernamePlain, encrypted,salt] )


inp = request
print("the tuple being sent is: ",request)








username = inp[2][0]
pword = inp[2][1]

print(type(pword))

with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
decrypted = private_key.decrypt(pword,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
salt = inp[2][2]
#decrypted 
decrypted = pickle.loads(decrypted)

digest = hashes.Hash(hashes.SHA256(), backend = default_backend())
digest.update(pickle.dumps(decrypted))
hashed = digest.finalize()
print("the hashed password is",hashed)
print("the unhashed password is",decrypted)
sql.writePword(username, hashed,salt)





















usernamePlain = input("what is the username: ")
pwordPlain = input("what is the password: ")
#https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
message = pickle.dumps(pwordPlain) 
        
with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )
encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
request = (1,"logon",[usernamePlain, encrypted] )

print("the tuple being sent is: ",request)

msg = request





username = request[2][0]
pword = request[2][1]
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
decrypted = private_key.decrypt(pword,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
decrypted = pickle.loads(decrypted)
salt = sql.retSalt(username)
print(salt[0][0])
print("the decrypted password is",decrypted)
salted = decrypted + str(salt[0][0])


digest = hashes.Hash(hashes.SHA256(), backend = default_backend())
digest.update(pickle.dumps(salted))
hashed = digest.finalize()
print("the hashed password is", hashed)
print("the unhashed password is",salted)

check = sql.checkPword(username, hashed)
print(check)
if check:
    reply = check[0]
else:
    reply = False


print(reply)