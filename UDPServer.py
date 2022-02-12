from socket import *

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

def register(name, IP, port):
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
    # What is the unique identifier? 
    print("Inside deregister()")
    players.pop(name) 
    print(players)
    print("\n")

def main():
    # register("Tao", "100.100.100.100", 2600)
    # register("Brenda", "100.100.100.100", 2600)
    # queryPlayers()
    # deregister("Tao")
    # queryGames()
    # sets port 
    serverPort = 2600
    # creat esocket 
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("The manager (server) is ready to receive")
    while True:
        # gets message from a client 
        message, clientAddress = serverSocket.recvfrom(2048)
        # convert message from bytes to string and make uppercase 
        modifiedMessage = message.decode().upper()
        # sends message back to client 
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)

if __name__ == "__main__":
    main()


    
