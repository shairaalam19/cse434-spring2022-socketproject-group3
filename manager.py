from http import client
import random
from socket import *
import json
from collections import namedtuple
import random
from copy import deepcopy
from math import ceil
from math import floor
from threading import Thread

playerPorts = [] # just player ports 
playerNames = [] # just player names 
gameCounter = 0
games = {}
playersInfo = {} # all info
availToPlay = {} # players that are NOT in a game 
deck = {}
# ex) 
# games = {
# 	1: {
# 		player: [ip, port, [card, card, card, card, card, card], score],
# 		player: [ip, port, [card, card, card, card, card, card], score],
# 		round: 0
# 		dealer: name 
# 		stock : [card, ... card]
# 		discard: [card, ... card]
# 	},
# 	2: {
# 		player: [ip, port, [card, card, card, card, card, card], score],
# 		player: [ip, port, [card, card, card, card, card, card], score],
# 		round: 0
# 		dealer: name
# 		stock: [card, ... card]
# 		discard: [card, ... card]
# 	}
# }
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

# SOCKET FUNCTION-----------------------------------------------------------------------------------------------

# sets up the socket 
def setupServer():
	global serverPort
	global serverSocket
	serverPort = 2700
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

# CARD FUNCTIONS-----------------------------------------------------------------------------------------------

def createDeck(): 
	global deck
	Card = namedtuple('Card', ['value', 'suit'])
	suits = ["D", "C", "H", "S"]
	values = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
	deck = [Card(value, suit) for value in values for suit in suits]
	# to print: 
	# print(deck[0].value, deck[0].suit)
	return deck 

# SCORING CARDS 

# Returns value of the individual card to calculate score 
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

# calculates score of all cards that is passed 
def totalScore(cards): 
    total = 0
    for i in range (0, len(cards)): 
        card = cards[i].value
        value = cardValue(card)
        if value != False:
            total += value
    return total

# calculates score of shown cards 
# cards: player's cards 
# show: up to how many cards to calculate score of 
def partialScore(cards, show):
    total = 0
    for i in range (0, show): 
        card = cards[i].value 
        value = cardValue(card)
        if value != False:
            total += value
    return total

# PRINTING CARDS

# return value of card to print as deck in game 
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

# Can print any cards in set for player
# cards : the player's cards 
# show : how many cards to actually show and how many stay hidden 
# return printable : string of cards to print 
def printPlayerCards(cards, show):
	printable = ""
	count = 0
	# first row 
	for i in range (0, int(floor(len(cards)/2)) ): 
		if count < show:
			card = cards[i].value
			value = printCardValue(card)
			printable += value + cards[i].suit + " "
		else: 
			printable += "*** "
		count += 1
	printable += "\n"

	# 2nd row 
	for i in range (int(ceil(len(cards)/2)), len(cards)): 
		if count < show:
			card = cards[i].value
			value = printCardValue(card)
			printable += value + cards[i].suit + " "
		else: 
			printable += "*** "
		count += 1
	printable += "\n"
	return printable

# ASSIGNING CARDS 

# assign random cards to each player 
# stores the stock and discard piles in the game dicitonary 
def assignCards(game): 
	global deck 
	
	# gets all the players' names in the game 
	# keys = list(game) 

	# gets all the values of the players in the game  
	# values = list(game.values())

	# copy the original deck in stock pile  
	stock = deepcopy(deck) 

	# gets random 6 cards for EACH player 
	# for i in range (0, len(game)):
	for name in game: 
		# get name of player 
		# name = keys[i]
		# assigns cards to each player 
		if name != 'round' and name != 'stock' and name != 'discard' and name != 'dealer':
			# get value of player 
			# player: IP, port, cards, score 
			# value = list(values[i])
			value = game.get(name)

			# get returned stock with remaining cards in deck 
			stock, playerCards = randomCardsToPlayer(stock)

			# add cards to player details 
			value.append(playerCards)
			# slot for score in player details 
			value.append(0)
			player = dict({name:value})
			game.update(player)

	# adds the stock pile to the game 
	stockPile = dict({"stock":stock})
	game.update(stockPile)

	# initializes the discard pile 
	discard = []
	discardPile = dict({"discard":discard})
	game.update(discardPile)

	# print("Game details: ", json.dumps(game), "\n")

	# returns game info and stock deck 
	return game

# gets random 6 cards from stock pile 
# return stock, playerCards : stock is the remaining cards, playerCards is the 6 random cards for player 
def randomCardsToPlayer(stock): 
	playerCards = []
	# gets 6 random cards for ONE player 
	for i in range (0, 6):
		cardIndex = random.randint(0, len(stock)-1)
		card = stock.pop(cardIndex)
		playerCards.append(card)
	return stock, playerCards 

# returns top card on pile 
def topCard(pile): 
	if len(pile) == 0:
		top = "EMPTY"
	else: 
		top = pile.pop(0)
	return top

# gets a random card from given cards 
def randomCard(cards): 
	cardIndex = random.randint(0, len(cards))
	card = cards.pop(cardIndex)
	return card

