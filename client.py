import socket		 	 
import sys
import ipaddress
import queue
import time
import binascii

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
    Data=input("\n Please provide the input Data or 'quit' to quit: ")
    size=len(Data)
    flag=False

    if(Data=="quit"):
        flag=True

    if(not(flag)):
        #Data in application layer
        print("-----------------------**********************************************************-------------------------")
        Data=ApplicationLayer(Data)
        print("---------------------------------------------")

        #Data in Transport Layer
        Data=TransportLayer(Data)
        print("---------------------------------------------")

        #Data in Network Layer
        Data=NetworkLayer(Data)
        print("---------------------------------------------")

        # print(Data)
        strInBinary=convertToBinary(Data)
        xorfinal=""

        for i in range(0,len(strInBinary),8):
            tmp=0
            for j in range(i,i+8):
                tmp^=0 if int(strInBinary[j])==0 else 1
            xorfinal+=str(tmp)

        #induce error
        size=96+size*8

        inp=input("Position you want to induce error(97-"+str(size)+") in or press -1 if you don't want any error ")
        if(inp=="-1"):
            strToSend=strInBinary
        else:
            x=int(strInBinary[int(inp)])
            x=(x+1)%2

            #error induced message at position inp
            strToSend=strInBinary[:int(inp)]+str(x)+strInBinary[int(inp)+1:]


                # print(xorfinal)
                # print(strfinal)
        # print(strToSend)     
        xorfinal+="$"+Data
        # print(xorfinal)
        s.send(strToSend.encode())
        s.send(xorfinal.encode())
        # s.send(Data.encode())
        
    else:
        s.send(qu.encode())
        # s.send(qu.encode())
        s.send(qu.encode())

    result = s.recv(1024).decode()       
    # 1024 is recv_size

    if result == "Quit":
        print("Closing client connection, goodbye")
        break
    else:
        print("orgnl message:", strInBinary)
        print("The answer is:", result)           

s.close 				 # Close the socket when done
