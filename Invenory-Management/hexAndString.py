hexa={'0':"0000",'1':"0001",'2':"0010",'3':"0011",'4':"0100",'5':"0101",'6':"0110",'7':"0111",
   '8':"1000",'9':"1001",'a':"1010",'b':"1011",'c':"1100",'d':"1101",'e':"1110",'f':"1111" }
bina={'0000':'0','0001':'1','0010':'2','0011':'3','0100':'4','0101':'5','0110':'6','0111':'7',
    '1000':'8','1001':'9','1010':'a','1011':'b','1100':'c','1101':'d','1110':'e','1111':'f'}

def string2hex(string):
    string_len=len(string)
    string=[("00000000"+bin(ord(string[i]))[2:])[-8:] for i in range(string_len)]
    string=''.join(string)
    he=""
    for i in range(0,string_len*8,4):
        he+=bina[string[i:i+4]]
    temp=16-(len(he)%16)
    he+="0"*temp
    res=[he[i:i+16] for i in range(0,len(he),16)] + [("0"*16+(hex(temp))[2:])[-16:]]
    return res

def hex2string(he):
    temp=int("0x"+he[-1],16)
    he="".join(he[:-1])
    he=he[:-1*temp]
    he=[hexa[he[i]] for i in range(len(he))]
    he="".join(he)
    string=[]
    for i in range(0,len(he),8):
        string.append(chr(int("0b"+he[i:i+8],2)))
    string="".join(string)
    return string

"""
a=string2hex("Vishal@Haswani@25")
# a=['56697368616c4048', '617377616e694032', '3500000000000000', '000000000000000e']
print(a)
a=hex2string(a)
# a="Vishal@Haswani@25"
print(a)
"""
