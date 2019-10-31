import socket		 	 # Import socket module
import sys
import ipaddress
import queue 
temp = queue.LifoQueue(maxsize=6)
def Convert_Binary(x):
    #print(x)
    while(x>0):
        temp.put(x%2)
        x//=2

    while(temp.qsize()<6):
        temp.put(0)


def  Encoding(equ):
    if(equ=="quit"):
        L.put(-1)
    else:   
        Len=len(equ)
        for i in range(Len):
            if(equ[i]==' '):
                L.put(0)
            else:
                x=ord(equ[i])-97
                if(x<0):
                    x+=32
                L.put(x+1)
        
        
L = queue.Queue(maxsize=20)


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
    equ=input("\n Please provide the input or Q to quit: ")
    Encoding(equ)
    
    #binary of the whole message excluding xor
    strfinal=""

    #stores the parity
    xorfinal=""
    flag=False
    while(L.qsize()>0):
        p=L.get()
        if(p==-1):
            flag=True
            break
        
        Convert_Binary(p)
            
        #temporary binary conversion
        str1=""

        #storing the xor of current slot of 6
        tmp=0
        for i in  range(6):

            y=temp.get()
            if(y==0):
                str1+="0"
                tmp^=0
            else:
                str1+="1"
                tmp^=1
                
        #reset            
        temp = queue.LifoQueue(maxsize=6)
        
        strfinal+=str1
        xorfinal+=str(tmp)
            
    
    if(not(flag)):
        #induce error
        inp=input("Position you want to induce error in ")

        x=int(strfinal[int(inp)])
        x=(x+1)%2

        #error induced message at position inp
        strToSend=strfinal[:int(inp)]+str(x)+strfinal[int(inp)+1:]


                # print(xorfinal)
                # print(strfinal)
                
        s.send(strToSend.encode())
        s.send(xorfinal.encode())
    else:
        s.send(qu.encode())
        s.send(qu.encode())

    result = s.recv(1024).decode()       
    # 1024 is recv_size
    if result == "Quit":
        print("Closing client connection, goodbye")
        break
    else:
        print("orgnl message:", strfinal)
        print("The answer is:", result)           

s.close 				 # Close the socket when done
