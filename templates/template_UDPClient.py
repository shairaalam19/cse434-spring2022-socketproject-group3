# be able to create a socket 
from socket import *
# Pass either the IP address or the hostname of the server ((do ifconfig to get the IP Address)
serverName = '10.120.70.106' 
serverPort = 2600
# AF_INET means IPv4 
# SOCK_DGRAM means UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)

# User input 
message = input('Input lowercase sentence:') 

# converts string to byte type and sends to server IP+port
clientSocket.sendto(message.encode(),(serverName, serverPort))

# recieves message from server and gets server IP 
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# prints message 
print(modifiedMessage.decode())

clientSocket = socket(AF_INET, SOCK_DGRAM)
