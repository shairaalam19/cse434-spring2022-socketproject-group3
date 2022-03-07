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
playerIPs = []
gameCounter = 0
games = {}
playersInfo = {} # all info
availToPlay = {} # players that are NOT in a game 
deck = {}
# ex) 
# games = {
# 	1: {
# 		player: [ip, port, [card, card, card, card, card, card], score, show],
# 		player: [ip, port, [card, card, card, card, card, card], score, show],
# 		maxCardShowing: 0, # the 
# 		holes: 0, # number of iterations 
# 		dealer: name,
# 		stock: [card, ... card]
# 		discard: [card, ... card]
# 	},
# 	2: {
# 		player: [ip, port, [card, card, card, card, card, card], score, show],
# 		player: [ip, port, [card, card, card, card, card, card], score, show],
# 		maxCardShowing: 0, # the 
# 		holes: 0, # number of iterations 
# 		dealer: name,
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
    global playerIPs

    registered = False
    if (player_name not in playerNames) and (player_port not in playerPorts):
        playerNames.append(player_name) # updating player names 
        playerPorts.append(player_port) # updating player ports 
        playerPorts.append(player_port) # updating player ports 
        if clientIP not in playerIPs:
            playerIPs.append(clientIP)

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
	showCards = []
	dups = []

	# get all the cards up until the certain value 
	for i in range (0, show): 
		card = cards[i].value 
		showCards.append(card)

	calculate = removeDups(showCards)

	for card in calculate:
		total += cardValue(card)

	return total

def removeDups(cards):
    showCards = []
    for card in cards: 
        if card not in showCards:
            showCards.append(card)
        else: 
            index = showCards.index(card)
            showCards.pop(index)
    return showCards

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

# return individual card printable version 
def printCard(card):
	# print("inside printCard()", json.dumps(card))
	# print(str(card.value))
	# print(json.dumps(card))
	value = printCardValue(card[0])
	printable = value + card[1]
	# print(printable)
	return printable


# ASSIGNING CARDS 

# assign random cards to each player 
# stores the stock and discard piles in the game dicitonary 
def initializeCards(game): 
	global deck 
	
	# gets all the players' names in the game 
	# keys = list(game) 

	# gets all the values of the players in the game  
	# values = list(game.values())

	# copy the original deck in stock pile  
	stock = deepcopy(deck) 
	discard = []
	# gets random 6 cards for EACH player 
	# for i in range (0, len(game)):
	for name in game: 
		# get name of player 
		# name = keys[i]
		# assigns cards to each player 
		if name != 'maxCardShowing' and name != 'stock' and name != 'discard' and name != 'dealer' and name != 'hole':
			# print("Assigning cards to: ", name)
			# get value of player 
			# player: IP, port, cards, score 
			# value = list(values[i])
			value = game.get(name)

			# get returned stock with remaining cards in deck 
			stock, discard, playerCards = randomCardsToPlayer(stock, discard)

			# add cards to player details 
			value.append(playerCards)
			# print("playerCards: \n", json.dumps(playerCards))

			# slot for score in player details 
			value.append(0)
			# slot for how many are cards are showing 
			value.append(2)
			player = dict({name:value})
			game.update(player)

	# adds the stock pile to the game 
	game.update({"stock":stock})

	# initializes the discard pile 
	firstDiscard = randomCard(stock)
	discard.insert(0,firstDiscard)
	game.update({"discard":discard})

	# print("Game details: ", json.dumps(game), "\n")

	# returns game info and stock deck 
	return game

# assign random cards to each player 
# stores the stock and discard piles in the game dicitonary 
def reassignCards(game): 
	# gets random 6 cards for EACH player 

	stock = game.get("stock")
	discard = game.get("discard")
	for name in game: 
		# get name of player 
		# name = keys[i]
		# assigns cards to each player 
		if name != 'maxCardShowing' and name != 'stock' and name != 'discard' and name != 'dealer' and name != 'hole':
			# get value of player 
			# player: IP, port, cards, score 
			# value = list(values[i])
			value = game.get(name)

			# get returned stock with remaining cards in deck 
			stock, discard, cards = randomCardsToPlayer(stock, discard)

			# add cards to player details 
			value[2] = cards
			# slot for how many are cards are showing 
			value[4] = 2
			# update game 
			game.update({name:value})

	# adds the stock pile to the game 
	game.update({"stock":stock})

	# updating the discard if it needed to restock 
	game.update({"discard":discard})

	# returns game info and stock deck 
	return game

