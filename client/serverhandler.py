import socket


class ServerHandler():
    def __init__(self) -> None:
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user = None

    # run this at start of program, must run before any other commands
    # returns true if connection successful
    # returns false if connection fails 
    # NOTE: if this fails, inform user that server may not be running
    def connect(self) -> bool:
        try:
            self.socket.connect((self.server, self.port))
            self.socket.recv(1024)  # just to flush the buffer
            return True
        except ConnectionRefusedError:
            return False

    # function to log in
    # returns role if login successful, None otherwise
    # NOTE: roles are "barista" or "manager"
    def login(self, username, password) -> str:
        message = ";".join(["login", username, password]).encode()
        self.socket.send(message)
        response = self.socket.recv(1024).decode().split(";")
        if response[0] == "loginsuccess":
            self.user = response[1]
            return response[2]
        else:
            return ""

    # function to log order of items
    # returns total price of order
    # NOTE: items are given in format ["item-quantity",...]. item must be named according to prices.txt
    # NOTE: pass discountcode as "nodiscountcode" for no discount code
    def order(self, items, discountcode):
        message = ["order", discountcode, self.user]
        message.extend(items)
        message = ";".join(message).encode()
        self.socket.send(message)
        response = self.socket.recv(1024).decode().split(";")
        return response[1]

    # function to request a report
    # returns list of items 
    # report_num must be in range 1 to 4
    def get_report(self, report_num):
        assert report_num in range(1, 5), "Invalid report number requested"
        message = ("report" + str(report_num)).encode()
        self.socket.send(message)
        response = self.socket.recv(1024).decode().split(";")
        return response[1:]

    # function to close connection to server
    def close_connection(self):
        self.socket.close()
