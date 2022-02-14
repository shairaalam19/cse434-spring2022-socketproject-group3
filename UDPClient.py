# be able to create a socket 
from socket import *

# serverIP = '10.120.70.106' 
# serverPort = 2600
# clientSocket = socket(AF_INET, SOCK_DGRAM)

registered = False
regName = ""

def setupClient(): 
    global serverIP 
    global serverPort 
    global clientSocket 
    # Pass either the IP address or the hostname of the server ((do ifconfig to get the IP Address)
    serverIP = '10.120.70.106' 
    serverPort = 2600
    # AF_INET means IPv4 
    # SOCK_DGRAM means UDP
    clientSocket = socket(AF_INET, SOCK_DGRAM)

def end(): 
    global serverIP 
    global serverPort 
    global clientSocket
    # END PROGRAM PROMPT

    # end = input("End Program (y/n)?")

    # # deregister(clientSocket)

    # while end != "y" and end != "n":
    #         end = input("Incorrect input. Enter 'y' or 'n' for 'Yes' or 'No'.\nEnd Program (y/n)?")

    # if end == "y":
    #     break;
    # elif end == "n":
    #     continue;
    clientSocket.close()

def receiveMessage():
    global serverIP 
    global serverPort 
    global clientSocket
    # message, clientAddress = serverSocket.recvfrom(2048)
    message, (serverIP, serverPort) = clientSocket.recvfrom(2048)
    # convert message from bytes to string and make uppercase 
    message = message.decode()
    return message, (serverIP, serverPort)

def sendMessage(message, IP, Port): 
    global serverIP 
    global serverPort 
    global clientSocket
    if clientSocket:
        clientSocket.sendto(message.encode(), (IP, Port))
    else: 
        print("clientSocket is empty")

def printMenu():
    menu = "Choose from the following: \n"
    menuItems = "Register Player [1] \nDe-register Player [2] \nQuery Players [3] \nQuery Games [4]\nEnd Program [5]"
    menuInput = "Input Menu Choice: "
    print(menu)
    print(menuItems)
    return menuInput

def validMenuChoice(menuChoice):
    valid = True    
    if not menuChoice.isnumeric(): 
        valid = False
    else:
        if int(menuChoice) != 1 and int(menuChoice) != 2 and int(menuChoice) != 3 and int(menuChoice) != 4 and int(menuChoice) != 5:
            valid = False
    return valid

def menu():
        global serverIP 
        global serverPort 
        global clientSocket
        global registered
        global regName

        menuChoice = input(printMenu())

        while not validMenuChoice(menuChoice): 
            print("\nInput choice was incorrect. Choose in number format.\n")
            menuChoice = input(printMenu())

        if int(menuChoice) != 5:
            # Send menu choice to server 
            sendMessage(menuChoice, serverIP, serverPort) 

            # Just registers or deregisters, so it expects a response from the server and then sends message 
            if int(menuChoice) == 1 or int(menuChoice) == 2:
                # receive message from server about the specific menu choice 
                serverResponse, (serverIP, serverPort) = receiveMessage()
                
                # user reacts to message from server 
                userInput = input(serverResponse)

                # send user input to server 
                sendMessage(userInput, serverIP, serverPort)

                print("\n")
            # Just querying, only expects response from server 
            else: 
                # gets query messages 
                serverResponse, (serverIP, serverPort) = receiveMessage()
                print(serverResponse)
                print("\n")
            
        return menuChoice

def main(): 
    setupClient()
    
    global serverIP 
    global serverPort 
    global clientSocket 

    while True: 
        # message = input("Send a message to server: ")
        # clientSocket.sendto(message.encode(), (serverIP, serverPort))
        # sendMessage(message, serverIP, serverPort)

        menuChoice = menu()
        if int(menuChoice) == 5:
            break;



if __name__ == "__main__":
    main()