# gets random 6 cards from stock pile 
# return stock, playerCards : stock is the remaining cards, playerCards is the 6 random cards for player 
def randomCardsToPlayer(stock, discard): 
	# print("Inside randomCardsToPlayer()")
	# print("stock:\n", json.dumps(stock))
	# print("discard:\n", json.dumps(discard))
	playerCards = []
	# gets 6 random cards for ONE player 
	for i in range (0, 6):
		cardIndex = random.randint(0, len(stock)-1)
		
		if len(stock) == 0: 
			# print("stock is empty")
			restock(stock, discard)
		
		card = stock.pop(cardIndex)
		# print(json.dumps(card))
		playerCards.append(card)
		# print(json.dumps(playerCards))	

	# print("After getting random 6 cards")
	# print("stock:\n", json.dumps(stock))
	# print("discard:\n", json.dumps(discard))	
	return stock, discard, playerCards 

# returns top card on pile 
def topCard(pile): 
	if len(pile) == 0:
		top = "EMPTY"
	else: 
		top = pile.pop(0)
	return top

# gets a random card from given cards 
def randomCard(cards): 
	# print("Inside randomCard()")
	cardIndex = random.randint(0, len(cards)-1)
	# print("cardIndex:", cardIndex)
	card = cards.pop(cardIndex)
	# print(json.dumps(card))
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

	# INITIALIZING GAME -----------------------------------------------------------------------------------

	# new game dictionary
	newGame = {}	

	# Take out dealer from available players list 
	dealerInfo = availToPlay.pop(dealer)
	# store in array for game 
	newGame.update(dict({dealer:dealerInfo}))
	newGame.update(dict({"dealer":str(dealer)}))

	# NEED CONFIRMATION FROM CLIENT 
	# ip = dealerInfo[0]
	# port = dealerInfo[1]
	# reply = "game"
	# serverSocket.sendto(reply.encode(),(ip,port))
	# # ISSUE: confirm could be command argument from other client 
	# confirm, ip, port = receiveMsg() # stalls here until confirms 
	# print("Player: ", dealer, "'s confirmation message: ", confirm)

	# get random players and store in newGame   
	for i in range(1, totalPlayers): # min = 2, max = 4 (already registered 1)
		# get new player info 
		newPlayerName = random.choice(list(availToPlay))
		# ip, port
		newPlayerInfo = availToPlay.pop(newPlayerName)
		newPlayer = dict({newPlayerName:newPlayerInfo})
		newGame.update(newPlayer) # add to dict of newGame

		# # NEED CONFIRMATION FROM CLIENT 
		ip = newPlayerInfo[0]
		port = newPlayerInfo[1]
		reply = "game"
		serverSocket.sendto(reply.encode(),(ip,port))
		# confirm, ip, port = receiveMsg() # stalls here until confirms (should be max 5 second confirmation) and all in play()
		# print("Player: ", newPlayerName, "'s confirmation message: ", confirm)

	
	# setting a game identifier
	gameIdentifier = 1
	while gameIdentifier in games: 
		gameIdentifier = gameIdentifier + 1

	# updating ALL the games 
	games.update({gameIdentifier : newGame}) # add to games 

	# assign cards to every new player 
	# creates stock and discard piles 
	initializeCards(newGame)
	# adds feature about which maxCardShowing it is in (shows how many cards to show )
	newGame.update({"maxCardShowing":2})
	
	# how many holes it is in (max 9)
	newGame.update({"hole":0})

	# print(json.dumps(newGame))

	# PLAY GAME ---------------------------------------------------------------------

	winner = play(newGame, gameIdentifier)
	print("WINNER:", winner)

	# send to client here 
	reply = 'GAME OVER'
	# reply = json.dumps(newGame)

	for name in newGame:
        # get name of player 
		if name != 'maxCardShowing' and name != 'stock' and name != 'discard' and name != 'dealer' and name != 'hole':
			value = newGame.get(name)
			# get IP of players 
			ip = value[0]			
			# get port 
			port = value[1]

			sendMsg(reply, ip, port)

			reply = 'no'

			sendMsg(reply, ip, port)

			info = [ip, port]
			availToPlay.update({name:info})
		# if name == newGame.get("dealer"):
		# 	value = newGame.get(name)
		# 	# get IP of players 
		# 	ip = value[0]			
		# 	# get port 
		# 	port = value[1]

		# 	reply = 'no'

		# 	sendMsg(reply, ip, port)

		# 	info = [ip, port]
		# 	availToPlay.update({name:info})


	# end(gameIdentifier, dealer)
    
	return reply

