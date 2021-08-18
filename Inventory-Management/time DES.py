from DES import *
from hexAndString import *
import datetime

data = "127.0.0.1\n3306\nroot\nIMS\nMdif59x02#"
key = input("Enter the Password: ")

data = string2hex(data)
pas = string2hex(key)
len_data = len(data)
len_pas = len(pas) - 1
enc_data = [0]*len_data
for i in range(len_data):
    enc_data[i] = DESAlgorithm(pas[i%len_pas], data[i], 1)
enc_data = "\n".join(enc_data)

#decryption process
begin = datetime.datetime.now()

data = enc_data.split("\n")
pas = string2hex(key)
len_data = len(data)
len_pas = len(pas) - 1
dec_data = [0]*len_data
for i in range(len_data):
    dec_data[i] = DESAlgorithm(pas[i%len_pas], data[i], 2)

dec_data = hex2string(dec_data)

end = datetime.datetime.now()
print("Decryption Time: ", end-begin)
# print(dec_data)
