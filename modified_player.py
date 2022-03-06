from http import client, server
from socket import *
from http import client
import random
from socket import *
import json
from collections import namedtuple
import random
from copy import deepcopy
from math import ceil
from math import floor
import pickle
import time 

playerName = ''
cards = {}
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

def setupServer():
    global serverIP
    global serverPort
    global clientSocket
    serverIP = '10.120.70.106' 
    serverPort = 2700
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    #if clientSocket:
        #print('connected')

def play():
    global serverIP
    global serverPort
    reply = "confirm"
    sendMsg(reply.encode(), serverIP, serverPort)
    print("YOU ARE PLAYING A GAME \n")
    message, ip, port = receiveMsg() 
    while message != "GAME OVER": 
        print(message)
        message, ip, port = receiveMsg() 
        # gets all cards, the players, discard, stock pile 
        # game = json.loads(message)

    if message == 'GAME OVER':
        # # reply = reply.decode()
        # game = json.loads(reply)
        # # print(game)
        # print("PLAYERS: ")
        # for name in game: 
        #     if name != 'round' and name != 'stock' and name != 'discard' and name != 'dealer':
        #         value = game.get(name)
        #         # print(value)
        #         ip = value[0]
        #         port = value [1]
        #         cards = value[2]
        #         printCards = printPlayerCards(cards, 6)
        #         print(name, ':')
        #         print(printCards)
        print(reply)

def printMenu():
    menu = "Enter one of the following commands: \n"
    menuItems = "\nregister <user> <IPv4-address> <port> \nquery players \nstart game <user> <k> \nquery games \nend <game-identifier> <user>\nde-register <user> \n\n"
    print(menu + menuItems)
    # return menu + menuItems

def printCardValue(card): 
    cardPrint = {
		"A" : " A", 
		2 : " 2",
		3 : " 3",
		4 : " 4",
		5 : " 5",
		6 : " 6",
		7 : " 7",
		8 : " 8",
		9 : " 9",
		10 : "10",
		"J" : " J",
		"Q" : " Q",
		"K" : " K"
	}
    return cardPrint.get(card, False)

# return printable : string of cards to print 
def printPlayerCards(cards, show):
    printable = ""
    count = 0
    for i in range (0, int(floor(len(cards)/2))):
        if count < show:
            card = cards[i]
            num = printCardValue(card[0])
            suit = card[1]
            printable += num + suit + " "
        else: 
            printable += "*** "
        count += 1
    printable += "\n"
    for i in range (int(floor(len(cards)/2)), len(cards)):
        if count < show:
            card = cards[i]
            num = printCardValue(card[0])
            suit = card[1]
            printable += num + suit + " "
        else: 
            printable += "*** "
        count += 1
    printable += "\n"
    return printable

def cardValue(card): 
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
    return cardValue.get(card, False)

def totalScore(cards): 
    total = 0
    for i in range (0, len(cards)): 
        card = cards[i].value
        value = cardValue(card)
        if value != False:
            total += value
    return total

def partialScore(cards, show):
    total = 0
    for i in range (0, show): 
        card = cards[i].value 
        value = cardValue(card)
        if value != False:
            total += value
    return total

# cards : player cards 
# oldIndex : the card it wants to swap with 
# newCard : the card from the discard/stock pile 
# return cards, oldCard : returns the new set of cards of the players, returns the discarded card that goes back to the pile 
def swap(cards, oldIndex, newCard): 
    oldCard = cards.pop(oldIndex)
    cards.insert(oldIndex, newCard)
    return cards, oldCard

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

    # TIMERRRRRR
    # WAITING HERE UNTIL USER RESPONSE 
    commandChoice = input(commandPrompt) #command to sent to sever

    sec = 1
    start_time = time.time()
    
    passed = time.time() - start_time


    while passed < sec :
        if passed >= sec and commandChoice == None:
            return "empty"
        passed = time.time() - start_time


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
            # need confirmation that it is in game (checks all players in the game dictionary)
            reply,(serverIP,serverPort) = clientSocket.recvfrom(2040) # server says "game"
            reply = reply.decode()

            if reply == "game": 
                play()
            else:
                reply = "FAILURE"
                return reply 

            commandClient()
        else: 
            print('FAILURE. Command not correct.')
            commandClient()

    if action == 'end':
        sendMsg(commandChoice, serverIP, serverPort)
        reply,(serverIP,serverPort) = clientSocket.recvfrom(2040)
        reply_de = reply.decode()
        print(reply_de , '\n')

    if action == 'de-register':
        if cmdChoice_list[1] == playerName:
            sendMsg(commandChoice,serverIP,serverPort)
            reply,(serverIP,serverPort) = clientSocket.recvfrom(2040)
            reply_de = reply.decode()

            if reply_de == 'SUCCESSFUL':
                print(reply_de, '\n')
                playerName = ''
                # closes client 
                return 'SUCCESSFUL de-register' 
            elif reply_de == 'FAILURE': 
                print(reply_de, '. did not de-register\n')
                reply = commandClient()
                if reply == 'SUCCESSFUL':
                    return reply
            elif reply == '':
                print('NO REPLY \n')
        else:
            print('FAILURE. Not de-registering your player.', '\n')
            reply = commandClient()
            if reply == 'SUCCESSFUL':
                return reply
            

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
printMenu() # prints once 
# start_time = time.time() # starts a timer 
# end_time = 

while True: 
    clientSocket.settimeout(5)
    try:
        recvpack, (ip, port) = clientSocket.recvfrom(1024)
    except error:
        recvpack = None
    if recvpack == "game":
        play()
    else: 
        response = commandClient()
        # if response == "empty": don't do anything 
        if response == "SUCCESSFUL":
            print("Closing client socket.")
            clientSocket.close()
            break;