# iterates through each hole and iteration of players and determines score 
def play(game, gameIdentifier):
	global serverSocket
	
	# sends to players what the game identifier is 
	for name in game:
		# get name of player 
		if name != 'maxCardShowing' and name != 'stock' and name != 'discard' and name != 'dealer' and name != 'hole':
			value = game.get(name)
			# get IP of players 
			ip = value[0]			
			# get port 
			port = value[1]

			reply = "Game Identifier: " + str(gameIdentifier)
			sendMsg(reply, ip, port)

	# get maxCardShowing - how many cards to show 
	maxCardShowing = game.get("maxCardShowing")
	hole = game.get("hole")

	# iterate through all the holes 
	while hole < 1:
		print("Hole: ", hole, "\n")
		# iterates through each player until 6 cards show for the first time  
		# increments the maxCardShowing when a player swaps a card (can only increment once per iteration)
		# maxCardShowing = 2

		while maxCardShowing <= 6:
			# swap = if something has been taken from the stock pile 
			swap = False

			# iterate through all the players 
			for name in game:
				# get name of player 
				if name != 'maxCardShowing' and name != 'stock' and name != 'discard' and name != 'dealer' and name != 'hole':
					# get values of player 
					value = game.get(name)

					# get IP of players 
					ip = value[0]				
					# get port 
					port = value[1]
					# get cards of player 
					cards = value[2]
					# how many it is currently showing on the deck (max 6)
					show = value[4]

					# SEND TO CLIENT
					print(name)
					print(ip)
					print(port)

					# SENDING HOLE
					reply = "HOLE " + str(hole) + ":"
					print(reply)
					sendMsg(reply, ip, port)

					# SENDING CARDS TO PLAYER
					reply = printPlayerCards(cards, show)
					print(reply)
					serverSocket.sendto(reply.encode(),(ip,port))
					
					# SENDING DISCARD CARD TO PLAYER
					# get the discard 
					discard = game.get("discard")
					# print("Discard", json.dumps(discard))

					topDiscard = discard[0]
					# print("topDiscard")
					# print(topDiscard)
					cardPoints = cardValue(topDiscard[0])
					# print(json.dumps(topDiscard))
					# print("topDiscard", json.dumps(topDiscard))
					# printedDiscard = printCard(topDiscard)
					# print("printedDiscard: ", printedDiscard )
					
					if printCard(topDiscard) == False: 
						reply = "Discard: no discarded cards" 
					else: 
						reply = "Discard:" + printCard(topDiscard)

					print(reply)
					sendMsg(reply, ip, port)

					# CALCULATE INFO TO DETERMINE DECISION 

					# get score of current player 
					score = partialScore(cards, show) # value[3]

					# get score of current top player 
					topPlayer, topScore = winner(game)

					# get the current stock 
					stock = game.get("stock")

					# if there's nothing in the stock 
					if len(stock) == 0: 
						restock(stock, discard)

					# calculate if theres dupes so far in player's cards 
					subCards = cards[0:show]
					subCards = removeDups(subCards)
					# print(subCards)

					# get average of cards 
					sum = 0
					# values = list(subCards.values())
					for card in subCards:
						point = cardValue(card)
						sum += point
					average = sum/len(subCards)

					# print(topScore)
					# print(score)

					# DECISION
					# 1) swap player card with randomCard(stock): if topScore < score 
					if topScore < score: 
						# print("inside topScore < score")
						stockCard = randomCard(stock)
						cards, oldCard = swapCard(cards, show-1, stockCard)
						value[2] = cards
						# print(json.dumps(cards))
						# value.insert(2, cards)
						discard = game.get("discard") # gets the discard pile 
						discard.insert(0, oldCard) # discards the old card 
						swap = True

						# increment how many cards are showing  
						value[4] += 1 # increments how many are showing for the player 
						show = value[4]

						# SEND TO CLIENT: prints updated cards 
						reply = "SWAP WITH STOCK PILE: \n" + printPlayerCards(cards, show)
						print(reply)
						serverSocket.sendto(reply.encode(),(ip,port))

					# 2) swap player card with topCard(discard)
					elif (topDiscard in subCards) or (average > cardPoints):
						# print("inside elif in play()")
						if topDiscard in subCards:
							matchIndex = subCards.index(topDiscard)
							randomIndex = random.randint(0, show-1)
							while randomIndex == matchIndex:
								randomIndex = random.randint(0, show-1)
							cards, oldCard = swapCard(cards, show-1, topDiscard)

						else: 
							cards, oldCard = swapCard(cards, show-1, topDiscard)

						value[2] = cards 
						discard.insert(0, oldCard)
						swap = True 

						# increment how many cards are showing 
						value[4] += 1 # increments how many are showing for the player 
						show = value[4]
						
						# SEND TO CLIENT: prints updated cards 
						reply = "SWAP WITH DISCARD PILE: \n" + printPlayerCards(cards, show)
						print(reply)
						serverSocket.sendto(reply.encode(),(ip,port))

					# 3) swap randomCard(stock) and put it onto the stack 
					else: 
						# print("inside else in play()")
						# it is restocked if it was empty 
						stockCard = randomCard(stock)
						discard.insert(0, stockCard)

						# do not update how many cards are showing 

						# SEND TO CLIENT: prints updated cards 
						reply = "FORFEIT STOCK CARD: \n" + printPlayerCards(cards, show)
						print(reply)
						serverSocket.sendto(reply.encode(),(ip,port))

					# update score for player in game 
					score = partialScore(cards, show-1)
					value[3] = score

					# update value for each player 
					# player: ip, port, cards, score, show 
					player = dict({name:value})
					game.update(player)
			
			if swap == True: 
				maxCardShowing += 1
			game.update({"maxCardShowing":maxCardShowing})
			# print(json.dumps(game))

		playerCount = 0;
		for name in game: 
			if name != 'maxCardShowing' and name != 'stock' and name != 'discard' and name != 'dealer' and name != 'hole':
				playerCount += 1
				info = game.get(name)
				cards = info[2]
				for card in cards: 
					discard.insert(0, card)
		
		cardCount = playerCount * 6

		if len(stock) <= cardCount: 
			restock(stock, discard)

		hole += 1
		game.update({"hole":hole})

	# game done and send winner 
	winningPlayer, winningScore = winner(game)

	return winningPlayer

