# File that will run as the central python server

import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

class ClientThread(threading.Thread):
    def __init__(self, client_socket, client_address):
        super().__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        print("New connection from ", client_address)

    def run(self):
        pass


if __name__=="__main__":
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST,PORT))
    print("Server started")

    while True:
        server.listen()
        clientSocket, clientAddress = server.accept()
        newThread = ClientThread(clientSocket, clientAddress)
        newThread.start()
