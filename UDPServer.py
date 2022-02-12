from socket import *
import json

# dictionary of dictionaries (players is a dictionary containing a dictionary for every player)
players = {} 

# games is a dictionary with the following
# key: game counter 
# value: dictionary for every single game 
gameCounter = 1;
games = {}

# game dictionary
# key = gameCount (and then increment so next game can have that identifier)
# value: list of players with players[0] = dealer

# sets port 
serverPort = 2600
# creat esocket 
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

def setupServer():
    global serverPort
    global serverSocket

    # sets port 
    serverPort = 2600
    # creat esocket 
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("The manager (server) is ready to receive")


def receiveMessage():
    global serverPort
    global serverSocket
    message = ""
    clientIP = ""
    clientPort = ""

    if serverSocket:
        message, (clientIP, clientPort) = serverSocket.recvfrom(2048)
        message = message.decode()
    else: 
        print("serverSocket is empty")

    return message, (clientIP, clientPort)

def sendMessage(message, IP, Port): 
    global serverPort
    global serverSocket
    if serverSocket:
            serverSocket.sendto(message.encode(), (IP, Port))
    else: 
        print("serverSocket is empty")

def register(name, IP, port):
    global players

    print("Inside register()")
    location = [IP, port]
    player = dict({name: location})
    players.update(player) 
    print(player)
    print("\n")
    return player

def deregister(name):
    global players

    print("Inside deregister()")
    players.pop(name) 
    print(players)
    print("\n")
    return players

def queryPlayers():
    global players 
    print("Inside queryPlayers()")
    print(players)
    print("\n")
    return json.dumps(players)

def startGame(dealer, user):
    global games
    print("Inside startGame()")
    print("\n")

def queryGames():
    global games
    print("Inside queryGames()")
    print(games)
    print("\n")
    return json.dumps(games)

def endGame(id, user):
    global games
    print("Inside endGame()")
    print("\n")

def menu(choice, clientIP, clientPort):
    global serverPort
    global serverSocket
    global players
    global games
    # print("Menu Choice from client: ")
    # print(choice)
    if choice == "1" : 
        message = "\nEnter Name to Register: "
        sendMessage(message, clientIP, clientPort)

        name, (clientIP, clientPort) = receiveMessage()
        register(name, clientIP, clientPort)
        # sendMessage(queryPlayers(), clientIP, clientPort)

    if choice == "2":
        message = "\nEnter Name to De-register: "
        sendMessage(message, clientIP, clientPort)

        name, (clientIP, clientPort) = receiveMessage()
        deregister(name)
        # sendMessage(queryPlayers(), clientIP, clientPort)

    if choice == "3": 
        sendMessage(queryPlayers(), clientIP, clientPort)

    if choice == "4":
        sendMessage(queryGames(), clientIP, clientPort)

def main():    
    # setupServer()

    print("The manager (server) is ready to receive")

    while True:
        # message, (clientIP, clientPort) = serverSocket.recvfrom(2048)
        message, (clientIP, clientPort) = receiveMessage()
        # print(message)
        menu(message, clientIP, clientPort)

if __name__ == "__main__":
    main()


    
