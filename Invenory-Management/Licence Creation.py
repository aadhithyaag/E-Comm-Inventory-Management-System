from hexAndString import *
from DES import *

db_host = "127.0.0.1"
db_port = "3306"
db_user = "root"
db_database = "IMS"
db_password = "Mdif59x02#"
password = input("Enter the desired Password for software: ")


msg=string2hex(db_host+"\n"+db_port+"\n"+db_user+"\n"+db_database+"\n"+db_password)
key=string2hex(password)
print(msg)

len_msg=len(msg)
len_key=len(key)-1
content=[]
for i in range(len_msg):
    content.append(DESAlgorithm(key[i%len_key],msg[i],ch=1))

content="\n".join(content)
print("\n\n"+content)

ch = input("\n\nDo you want to create the Licence.txt file:\n\t1: Yes\n\t2: No\nChoice: ")
if ch=="1":
    a=open("Licence.txt","w")
    a.write(content)
    a.close()
