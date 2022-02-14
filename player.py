from http import client, server
from socket import *





def setupServer():
    global serverIP
    global serverPort
    global clientSocket
    serverIP = '10.120.70.106' 
    serverPort = 2600
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    #if clientSocket:
        #print('connected')

def printMenu():
    menu = "Enter one of the following commands: \n"
    menuItems = "register <user> <IPv4-address> <port> \nderegister <user> \nquery players \nquery games \n"
    return menu + menuItems

def commandClient():
    global serverIP
    global serverPort
    global clientSocket
    commandPrompt = printMenu()
    #commandChoice = input("Enter Command: ") #command to sent to sever
    commandChoice = input(commandPrompt) #command to sent to sever
    cmdChoice_list = commandChoice.split( ) #split into array
    action = cmdChoice_list[0] #gives the first word in command
    #print(action)
    if action == 'register':
        sendMsg(commandChoice,serverIP,serverPort)
        #clientSocket.sendto(commandChoice.encode(),(serverIP,serverPort))
        #reply = receiveMsg()
        reply,(serverIP,serverPort) = clientSocket.recvfrom(2040)
        reply_de = reply.decode()
        print(reply_de)
        if reply == 'SUCCESSFUL':
            return reply
        elif reply == 'FAILURE': 
            print('FAILURE')
            commandClient()
        elif reply == '':
            print('NO REPLY')
    
    if action == 'query':
        sendMsg(commandChoice,serverIP,serverPort)
        reply,(serverIP,serverPort) = clientSocket.recvfrom(2040)
        reply_de = reply.decode()
        print(reply_de)
    
    if action == 'de-register':
        sendMsg(commandChoice,serverIP,serverPort)
        reply,(serverIP,serverPort) = clientSocket.recvfrom(2040)
        reply_de = reply.decode()
        if reply_de == 'SUCCESSFUL':
            print(reply_de)
            return reply_de
            

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
    return message


setupServer() #set up

while True: 
    message = commandClient() #get input command
    if message == 'SUCCESSFUL':
        clientSocket.close()
        break;
    #print(message)
    