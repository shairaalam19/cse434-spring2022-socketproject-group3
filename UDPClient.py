# be able to create a socket 
from socket import *

def deregister(clientSocket): 
    clientSocket.close()

def main(): 
    # Pass either the IP address or the hostname of the server ((do ifconfig to get the IP Address)
    serverName = '10.120.70.106' 
    serverPort = 2600
    # AF_INET means IPv4 
    # SOCK_DGRAM means UDP
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    message = input('Input lowercase sentence:') 

    # converts string to byte type and sends to server IP+port
    clientSocket.sendto(message.encode(),(serverName, serverPort))

    # recieves message from server and gets server IP 
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    # prints message 
    print(modifiedMessage.decode())

    end = input("End Program (y/n)?")

    while True: 
        # raw_input for python 2.x
        message = input('Input lowercase sentence:') 

        # SEND TO SERVER
        # converts string to byte type and sends to server IP+port
        clientSocket.sendto(message.encode(),(serverName, serverPort))

        # RECEIVE FROM SERVER
        # recieves message from server and gets server IP 
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

        # OTHER USE
        # prints message 
        print(modifiedMessage.decode())

        end = input("End Program (y/n)?")

        deregister(clientSocket)

        while end != "y" and end != "n":
                end = input("Incorrect input. Enter 'y' or 'n' for 'Yes' or 'No'.\nEnd Program (y/n)?")

        if end == "y":
            break;
        elif end == "n":
            continue;


if __name__ == "__main__":
    main()

