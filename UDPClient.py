# be able to create a socket 
from socket import *
# Pass either the IP address or the hostname of the server (like general.asu.edu)
serverName = 'hostname' 
serverPort = 12000
# AF_INET means IPv4 
# SOCK_DGRAM means UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input('Input lowercase sentence:')
clientSocket.sendto(message.encode(),(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()