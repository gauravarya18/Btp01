import socket		 	 
import sys
import binascii
import time

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

def ReverseApplicationLayer(Data):
    print("In Reverse Application layer")
    print("Header LH5 added to the data")
    
    idx=0
    for i in range(len(Data)):
        if (Data[i]=='-'):
            idx=i
            break
    
    AppData=Data[idx+1:]
    time.sleep(5)
    print(AppData)
    return AppData

def ReverseTransportLayer(AppData):
    print("In Reverse Transport Layer")
    print("Header LH4 removed to the data")
    
    idx=0
    for i in range(len(AppData)):
        if (AppData[i]=='-'):
            idx=i
            break
    
    TransData=AppData[idx+1:]
    time.sleep(5)
    print(TransData)
    return TransData

def ReverseNetworkLayer(TransData):
    print("In Reverse Network Layer")
    print("Header LH3 removed to the data")

    idx=0
    for i in range(len(TransData)):
        if (TransData[i]=='-'):
            idx=i
            break
    
    NetData=TransData[idx+1:]

    time.sleep(5)
    print(NetData)
    return NetData



s = socket.socket() 	  		 # Create a socket object
host = socket.gethostname()                    # Get local machine name
port = int(4444)
s.bind((host, port)) 			 # Bind to the port
s.listen(5) 			         # Now wait for client connection.
print("Server is up and running")


while True:
     c, addr = s.accept() 		# Establish connection with client.
     print('Got connection from', addr)
     print(" '~'  is corrsponding to the errorneous bit")

     Num=0
     while True:
        #recieve the final string (error induced)
        message=c.recv(1024).decode()

        #recieve the xor string
        parity=c.recv(1024).decode()
        j=0

        # print(message)
        # print(parity)
        print("------------------------------------------------")
        if message == "quit":
            c.send("Quit".encode())
            break
        else:
            
            AnsStr=""
            #roving over the parity string
            for j in range(0,len(parity)):

                #to store the number
                Num=0

                #to store the corresponding temp. xor
                tmp=0

                #roving over the corresponding message string
                for i  in  range(j*8,j*8+8):
                    if(message[i]=="1"):
                        tmp^=1
                    else:
                        tmp^=0
                
                tempChar=text_from_bits(message[j*8:j*8+8])

                if(parity[j]!=str(tmp)):
                    #corresponding to the erroreneous bit
                    # print("~",Decode(Num-1))
                    AnsStr+="~"
                    AnsStr+=str(tempChar)
                else:
                    # print(Decode(Num-1))
                    AnsStr+=str(tempChar)
            
            print(AnsStr)

            AnsStr=ReverseNetworkLayer(AnsStr)
            print("---------------------------------------------")

            AnsStr=ReverseTransportLayer(AnsStr)
            print("---------------------------------------------")

            AnsStr=ReverseApplicationLayer(AnsStr)
            print("---------------------------------------------")

            print(AnsStr)
            c.send(message.encode())
          

     c.close() 			# Close the connection.
     
