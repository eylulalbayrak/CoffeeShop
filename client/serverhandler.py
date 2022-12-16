import socket



class ServerHandler():
    def __init__(self) -> None:
        self.server= "127.0.0.1"
        self.port=5000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user = None
    
    # run this at start of program, must run before any other commands
    # returns true if connection succesful
    # returns false if connection fails 
    # NOTE: if this fails, inform user that server may not be running
    def connect(self) -> bool:
        try:
            self.socket.connect((self.server,self.port))
            self.socket.recv(1024) # just to flush the buffer
            return True
        except ConnectionRefusedError:
            return False

    # function to login
    # returns role if login succesful, None otherwise
    # NOTE: roles are "barista" or "manager"
    def login(self,username,password) -> bool:
        message = ";".join(["login",username,password]).encode()
        self.socket.send(message)
        response = self.socket.recv(1024).decode().split(";")
        if response[0] == "loginsuccess":
            self.user = response[1]
            return response[2]
        else:
            return None

    # function to log order of items
    # returns total price of order
    # NOTE: items are given in format ["item-quantity",...]. item must be named according to prices.txt
    # NOTE: pass discountcode as "nodiscountcode" for no discount code
    def order(self,items, discountcode):
        message = ["order",discountcode,self.user]
        message.extend(items)
        message = ";".join(message).encode()
        self.socket.send(message)
        response = self.socket.recv(1024).decode().split(";")
        return response[1]

    # function to request a report
    # returns list of items 
    # report_num must be in range 1 to 4
    def get_report(self, report_num):
        assert report_num in range(1,5), "Invalid report number requested"
        message = ("report"+str(report_num)).encode()
        self.socket.send(message)
        response = self.socket.recv(1024).decode().split(";")
        return response[1:]

    # function to close connection to server
    def close_connection(self):
        self.socket.close()


# this is just example / test code
if __name__ == "__main__":
    server = ServerHandler()
    print("result of connect call: ", server.connect())

    print("result of login call: ", server.login('dave','k343'))

    items = ["expresso-1","sansebastian-1"]
    discountcode="23c456"
    print('result of order call: ', server.order(items,discountcode))

    for num in range(1,6):
        try:
            print(f"result of report{num} call: ", server.get_report(num))
        except AssertionError:
            pass
    
    server.close_connection()