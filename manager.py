from http import client
from socket import *
import json

playerPorts = []
playerNames = []
gameCounter = 0
games = {}
playersInfo = {}

def setupServer():
	global serverPort
	global serverSocket
	serverPort = 2600
	serverSocket = socket(AF_INET,SOCK_DGRAM)
	serverSocket.bind(('',serverPort))
	print("The manager is ready to receive...")

def receiveMsg():
	global serverPort
	global serverSocket
	if serverSocket:
		message,(clientIP,clientPort) = serverSocket.recvfrom(2048)
		message_decode = message.decode()
	return message_decode,clientIP,clientPort

def sendMsg(message,IP,Port):
	global serverPort
	global serverSocket
	if serverSocket:
		serverSocket.sendto(message.encode(),(IP,Port))

def clientCmd(message,clientIP,clientPort):
	global serverPort
	global serverSocket
	cmd_list = message.split( )
	action = cmd_list[0]

	if action == 'register':
		player_port = int(cmd_list[3]) #fourth argument in messgae received
		player_name = (cmd_list[1]) #name is second argument
		print('player port is: ',player_port)
		print(playerPorts)
		reply = ''
		count = 0
		if player_name not in playerNames and player_port not in playerPorts:
			playerNames.append(player_name)
			#count += 1
			#if player_port not in playerPorts:
			playerPorts.append(player_port)
			count += 1
		if count == 1:
			info = [clientIP,player_port]
			new_player = dict({player_name:info})
			playersInfo.update(new_player)
			reply = 'SUCCESSFUL'
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		else:
			reply = 'FAILURE'
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		#print('All player ports:',playerPorts)
		#print('All player names:',playerNames)
		print('All players info:',playersInfo)

	if action == 'query':
		if cmd_list[1] == 'games':
			reply = '0'
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		if cmd_list[1] == 'players':
			reply = json.dumps(playersInfo)
			serverSocket.sendto(reply.encode(),(clientIP,clientPort))

	if action == 'de-register':
		name = cmd_list[1]
		playersInfo.pop(name)
		reply = 'SUCCESSFUL'
		serverSocket.sendto(reply.encode(),(clientIP,clientPort))
		#print('All player ports:',playerPorts)
		#print('All player names:',playerNames)
		print('After de-register:',playersInfo)
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
