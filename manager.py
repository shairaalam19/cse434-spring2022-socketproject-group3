from http import client
import random
from socket import *
import json
from collections import namedtuple
import random

playerPorts = [] # just player ports 
playerNames = [] # just player names 
gameCounter = 0
games = {}
playersInfo = {} # all info
availToPlay = {} # players that are NOT in a game 
deck = {}

# sets up the server socket 
def setupServer():
	global serverPort
	global serverSocket
	serverPort = 2600
	serverSocket = socket(AF_INET,SOCK_DGRAM)
	serverSocket.bind(('',serverPort))
	print("The manager is ready to receive...")

# returns the decoded message and client's IP and port 
def receiveMsg():
	global serverPort
	global serverSocket
	if serverSocket:
		message,(clientIP,clientPort) = serverSocket.recvfrom(2048)
		message_decode = message.decode()
	return message_decode,clientIP,clientPort

# sends an encoded message to the given IP and port 
def sendMsg(message,IP,Port):
	global serverPort
	global serverSocket
	if serverSocket:
		serverSocket.sendto(message.encode(),(IP,Port))

def createDeck(): 
	global deck
	Card = namedtuple('Card', ['value', 'suit'])
	suits = ["D", "C", "H", "S"]
	values = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
	deck = [Card(value, suit) for value in values for suit in suits]
	# to print: 
	# print(deck[0].value, deck[0].suit)
	return deck 

# Can print any cards in set (can print players cards or all cards -> depends on tuples )
def printCards(cards):
	for i in range (0,51): 
		print(cards[i].value, cards[i].suit)

def shuffleCards(k): 
	global deck 
	cardIndex = ''
	card = ''
	stock = deck.copy()
	# deck for the specific game 
	game = [] 
	# gets random 6 cards for EACH player 
	for i in range (0, k+1):
		playerCards = []
		# gets 6 random cards for ONE player 
		for i in range (0, 6):
			cardIndex = random.randint(0, len(game))
			card = stock.pop(cardIndex)
			playerCards.append(card)
		# stores the set of 6 cards in te 
		game.append(playerCards)
    
	# returns game deck and stock deck 
	return game, stock 

def register(player_name, clientIP, player_port): 
	global playerPorts
	global availToPlay
	global playersInfo
	global playerNames
	global playerPorts
	
	registered = False
	if (player_name not in playerNames) and (player_port not in playerPorts):
		playerNames.append(player_name) # updating player names 
		playerPorts.append(player_port) # updating player ports 

		# Updating total info 
		info = [clientIP, player_port]
		new_player = dict({player_name:info})
		playersInfo.update(new_player)
		availToPlay.update(new_player)

		registered = True
		print(player_name + " is registered")
		
	return registered;

def start(dealer, k): 
	global newGame
	global playerNames
	global availToPlay

	reply = ''
	if dealer not in playerNames: 
		reply = 'FAILURE'
	elif k <= 0 or k >= 4:
		reply = 'FAILURE'
	elif len(playerNames) < k:
		reply = 'FAILURE'
	else: 
		# new game 
		newGame = []	
		# setting index 0 as dealer 
		dealerInfo = availToPlay.pop(dealer)
		newGame.append(dealerInfo) 
		for i in range(1, k+1):
			# get new player info 
			newName, [newIP, newPort] = random.choice(list(availToPlay.items()))
			newPlayer = newName, [newIP, newPort] 
			
			newGame.append(newPlayer) # add to array of game 
			availToPlay.pop(newName) # remove new player from availToPlay
		games.update(newGame) # add to games 
		reply = 'SUCCESSFUL'

	return reply

# takes in the command that client chose and determines outputs based on that 
def clientCmd(message,clientIP,clientPort):
	global serverPort
	global serverSocket
	global playerNames
	global games

	cmd_list = message.split( )
	action = cmd_list[0]

	# COMMAND STRUCTURE 
	# register <user> <IP address> <port0> <port1> <port2>
	# action player_name player

	if action == 'register':
		player_port = int(cmd_list[3]) # fourth argument in message received
		player_name = (cmd_list[1]) # name is second argument

		print('player port is: ', player_port)
		print(playerPorts)

		reply = ''
		registered = register(player_name, clientIP, player_port)
		
		if registered is True:
			reply = 'SUCCESSFUL'
			print(reply)
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		else:
			reply = 'FAILURE'
			print(reply)
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))

		# Printing players info 
		#print('All player ports:',playerPorts)
		#print('All player names:',playerNames)
		print('All players info:', playersInfo)

	if action == 'query':
		if cmd_list[1] == 'games':
			reply = '0' 
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		if cmd_list[1] == 'players':
			reply = json.dumps(playersInfo)
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))
	
	if action == 'start':
		dealer = cmd_list[2]
		k = cmd_list[3]
		reply = ''

		if k.isnumeric(): 
			k = int(k)
			reply = start(dealer, k)
		else: 
			reply = 'FAILURE'

		# return message 
		serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		
			

	if action == 'de-register':
		name = cmd_list[1]
		if name in playerNames: 
			playersInfo.pop(name)
			reply = 'SUCCESSFUL'
		else: 
			reply = 'FAILURE'
		serverSocket.sendto(reply.encode(),(clientIP,clientPort))

		#print('All player ports:',playerPorts)
		#print('All player names:',playerNames)
		print('After de-register:', playersInfo)
		# del playersInfo[name]
		# playerNames.remove(name)

def main():
	setupServer()
	# creates base deck to use 
	createDeck() 
	while True:
		message,clientIP,clientPort = receiveMsg() #decoded msg
		#message,(clientIP,clientPort) = serverSocket.recvfrom(2048)
		#print(message.decode())
		clientCmd(message,clientIP,clientPort)
        

if __name__ == "__main__":
    main()
