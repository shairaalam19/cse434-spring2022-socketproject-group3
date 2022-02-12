# from socket import *
# serverPort = 2600
# serverSocket = socket(AF_INET, SOCK_DGRAM)
# serverSocket.bind(('', serverPort))
# print("The server is ready to receive")
# while True:
#     message, clientAddress = serverSocket.recvfrom(2048)
#     modifiedMessage = message.decode().upper()
#     serverSocket.sendto(modifiedMessage.encode(), clientAddress)

# Players
# port = 2600
# IP = '10.120.70.106'
# location = [IP, port]
# name = 'Tao'
# player1 = dict({name: location})
# print(player1)

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

def register(name, IP, port ):
    print("Inside register()")
    location = [IP, port]
    player = dict({name: location})
    players.update(player) 
    print(player)
    print("\n")

def queryPlayers():
    print("Inside queryPlayers()")
    print(players)
    print("\n")

def startGame(dealer, user):
    print("Inside startGame()")
    print("\n")

def queryGames():
    print("Inside queryGames()")
    print(games)
    print("\n")

def end(id, user):
    print("Inside startGame()")
    print("\n")
 
def deregister(name):
    print("Inside deregister()")
    players.pop(name)
    print(players)
    print("\n")

def main():
    register("Tao", "10.120.70.106", 2600)
    register("Brenda", "10.120.70.106", 2600)
    queryPlayers()
    # queryGames()
    deregister("Tao")
    deregister("Brenda")

if __name__ == "__main__":
    main()

    