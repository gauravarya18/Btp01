import socket		 	 # Import socket module
import sys
def Decode(Num):
    if(Num==-1):
        return " "
    return chr(Num+97)
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
     count=0
     Num=0
     while True:
        #recieve the final string (error induced)
        message=c.recv(1024).decode()

        #recieve the xor string
        parity=c.recv(1024).decode()
        j=0

        # print(message)
        # print(parity)
        print("--------------------------------------------------------------------------------------------------------------------------------------")
        if message == "Q" or message == "q" or message == "Quit" or message == "quit" or message == "quit()":
            c.send("Quit".encode())
            break
        else:
            
            #roving over the parity string
            for j in range(0,len(parity)):

                #to store the number
                Num=0

                #to store the corresponding temp. xor
                tmp=0

                #roving over the corresponding message string
                for i  in  range(j*6,j*6+6):
                    Num*=2
                    if(message[i]=="1"):
                        Num+=1
                        tmp^=1
                    else:
                        tmp^=0
                
                if(parity[j]!=str(tmp)):
                    #corresponding to the erroreneous bit
                    print("~",Decode(Num-1))
                else:
                    print(Decode(Num-1))
            

            
            c.send(message.encode())
          

     c.close() 			# Close the connection.