# GAME FUNCTIONS-----------------------------------------------------------------------------------------------

def check(dealer, k):
	reply = ''
	totalPlayers = k + 1 
	# checks if dealer exists 
	if dealer not in playerNames: 
		reply = 'FAILURE'
	# checks if number of additional players are in range 1 <= k <= 3 
	# min = 2, max = 4
	elif k < 1 or k > 3:
		reply = 'FAILURE'
	# checks if enough players available to play for the game 
	elif len(availToPlay) < totalPlayers:
		reply = 'FAILURE'
	else: 
		reply = 'SUCCESSFUL'
	return reply

# adds the players to a game 
# total number of players = k + 1 
def start(dealer, k): 
	global playerNames
	global availToPlay
	global playersInfo
	global deck

	reply = ''
	totalPlayers = k + 1 
	# checks if dealer exists 
	if dealer not in playerNames: 
		reply = 'FAILURE'
	# checks if number of additional players are in range 1 <= k <= 3 
	# min = 2, max = 4
	elif k < 1 or k > 3:
		reply = 'FAILURE'
	# checks if enough players available to play for the game 
	elif len(availToPlay) < totalPlayers:
		reply = 'FAILURE'
	else: 
		# new game dictionary
		newGame = {}	

		# Take out dealer from available players list 
		dealerInfo = availToPlay.pop(dealer)
		# store in array for game 
		newGame.update(dict({dealer:dealerInfo}))
		newGame.update(dict({"dealer":str(dealer)}))

		# get random players and store in newGame   
		for i in range(1, totalPlayers): # min = 2, max = 4 (already registered 1)
			# get new player info 
			newPlayerName = random.choice(list(availToPlay))
			newPlayerInfo = availToPlay.pop(newPlayerName)
			newPlayer = dict({newPlayerName:newPlayerInfo})
			newGame.update(newPlayer) # add to dict of newGame
		
		# setting a game identifier
		gameIdentifier = 1
		while gameIdentifier in games: 
			gameIdentifier = gameIdentifier + 1

		# updating ALL the games 
		games.update({gameIdentifier : newGame}) # add to games 

		# assign cards to every new player 
		# creates stock and discard piles 
		assignCards(newGame)
		# adds feature about which round it is in 
		round = dict({"round":0})
		newGame.update(round)

		winner = play(newGame)
		print(winner)

		# send to client here 
		reply = 'GAME OVER'
		# reply = json.dumps(newGame)

	return reply

# iterates through each round and determines score 
def play(game):
	global serverSocket
	# get round 
	round = game.get("round")
	# iterates through each round 
	while round < 6:
		# iterate through each player 
		# for i in range (0, len(game)):
		print("Round ", str(round+1), ": \n")
		for name in game:
			# game = {
			# 	player : IP, port, cards[], score
			# }
			
			# get name of player 
			if name != 'round' and name != 'stock' and name != 'discard' and name != 'dealer':
				# get values of player 
				# value = values[i]
				value = game.get(name)

				# get IP of players 
				ip = value[0]
				
				# get port 
				port = value[1]

				# get cards of player 
				cards = value[2]

				# SEND TO CLIENT
				print(name)
				print(ip)
				print(port)

				# Telling client what round it is 
				reply = "ROUND " + str(round+1) + ":"
				print(reply)
				serverSocket.sendto(reply.encode(),(ip,port))

				# sending client the rounds it is in 
				reply = printPlayerCards(cards, round+1)
				print(reply)
				serverSocket.sendto(reply.encode(),(ip,port))
				
				discard = game.get("discard")

				reply = topCard(discard)
				reply = json.dumps(reply)
				print(reply)
				serverSocket.sendto(reply.encode(),(ip,port))

				# get score at this point in round 
				score = partialScore(cards, round+1)

				topPlayer, topScore = winner(game)
				
				# currently not winning, so switch cards 
				if topScore < score: 
					# get stock pile 
					stock = game.get("stock")
					# get top of stock pile 
					swapCard = randomCard(stock)
					# swap cards with the stock pile 
					cards, oldCard = swap(cards, round, swapCard)
					# update player cards 
					# value = game.get(name)
					value[2] = cards 

					# put the oldCard in the discard pile 
					discard = game.get("discard")
					discard.insert(0, oldCard)
					score = partialScore(cards, round+1)

					# SEND TO CLIENT
					reply = "SWAP: \n" + printPlayerCards(cards, round+1)
					print(reply)
					serverSocket.sendto(reply.encode(),(ip,port))

				# update score for player in game 
				value[3] = score
				player = dict({name:value})
				game.update(player)

		# increment round 
		round += 1
		game.update({"round":round})
		# print(json.dumps(game))
		# PRINT TO EACH OF THE PLAYERS AND WHAT THEIR CARDS LOOK LIKE IN THE ROUND 

	# game done and send winner 
	winningPlayer, winningScore = winner(game)

	return winningPlayer

