import socket		 	 # Import socket module
import sys
import ipaddress
import queue 
temp = queue.LifoQueue(maxsize=5)
def Convert_Binary(x):
    #print(x)
    while(x>0):
        temp.put(x%2)
        x//=2
        #print(x)
    #print(x)
    #print(temp.qsize())
    while(temp.qsize()<5):
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
    equ=input("Please give me your equation (Ex: 2+2) or Q to quit: ")
    Encoding(equ)
    while(L.qsize()>0):
        p=L.get()
        #print("h0")
        #print(p)
        if(p==-1):
            s.send(qu.encode())
        else:
            Convert_Binary(p)
            print("h1")
            str1=""
            for i in  range(5):
                y=temp.get()
                if(y==0):
                    str1+="0"
                else:
                    str1+="1"
                print(y)
            s.send(str1.encode())
    #print("h2")
    result = s.recv(1024).decode()       # 1024 is recv_size
    if result == "Quit":
        print("Closing client connection, goodbye")
        break
    elif result == "ZeroDiv":
        print("You can't divide by 0, try again")
    elif result == "MathError":
        print("There is an error with your math, try again")
    elif result == "SyntaxError":
        print("There is a syntax error, please try again")
    elif result == "NameError":
        print("You did not enter an equation, try again")
    else:
        print("The answer is:", result)

s.close 				 # Close the socket when done
