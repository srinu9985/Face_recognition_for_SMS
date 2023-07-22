import re,json
import time

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import pymongo

#For password extraction

f = open(r'D:\Project-mini\passwords_n18.txt','r')
a = f.read()

regex = re.compile("(\w+):(\w*[!@#$%^&*()_+{}|;:'\"?>\<.,`~A-Za-z0-9]*\w*)(.*)")
found_string = regex.sub(r'"\1":"\2",',a) # print(found_string) --> It's a string # print(type(found_string)) ---><class 'str'>

# result = regex.findall(a) #It gives a list of tuples where each tuple consists matched groups in string format seperated by comma

dict_in_string = '{'+found_string+'"N180109":"Va2Wd"}'
dictionary_n18 = json.loads(dict_in_string)

id=180000
while id<181191:
    id+=1
    if 'N'+str(id) in dictionary_n18:
        continue
    else:
        dictionary_n18['N'+str(id)]=None    # print(type(dictionary_n18)) --> It's a dictionary

sorted_dictionary_n18 = dict(sorted(dictionary_n18.items(),key=lambda k: k[0]))


#For encryption

key_generate_passphrase = "mini_project@143"

kdf = PBKDF2HMAC(algorithm=hashes.SHA256, length = 32, salt ="2018_batch".encode(), iterations=100000,backend=default_backend())
key = kdf.derive(key_generate_passphrase.encode())
#If I don't use base64 encodeing it was giving error as Fernet key must be 32 url-safe base64-encoded bytes
key = base64.urlsafe_b64encode(key).decode()
print(key)

fernet = Fernet(key)
plaintext = "I am pavan"
def encrypt(plaintext):
    ciphertext = fernet.encrypt(plaintext.encode())
    return ciphertext
def decrypt(ciphertext):
    decrypted = fernet.decrypt(ciphertext).decode()
    return decrypted
for i in sorted_dictionary_n18:
    if sorted_dictionary_n18[i]==None:
        continue
    else:
        sorted_dictionary_n18[i] = encrypt(sorted_dictionary_n18[i])

encrypted_passwords_n18 = sorted_dictionary_n18
