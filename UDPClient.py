# import socket 
# # be able to create a socket 
# from socket import *
# # Pass either the IP address or the hostname of the server ((do ifconfig to get the IP Address)
# serverName = '10.120.70.106' 
# serverPort = 2600
# # AF_INET means IPv4 
# # SOCK_DGRAM means UDP
# clientSocket = socket(AF_INET, SOCK_DGRAM)
# # raw_input for python 2.x
# message = input('Input lowercase sentence:') 
# # converts to byte type 
# clientSocket.sendto(message.encode(),(serverName, serverPort))
# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
# print(modifiedMessage.decode())
# clientSocket.close()

