from http import client, server
from socket import *

playerName = ''
cards = {}

def setupServer():
    global serverIP
    global serverPort
    global clientSocket
    serverIP = '10.120.70.106' 
    serverPort = 2600
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    #if clientSocket:
        #print('connected')

def printMenu():
    menu = "Enter one of the following commands: \n"
    menuItems = "\nregister <user> <IPv4-address> <port> \nquery players \nstart game <user> <k> \nquery games \nend <game-identifier> <user>\nde-register <user> \n\n"
    return menu + menuItems

def cardValue(card): 
    # cardValue = {
    #     "A" : 1, 
    #     "2" : -2,
    #     "3" : 3,
    #     "4" : 4,
    #     "5" : 5,
    #     "6" : 6,
    #     "7" : 7,
    #     "8" : 8,
    #     "9" : 9,
    #     "10" : 10,
    #     "J" : 10,
    #     "Q" : 10,
    #     "K" : 0
    # }
    cardValue = {
        "A" : 1, 
        2 : -2,
        3 : 3,
        4 : 4,
        5 : 5,
        6 : 6,
        7 : 7,
        8 : 8,
        9 : 9,
        10 : 10,
        "J" : 10,
        "Q" : 10,
        "K" : 0
    }
    return cardValue.get(card, "FAILURE")

def playerScore(cards): 
    total = 0
    for i in cards: 
        total += 0
    return total

def commandClient():
    global serverIP
    global serverPort
    global clientSocket
    global playerName

    # COMMAND STRUCTURE 
	# register <user> <IP address> <port0> <port1> <port2>
	# action player_name player

    # Print menu for player 
    commandPrompt = printMenu()

    # WAITING HERE UNTIL USER RESPONSE 
    commandChoice = input(commandPrompt) #command to sent to sever

    # splits user inputs into array
    cmdChoice_list = commandChoice.split( )

    #gives the first word in command 
    action = cmdChoice_list[0] 
    #print(action)

    # Specific to command action 
    if action == 'register': 
        if playerName == '':
            sendMsg(commandChoice,serverIP,serverPort)
            # clientSocket.sendto(commandChoice.encode(),(serverIP,serverPort))
            #reply = receiveMsg()
            reply,(serverIP,serverPort) = clientSocket.recvfrom(2040)

            # decode reply from server 
            reply_de = reply.decode()
            # print(reply_de)
            if reply_de == 'SUCCESSFUL':
                print('SUCCESSFUL \n')
                playerName = cmdChoice_list[1]
                # return reply
            elif reply_de == 'FAILURE': 
                print('FAILURE')
                commandClient()
            elif reply_de == '':
                print('NO REPLY \n')
        else: 
            print('FAILURE. No player name.')
            commandClient()
    
    if action == 'query':
        sendMsg(commandChoice,serverIP,serverPort)
        reply,(serverIP,serverPort) = clientSocket.recvfrom(2040)
        reply_de = reply.decode()
        print(reply_de, '\n')
    
    if action == 'start':
        if cmdChoice_list[1] == 'game':
            sendMsg(commandChoice, serverIP, serverPort)
            reply,(serverIP,serverPort) = clientSocket.recvfrom(2040)
            reply_de = reply.decode()
            print(reply_de , '\n')
        else: 
            print('FAILURE. Command not correct.')
            commandClient()

    if action == 'end':
        sendMsg(commandChoice, serverIP, serverPort)
        reply,(serverIP,serverPort) = clientSocket.recvfrom(2040)
        reply_de = reply.decode()
        print(reply_de , '\n')

    if action == 'de-register':
        sendMsg(commandChoice,serverIP,serverPort)
        reply,(serverIP,serverPort) = clientSocket.recvfrom(2040)
        reply_de = reply.decode()

        if reply_de == 'SUCCESSFUL':
            print(reply_de, '\n')
            playerName = ''
            # closes client 
            return reply_de 
        # ADDED
        elif reply == 'FAILURE': 
            print('FAILURE')
            commandClient()
        elif reply == '':
            print('NO REPLY \n')
            

def sendMsg(message, IP, Port):
    global serverIP
    global serverPort
    global clientSocket
    if clientSocket:
        clientSocket.sendto(message.encode(),(IP,Port))
    else:
        print("clientSocket is empty")

def receiveMsg():
    global serverIP
    global serverPort
    global clientSocket
    message,(serverIP,serverPort) = clientSocket.recvfrom(2040)
    message = message.decode()
    return message, serverIP, serverPort


setupServer() #set up

while True: 
    message = commandClient() #get input command
    if message == 'SUCCESSFUL':
        print("Closing client socket.")
        clientSocket.close()
        break;
    #print(message)
    