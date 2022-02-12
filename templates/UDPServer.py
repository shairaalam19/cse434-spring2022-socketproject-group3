from socket import *

serverPort = 2500
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
host = gethostname()
#ip = gethostbyname(host)
#print("host IP: ",ip)
print("The server is ready to recieve")

register = 'register'
reg_encode = 'You are registering'
name = 'Enter Name: '
send = 'Sending from server'
while True:
	
	#send = send.encode()
	
	#message,clientAddress = serverSocket.recvfrom(2048)
	#modifiedMessage = message.decode().upper()
	action,clientAddress = serverSocket.recvfrom(2048)
	serverSocket.sendto(send.encode(),clientAddress)
	action_mod = action.decode()
	if action_mod == register:
		serverSocket.sendto(reg_encode.encode(),clientAddress)
		client_name,clientAddress = serverSocket.recvfrom(2048)
		#name_mod = name.decode()
		#print(name_mod)
		#print(name)
	#serverSocket.sendto(modifiedMessage.encode(),clientAddress)
	#serverSocket.sendto(mod_name.encode(),clientAddress)
	#print("Client IP: ",clientAddress)