# if stock is empty, then reshuffle with the discard 
def restock(game):
	stock = game.get("stock")
	discard = game.get("discard")
    	
	stock = stock + discard 
	discard = []
	discardedCard = randomCard(stock)
	discard.insert(0, discardedCard)

	game.update({"stock":stock})
	game.update({"discard":discard})

# cards : player cards 
# oldIndex : the card it wants to swap with 
# newCard : the card from the discard/stock pile 
# return cards, oldCard : returns the new set of cards of the players, returns the discarded card that goes back to the pile 
def swapCard(cards, oldIndex, newCard): 
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
		if name != 'maxCardShowing' and name != 'stock' and name != 'discard' and name != 'dealer' and name != 'hole':
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

				# for name in endedGame: 
				# 	if name != 'maxCardShowing' and name != 'stock' and name != 'discard' and name != 'dealer' and name != 'hole':
				# 		value = endedGame.get(name)
				# 		ip = value[0]
				# 		port = value[1]
				# 		info = [ip, port]
				# 		availToPlay.update({name:info})

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
			print(reply)
			# game can start 
			if reply == 'SUCCESSFUL':
				sendMsg(reply, clientIP, clientPort) # sends back "SUCCESSFUL"
				reply = start(dealer,k) # sends back "GAME OVER"
				sendMsg(reply, clientIP, clientPort)
				reply = 'no' # sends back "no"
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

	if action == '?':
		reply = ''
		# available = False
		# for player in availToPlay:
        #     # player : ip, port
		# 	value = availToPlay.get(player) 
		# 	ip = value[0]
		# 	port = value[1]
		# 	if clientIP == ip and clientPort == port:
		# 		available = True
		# 		break
        # ip and port wasn't found in availToPlay
		if cmd_list[1] not in availToPlay:
			reply = "game"
			print(reply, "to ", cmd_list[1])
			sendMsg(reply, clientIP, clientPort)
        # found in availToPlay
		else:
			reply = "no"
			print(reply, "to ", cmd_list[1])
			sendMsg(reply, clientIP, clientPort)

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

