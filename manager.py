from http import client
import random
from socket import *
import json
from collections import namedtuple
import random
from copy import deepcopy
from math import ceil
from math import floor

playerPorts = [] # just player ports 
playerNames = [] # just player names 
gameCounter = 0
games = {}
playersInfo = {} # all info
availToPlay = {} # players that are NOT in a game 
deck = {}
printCardValue = {
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

# SOCKET FUNCTION 

# sets up the server socket 
def setupServer():
	global serverPort
	global serverSocket
	serverPort = 2600
	serverSocket = socket(AF_INET,SOCK_DGRAM)
	serverSocket.bind(('',serverPort))
	print("The manager is ready to receive... \n")

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
		print(player_name + " is registered \n")
		
	return registered;

# CARD FUNCTIONS

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
def printPlayerCards(cards, show):
	printable = ""
	count = 0
	for i in range (0, int(floor(len(cards)/2)) ): 
		if count < show:
			value = printCardValue.get(cards[i].value)
			printable += value + cards[i].suit + " "
		else: 
			printable += "*** "
		count += 1
	printable += "\n"
	for i in range (int(ceil(len(cards)/2)), len(cards)): 
		if count < show:
			value = printCardValue.get(cards[i].value)
			printable += value + cards[i].suit + " "
		else: 
			printable += "*** "
		count += 1
	return printable

def assignCards(game): 
	global deck 
	
	# gets all the players' names in the game 
	keys = list(game) 

	# gets all the values of the players in the game  
	values = list(game.values())

	# gamedeck 
	stock = deepcopy(deck) 

	# gets random 6 cards for EACH player between the first player and the last player 
	for i in range (0, len(game)):
		# get name of player 
		key = keys[i]
		# get key of player 
		value = values[i]
		# get returned stock with remaining cards in deck 
		stock, playerCards = randomCardsToPlayer(stock)

		# updated game dictionary to also add the cards that each player has 
		value.append(playerCards)
		player = dict({key:value})
		game.update(player)
		# print("Player: ", key)
		# print(printPlayerCards(playerCards, 2))

	print("Game details: ", json.dumps(game))
	# returns game info and stock deck 
	return game, stock

def randomCardsToPlayer(stock): 
	playerCards = []
	# gets 6 random cards for ONE player 
	for i in range (0, 6):
		cardIndex = random.randint(0, len(stock)-1)
		card = stock.pop(cardIndex)
		playerCards.append(card)
	return stock, playerCards 

def randomCard(stock): 
	cardIndex = random.randint(0, len(stock))
	card = stock.pop(cardIndex)
	return stock, card

# GAME FUNCTIONS

def start(dealer, k): 
	global playerNames
	global availToPlay
	global playersInfo
	global deck

	reply = ''
	if dealer not in playerNames: 
		reply = 'FAILURE'
	# 1 <= k <= 3 
	elif k < 1 or k > 3:
		reply = 'FAILURE'
	elif len(availToPlay) < k+1:
		reply = 'FAILURE'
	else: 
		# new game 
		newGame = {}	

		# setting index 0 as dealer 
		# Take out dealer from available players list 
		dealerInfo = availToPlay.pop(dealer)
		# store in array for game 
		newGame.update(dict({dealer:dealerInfo}))

		# get random players   
		for i in range(1, k+1): # gets at least 1 other player up until max 4 
			# get new player info 
			newPlayerName = random.choice(list(availToPlay))
			newPlayerInfo = availToPlay.pop(newPlayerName)
			newPlayer = dict({newPlayerName:newPlayerInfo})
			newGame.update(newPlayer) # add to dict of newGame

		# ex) 
		# games = {
		# 	1: {
		# 		player: playerInfo,
		# 		player: playerInfo
		# 	},
		# 	2: {
		# 		player: playerInfo,
		# 		player: playerInfo
		# 	}
		# }
		
		# setting a game identifier
		gameIdentifier = 1
		while gameIdentifier in games: 
			gameIdentifier = gameIdentifier + 1

		# updating ALL the games 
		games.update({gameIdentifier : newGame}) # add to games 

		# print("Current available players: ", json.dumps(availToPlay))
		# print("Current games: ", json.dumps(games))
		# print("Current game: ", json.dumps(newGame))
		# print("Current deck: ", json.dumps(deck))

		assignCards(newGame)

		reply = 'SUCCESSFUL'

	return reply

def end(gameIdentInput, dealer):
	global games
	reply = ''
	endedGame = {}
	
	if gameIdentInput.isnumeric():
		gameIdentifier = int(gameIdentInput)
		if gameIdentifier in games:
			game = games.get(gameIdentifier)
			playersName = list(game)
			gameDealer = playersName[0]
			if dealer != gameDealer:
				reply = 'FAILURE. dealer is not correct.'
				print(dealer)
			else : 
				endedGame = games.pop(gameIdentifier)
				playersInfo = list(endedGame.values())
				for i in range(0, len(playersInfo)): 
					# get IP and port of each player and store back in availToPlay 
					ip = playersInfo[i][0]
					port = playersInfo[i][1]
					name = playersName[i]
					info = [ip, port]
					player = dict({name:info})
					availToPlay.update(player)
				reply = 'SUCCESSFUL'
				# print("Updated availToPlay: ", json.dumps(availToPlay))
	else: 
		reply = 'FAILURE. gameIdentifier does not exist.'
		print(json.dumps(games))
	
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

		print('player port is: ', player_port, '\n')
		print(playerPorts, '\n')

		reply = ''
		registered = register(player_name, clientIP, player_port)
		
		if registered is True:
			reply = 'SUCCESSFUL'
			print(reply, '\n')
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		else:
			reply = 'FAILURE'
			print(reply, '\n')
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))

		# Printing players info 
		#print('All player ports:',playerPorts)
		#print('All player names:',playerNames)
		print('All players info:', playersInfo, '\n')

	if action == 'query':
		if cmd_list[1] == 'games':
			reply = json.dumps(games) 
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
		
	if action == 'end': 
		gameIdentifier = cmd_list[1]
		dealer = cmd_list[2]	
		reply = end(gameIdentifier, dealer)

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
		print('After de-register:', playersInfo, '\n')
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
