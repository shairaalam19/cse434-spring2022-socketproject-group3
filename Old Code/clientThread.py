# Import socket module
import socket
from socket import *  
 
def main():
    serverIP = '10.120.70.106' 
    serverPort = 2700
 
    clientSocket = socket(AF_INET,SOCK_STREAM)
 
    # connect to server on local computer
    clientSocket.connect((serverIP,serverPort))
 
    # message you send to server
    # message = "Hello from Client"

    while True:
        # print("Inside while True")

        # SEND MESSAGE TO SERVER
        message = input("Send message to client: ")
        # message sent to server
        clientSocket.send(message.encode())
 
        # RECEIVE MESSAGE FROM SERVER
        # message received from server
        data = clientSocket.recv(2048)
        message = data.decode()
        # print the received message
        print(message)
 
        # # ask the client whether he wants to continue
        # ans = input('\nDo you want to continue(y/n) :')

        # if ans == 'y':
        #     continue
        # else:
        #     break

    # close the connection
    clientSocket.close()
 
if __name__ == '__main__':
    main()