# import socket programming library
import socket
from socket import * 
# import thread module
from _thread import *
import threading
 
print_lock = threading.Lock()
 
# thread function
def threaded(c):
    while True:
        # RECEIVE MESSAGE FROM CLIENT 
        # data received from client
        data = c.recv(2048)
        message = data.decode()

        # checks if there is data that was sent from the client 
        if not data:
            print('Bye')
             
            # lock released on exit
            print_lock.release()
            break
        else: 
            print(message)
 
        # SEND MESSAGE TO CLIENT 
        # confirmation message to client 
        message = "Server successfully received this message: " + message

        # send message back to client 
        c.send(message.encode())
 
    # connection closed
    c.close()
 
 
def main():
    serverIP = ""
 
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    serverPort = 2700
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind((serverIP, serverPort))
    print("Socket binded to port", serverPort)
 

    # put the socket into listening mode
    serverSocket.listen(5)
    print("Socket is listening")
    # a forever loop until client wants to exit
    while True:
        
        # establish connection with client
        c, addr = serverSocket.accept()
 
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))

    s.close()
 
 
if __name__ == '__main__':
    main()