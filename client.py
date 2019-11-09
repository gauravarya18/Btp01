import socket		 	 
import sys
import ipaddress
import queue
import time
import binascii
import numpy as np
from matplotlib.pyplot import step, show

def binary_data(data):
    return [1 if x in data else 0 for x in range(data[-1] + 1)]
def xor(a, b): 
    result = [] 
   
    
    for i in range(1, len(b)): 
        if a[i] == b[i]: 
            result.append('0') 
        else: 
            result.append('1') 
   
    return ''.join(result) 
   
   
def mod2div(divident, divisor): 
   
    pick = len(divisor) 
   
    tmp = divident[0 : pick] 
   
    while pick < len(divident): 
   
        if tmp[0] == '1': 
            tmp = xor(divisor, tmp) + divident[pick] 
        else:   
            tmp = xor('0'*pick, tmp) + divident[pick] 
   
        pick += 1
   
    if tmp[0] == '1': 
        tmp = xor(divisor, tmp) 
    else: 
        tmp = xor('0'*pick, tmp) 
   
    checkword = tmp 
    return checkword 
   

def encodeData(data, key): 
   
    l_key = len(key) 

    appended_data = data + '0'*(l_key-1) 
    remainder = mod2div(appended_data, key) 
   
    codeword = remainder 
    return codeword     

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def convertToBinary(Tstr):
    return text_to_bits(Tstr)

def ApplicationLayer(Data):
    print("In Application layer")
    print("Header LH5 added to the data")
    AppData="LH5-"+Data
    print(AppData)
    time.sleep(5)
    return AppData

def TransportLayer(AppData):
    print("In Transport Layer")
    print("Header LH4 added to the data")
    TransData="LH4-"+AppData
    print(TransData)
    time.sleep(5)
    return TransData

def NetworkLayer(TransData):
    print("In Network Layer")
    print("Header LH3 added to the data")
    NetData="LH3-"+TransData
    print(NetData)
    time.sleep(5)
    return NetData
#1 2 4 5 7     1  3 4 6 7    2 3 4 8      8 7 6 5
def Redundancy_Bit(Data,TemperedData):
    
    r1=int(Data[6],2)^int(Data[5],2)^int(Data[3],2)^int(Data[2],2)^int(Data[0],2)
    r2=int(Data[4],2)^int(Data[3],2)^int(Data[6],2)^int(Data[1],2)^int(Data[0],2)
    r4=int(Data[3],2)^int(Data[4],2)^int(Data[5],2)
    r8=int(Data[0],2)^int(Data[1],2)^int(Data[2],2)
    Ans=TemperedData[0:3]+str(r8)+TemperedData[3:6]+str(r4)+TemperedData[6]+str(r2)+str(r1)
    

    return Ans

def Physical_Layer(ans,choice):
    data=[]
    if(choice=="1"):
        flag=True
        for i in  range (len(ans)):
            if(ans[i]=="1"):
                flag=not(flag)
            if(flag):
                data.append(i+1)
    elif(choice=="2"):
        for i in  range (0,2*len(ans),2):
            print(i)
            if(ans[i//2]=="0"):
                data.append(i+1)
            else:
                data.append(i+2)
            

    
    bindata = binary_data(data)
    xaxis = np.arange(0, data[-1] + 1)
    yaxis = np.array(bindata)
    step(xaxis, yaxis)
    show()



s = socket.socket() 	  		 # Create a socket object
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)
host = str(ipaddress.ip_address(IPAddr))     # Reading IP Address
port = int(4444)                           # Reading port number
s.connect((host, port))                           # Connecting to server
print("The IP address of the server is:", host)
print("The port number of the server is:", port)
qu="quit"


while(True):
    Data=input("\nPlease provide the input Data or 'quit' to quit: ")
    size=len(Data)
    flag=False

    if(Data=="quit"):
        flag=True

    if(not(flag)):
        #Data in application layer
        print("-----------------------****************-------------------------")
        Data=ApplicationLayer(Data)
        print("---------------------------------------------")

        #Data in Transport Layer
        Data=TransportLayer(Data)
        print("---------------------------------------------")

        #Data in Network Layer
        Data=NetworkLayer(Data)
        print("---------------------------------------------")

        # print(Data)
        strInBinary=""
        for i in range (len(Data)):
            temp_=convertToBinary(Data[i])
            strInBinary+=temp_[1:]
        
        xorfinal=""

        for i in range(0,len(strInBinary),7):
            tmp=0
            for j in range(i,i+7):
                tmp^=0 if int(strInBinary[j])==0 else 1
            xorfinal+=str(tmp)

        #induce error
        size=84+size*7-1
        Tech=input("Enter  \n1.) XOR Detection  \n2.) CRC Detection\n3.)Hamming Code Detection and Correction\n")
        inp=input("Position you want to induce error(84-"+str(size)+") in or press -1 if you don't want any error::")
        choice=input("Choice of your Physical Layer Encoding Scheme \n1.)NRZ-I\n2.)Manchester\n")
        if(inp=="-1"):
            strToSend=strInBinary
        else:
            x=int(strInBinary[int(inp)])
            x=(x+1)%2

            #error induced message at position inp
            strToSend=strInBinary[:int(inp)]+str(x)+strInBinary[int(inp)+1:]

        if(Tech=="1"):
            Physical_Layer(("00"+strToSend),choice)
            s.send(("00"+strToSend).encode())
            s.send(xorfinal.encode())
        elif(Tech=="2"):
            key = "1001"
            ans=""
            for i in range(0,len(strInBinary)//7):
                ans+=encodeData(strInBinary[i*7:i*7+7],key)
            Physical_Layer(("01"+strToSend),choice)
            s.send(("01"+strToSend).encode()) 
            s.send(ans.encode())   
        else:  
            ans="" 
            for i in range(0,len(strInBinary)//7):
                ans+=Redundancy_Bit(strInBinary[i*7:i*7+7],strToSend[i*7:i*7+7])
            # print(strInBinary)
            # print(strToSend)
            Physical_Layer(("10"+ans),choice)
            s.send(("10"+ans).encode()) 
            # print(ans)
            #s.send(ans.encode()) 
        
    
        
    else:
        s.send(qu.encode())
        s.send(qu.encode())

    result = s.recv(1024).decode()       
    # 1024 is recv_size

    if result == "Quit":
        print("Closing client connection, goodbye")
        break
    else:
        # print("orgnl message:", strInBinary)
        print("The answer is:", result)           

s.close 				 # Close the socket when done
