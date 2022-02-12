# be able to create a socket 
from asyncio.windows_events import NULL
from socket import *

def deregister(clientSocket): 
    clientSocket.close()

def main(): 
    # Pass either the IP address or the hostname of the server ((do ifconfig to get the IP Address)
    serverIP = '10.120.70.106' 
    serverPort = 2600
    # AF_INET means IPv4 
    # SOCK_DGRAM means UDP
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # message = input('Input lowercase sentence:') 

    # converts string to byte type and sends to server IP+port
    # clientSocket.sendto(message.encode(),(serverName, serverPort))

    # recieves message from server and gets server IP 
    # modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    # prints message 
    # print(modifiedMessage.decode())

    # end = input("End Program (y/n)?")

    while True: 
        # Sending clientIP and clientPort information to server
        empty = ""

        # SEND TO SERVER
        # converts string to byte type and sends to server IP+port
        # clientSocket.sendto(empty.encode(),(serverIP, serverPort))

        # RECEIVE FROM SERVER
        # recieves message from server and gets server IP 
        # modifiedMessage, (serverIP, serverPort) = clientSocket.recvfrom(2048)
        # modifiedMessage = modifiedMessage.decode()
        # ---------------------------------------------------
        # OTHER USE
        # prints message 
        # print(modifiedMessage)

        menu = "Choose from the following: \n"
        menuItems = "Register Player [1] \nDe-register Player [2] \nQuery Players [3] \nQuery Games [4]\n"
        menuInput = "Input Menu Choice: "
        print(menu)
        print(menuItems)
        menuChoice = input(menuInput)

        # Check
        valid = True    
        if not menuChoice.isnumeric(): 
            valid = False
        else:
            if int(menuChoice) != 1 and int(menuChoice) != 2 and int(menuChoice) != 3 and int(menuChoice) != 4:
                valid = False

        while not valid: 
            print("Input choice was incorrect. Choose in number format\n")
            print(menu)
            print(menuItems)
            menuChoice = input(menuInput)
            # Check
            valid = True    
            if not menuChoice.isnumeric(): 
                valid = False
            else:
                if int(menuChoice) != 1 and int(menuChoice) != 2 and int(menuChoice) != 3 and int(menuChoice) != 4:
                    valid = False

        # menuChoice = int(menuChoice)
        clientSocket.sendto(menuChoice.encode(),(serverIP, serverPort)) 

        choiceFeedback, (serverIP, serverPort) = clientSocket.recvfrom(2048)
        choiceFeedback = choiceFeedback.decode()
        if choiceFeedback != "":
            userInput = input(choiceFeedback)
            clientSocket.sendto(userInput.encode(),(serverIP, serverPort)) 
            



        # END PROGRAM PROMPT

        # end = input("End Program (y/n)?")

        # # deregister(clientSocket)

        # while end != "y" and end != "n":
        #         end = input("Incorrect input. Enter 'y' or 'n' for 'Yes' or 'No'.\nEnd Program (y/n)?")

        # if end == "y":
        #     break;
        # elif end == "n":
        #     continue;


if __name__ == "__main__":
    main()

