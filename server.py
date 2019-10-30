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
     count=0
     Num=0
     while True:
        equation=c.recv(1024).decode()
        if equation == "Q" or equation == "q" or equation == "Quit" or equation == "quit" or equation == "quit()":
            c.send("Quit".encode())
            break
        else:
            #Result=(Decode(equation))
            #print(equation)
            Num=0
            for i  in  range(5):
                Num*=2
                if(equation[i]=="1"):
                    Num+=1
            print(Decode(Num-1))
            

            
            c.send(equation.encode())
          

     c.close() 			# Close the connection.