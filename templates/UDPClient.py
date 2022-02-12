from socket import *
serverName = '10.120.70.106'
serverPort = 2500
clientSocket = socket(AF_INET,SOCK_DGRAM)
message = input('Enter Action: ')
clientSocket.sendto(message.encode(),(serverName,serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()