# cards : player cards 
# oldIndex : the card it wants to swap with 
# newCard : the card from the discard/stock pile 
# return cards, oldCard : returns the new set of cards of the players, returns the discarded card that goes back to the pile 
def swap(cards, oldIndex, newCard): 
    oldCard = cards.pop(oldIndex)
    cards.insert(oldIndex, newCard)
    return cards, oldCard

# calculate who is winner in game and their score 
def winner(game):

	playerScores = {}

	# iterates through all of the players' scores 
	for name in game:
		# get name of player 
		# name = players[i]
		if name != 'round' and name != 'stock' and name != 'discard' and name != 'dealer':
			# get values of player 
			# value = values[i]
			value = game.get(name)

			# get score of player 
			score = value[3]

			# get total score 
			# score = totalScore(cards)

			# update the dictionary of all players scores 
			playerScore = dict({name:score})
			playerScores.update(playerScore)
	
	# print(json.dumps(playerScores))

	# find the one with the lowest score 
	winner = min(playerScores, key=playerScores.get)

	return winner, playerScores.get(winner)

# end the game and put back all the players in game into availToPlay 
def end(gameIdentInput, dealer):
	global games
	reply = ''
	endedGame = {}
	# print("Before game end:")
	# print("availToPlay: ", json.dumps(availToPlay))
	# print("games: ", json.dumps(games))
	if gameIdentInput.isnumeric():
		gameIdentifier = int(gameIdentInput)
		if gameIdentifier in games:
			game = games.get(gameIdentifier)
			playersName = list(game)
			gameDealer = playersName[0]
			if dealer != gameDealer:
				reply = 'FAILURE. dealer is not correct.'
			else: 
				# remove game from game identifier 
				endedGame = games.pop(gameIdentifier)
				# get all the players info 
				playersInfo = list(endedGame.values())

				# iterate through all the players 
				for i in range(0, len(playersInfo)): 
					# get name, IP, port of each player and store back in availToPlay 
					name = playersName[i]
					if name != 'round' and name != 'stock' and name != 'discard' and name != 'dealer':
						ip = playersInfo[i][0]
						port = playersInfo[i][1]
						info = [ip, port]
						player = dict({name:info})
						# store back into availToPlay so that these players can be another game again 
						availToPlay.update(player)
				reply = 'SUCCESSFUL'
				print("After game end:")
				print("availToPlay: ", json.dumps(availToPlay))
				print("games: ", json.dumps(games))
		else:
			reply = 'FAILURE. gameIdentifier is not a game.'
	else: 
		reply = 'FAILURE. gameIdentifier is not numeric.'
		print(json.dumps(games))
	
	return reply

# COMMANDS-----------------------------------------------------------------------------------------------

# takes in the command that client chose and determines outputs based on that 
def clientCmd(message,clientIP,clientPort):
	global serverPort
	global serverSocket
	global playerNames
	global games
	# print("Beginning of clientCmd")
	# print("message:", message)

	cmd_list = message.split( )
	action = cmd_list[0]

	# COMMAND STRUCTURE 
	# register <user> <IP address> <port0> <port1> <port2>
	# action player_name player

	if action == 'register':
		player_port = int(cmd_list[3]) # fourth argument in message received
		player_name = (cmd_list[1]) # name is second argument

		# print('player port is: ', player_port, '\n')
		# print(playerPorts, '\n')

		reply = ''
		# registered = register(player_name, clientIP, player_port)
		registered = register(player_name, clientIP, clientPort)

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
			reply = check(dealer, k)
			# game can start 
			if reply == 'SUCCESSFUL':
				sendMsg(reply, clientIP, clientPort)
				reply = start(dealer,k)
				sendMsg(reply, clientIP, clientPort)
			# game is not eligible to start and tells the player that 
			else:
				sendMsg(reply, clientIP, clientPort)
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
		reply = ''
		name = cmd_list[1]
		if name in playerNames: 
			removedInfo = playersInfo.pop(name)
			playerNames.remove(name)
			playerPorts.remove(removedInfo[1])
			reply = 'SUCCESSFUL'
		else: 
			reply = 'FAILURE'

		#print('All player ports:',playerPorts)
		#print('All player names:',playerNames)
		print('After de-registering: ', playersInfo, '\n')
		# del playersInfo[name]
		# playerNames.remove(name)
		serverSocket.sendto(reply.encode(),(clientIP,clientPort))
	# print("End of clientCmd")


# def main():
# 	setupServer()
# 	# creates base deck to use 
# 	createDeck() 
# 	while True:
# 		message,clientIP,clientPort = receiveMsg() #decoded msg
# 		clientCmd(message,clientIP,clientPort)

# def create_thread(message,clientIP,clientPort):
#     clientCmd(message,clientIP,clientPort)

def main():
    setupServer()
    # creates base deck to use 
    createDeck() 
    while True:
        message,clientIP,clientPort = receiveMsg() #decoded msg
        thread_new = Thread(target=clientCmd,args=[message,clientIP,clientPort])
        thread_new.start()
        #message,(clientIP,clientPort) = serverSocket.recvfrom(2048)
        #print(message.decode())
        

if __name__ == "__main__":
    main()

