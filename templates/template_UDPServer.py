from socket import *

# sets port 
serverPort = 2600
# creat esocket 
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The manager (server) is ready to receive")
while True:
    # gets message from a client 
    message, clientAddress = serverSocket.recvfrom(2048)
    # convert message from bytes to string and make uppercase 
    modifiedMessage = message.decode().upper()
    # sends message back to client 
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)