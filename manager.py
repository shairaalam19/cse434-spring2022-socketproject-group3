from http import client
from socket import *
import json

playerPorts = [] # just player ports 
playerNames = [] # just player names 
gameCounter = 0
games = {}
playersInfo = {} # all info

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

def register(player_name, clientIP, player_port): 
	global playerPorts
	registered = False
	if (player_name not in playerNames) and (player_port not in playerPorts):
		playerNames.append(player_name) # updating player names 
		playerPorts.append(player_port) # updating player ports 

		# Updating total info 
		info = [clientIP, player_port]
		new_player = dict({player_name:info})
		playersInfo.update(new_player)
		
		registered = True
		print(player_name + " is registered")
		
	return registered;


# takes in the command that client chose and determines outputs based on that 
def clientCmd(message,clientIP,clientPort):
	global serverPort
	global serverSocket
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
		count = 0

		# Update the array of players 
		# if (player_name not in playerNames) and (player_port not in playerPorts):
		# 	playerNames.append(player_name)
		# 	#count += 1
		# 	#if player_port not in playerPorts:
		# 	playerPorts.append(player_port)
		# 	count += 1
		registered = register(player_name, clientIP, player_port)
		
		# responds to the clients 
		# if count == 1:
		# 	info = [clientIP, player_port]
		# 	new_player = dict({player_name:info})
		# 	playersInfo.update(new_player)
		# 	reply = 'SUCCESSFUL'
		# 	# CHANGED
		# 	# sendMsg(reply, clientIP, clientPort) 
		# 	serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		# else:
		# 	reply = 'FAILURE'
		# 	# CHANGED
		# 	# sendMsg(reply, clientIP, clientPort) 
		# 	serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		if registered is True:
			# info = [clientIP, player_port]
			# new_player = dict({player_name:info})
			# playersInfo.update(new_player)
			reply = 'SUCCESSFUL'
			# CHANGED
			# sendMsg(reply, clientIP, clientPort) 
			print(reply)
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		else:
			reply = 'FAILURE'
			# CHANGED
			# sendMsg(reply, clientIP, clientPort) 
			print(reply)
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))

		# Printing players info 
		#print('All player ports:',playerPorts)
		#print('All player names:',playerNames)
		print('All players info:', playersInfo)

	if action == 'query':
		if cmd_list[1] == 'games':
			reply = '0' 
			# CHANGED
			# sendMsg(reply, clientIP, clientPort)
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		if cmd_list[1] == 'players':
			reply = json.dumps(playersInfo)
			# CHANGED
			# sendMsg(reply, clientIP, clientPort)
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))

	if action == 'de-register':
		name = cmd_list[1]
		if name in playerNames: 
			playersInfo.pop(name)
			reply = 'SUCCESSFUL'
		else: 
			reply = 'FAILURE'
		# CHANGED
		# sendMsg(reply, clientIP, clientPort)
		serverSocket.sendto(reply.encode(),(clientIP,clientPort))

		#print('All player ports:',playerPorts)
		#print('All player names:',playerNames)
		print('After de-register:', playersInfo)
		# del playersInfo[name]
		# playerNames.remove(name)

				

def main():
	setupServer()
	while True:
		message,clientIP,clientPort = receiveMsg() #decoded msg
		#message,(clientIP,clientPort) = serverSocket.recvfrom(2048)
		#print(message.decode())
		clientCmd(message,clientIP,clientPort)
        

if __name__ == "__main__":
    main()
