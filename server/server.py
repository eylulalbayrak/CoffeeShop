# File that will run as the central python server

import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 5000

FILEPATH = "server/textfiles"

# Thread to handle a client
class ClientThread(threading.Thread):
    def __init__(self, client_socket: socket.socket, client_address, locks):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.locks = locks
        self.filepath = FILEPATH
        
        # in case file names change
        self.filenames = {"users": "users.txt", "orders": "orders.txt", "prices": "prices.txt", "discountcodes": "discountcodes.txt"}
        print("New connection from ", client_address)
        

    # main handler
    def run(self):
        self.client_socket.send("connectionsuccess".encode())
        while True:
            msg = self.client_socket.recv(1024).decode()
            command = msg.split(";")[0]
            if command == "login":
                if not self.login(msg):
                    self.client_socket.close()
                    return
            elif command == "order":
                self.log_order(msg)
            elif command == "report1":
                self.generate_report1()
            elif command == "report2":
                self.generate_report2()
            elif command == "report3":
                self.generate_report3()
            elif command == "report4":
                self.generate_report4()
            
        
    # handle logins 
    def login(self, message: str):
        username, password = message.split(";")[1:3]

        usersfile = os.path.join(self.filepath,self.filenames["users"])
        lines = []
        self.locks[self.filenames["users"]].acquire()
        with open(usersfile, "r") as f:
            lines = f.readlines()
        self.locks[self.filenames["users"]].release()
        
        for line in lines:
            line = line.split(";")
            if line[0] == username and line[1] == password:
                msg = ";".join(["loginsucess",username,line[2]]).encode()
                print("sucessful login from user ", username)
                self.client_socket.send(msg)
                return True
        
        self.client_socket.send("loginfailure".encode())
        print("failure to login as user ", username)
        return False
        
                
    # handle an order
    def log_order(self, message:str):

        message = message.split(";")
        discountcode, barista = message[1:3]

        prices = self.__read_prices()

        items = message[3:]
        total,discount = self.__calculate_total(items,prices,discountcode)

        ordersfile = os.path.join(self.filepath,self.filenames["orders"])
        self.locks[self.filenames["orders"]].acquire()
        with open(ordersfile,"a") as f:
            order = ";".join([str(total),str(discount),barista,]) + ';'
            order += ";".join(items)
            f.write(order)
        self.locks[self.filenames["orders"]].release()

        msg = ";".join(["orderconfirmation",str(total)]).encode()
        self.client_socket.send(msg)
        print(f"Order logged from barista {barista} with a total of {total}")

    # read item prices from file and return price dictionary
    def __read_prices(self):
        pricesfile = os.path.join(self.filepath,self.filenames["prices"])
        prices = {}
        lines = []
        self.locks[self.filenames["prices"]].acquire()
        with open(pricesfile,"r") as f:
            lines = f.readlines()
        self.locks[self.filenames["prices"]].release()

        for line in lines:
            line = line.strip('\n').split(";")
            prices[line[0]] = int(line[1])
        return prices

    # helper function to calculate the total of the given items
    def __calculate_total(self,items,prices, discountcode):
        items = [i.split("-") for i in items]
        items = [ [item, int(quantity)] for item, quantity in items]
                
        total = 0
        for item, quantity in items:
            total += quantity * (prices[item])

        discount = self.__process_discount(discountcode)

        total -= discount
        return total, discount

    # helper function to calculate discount and remove it from file
    def __process_discount(self, discountcode):
        if discountcode == "nodiscountcode":
            return 0

        discountfile = os.path.join(self.filepath,self.filenames["discountcodes"])
        lines = []
        self.locks[self.filenames["discountcodes"]].acquire()
        with open(discountfile,"r+") as f:
            lines = f.readlines() 
            f.seek(0)
            f.truncate()     
            for line in lines:
                splitline = line.split(";")
                if splitline[0] == discountcode:
                    discount = int(splitline[1].strip('\n'))
                else:
                    f.write(line)
        self.locks[self.filenames["discountcodes"]].release()
        return discount

    # helper function to read all lines of the order file
    def __read_orders(self):
        ordersfile = os.path.join(self.filepath,self.filenames["orders"])
        self.locks[self.filenames["orders"]].acquire()
        lines = []
        with open(ordersfile,"r") as f:
            lines = [i.strip('\n') for i in f.readlines()]
        self.locks[self.filenames["orders"]].release()
        return lines

    # function to report most selling item
    def generate_report1(self):
        counters = {}
        orders = self.__read_orders()

        for order in orders:
            order = order.split(';')[3:]
            for item in order:
                item = item.split('-')
                counters[item[0]] = counters.get(item[0],0) + int(item[1])

        maxorders = max(counters.values())
        maxitems = [item for item in counters if counters[item] == maxorders]
        msg = ["report1"]
        msg.extend(maxitems)
        msg = ";".join(msg).encode()
        self.client_socket.send(msg)
        print("report1 generated")

    # function to report highest ordering barista
    def generate_report2(self):
        counters = {}
        orders = self.__read_orders()

        for order in orders:
            barista = order.split(";")[2]
            counters[barista] = counters.get(barista,0) + 1

        maxorders = max(counters.values())
        maxbaristas = [barista for barista in counters if counters[barista] == maxorders]
        msg = ["report2"]
        msg.extend(maxbaristas)
        msg = ";".join(msg).encode()
        self.client_socket.send(msg)
        print("report2 generated")
    
    # function to report most ordered item on discount
    def generate_report3(self):
        counters = {}
        orders = self.__read_orders()

        for order in orders:
            order = order.split(';')
            if order[1] == "0":
                continue
            for item in order[3:]:
                item = item.split('-')
                counters[item[0]] = counters.get(item[0],0) + int(item[1])

        maxorders = max(counters.values())
        maxitems = [item for item in counters if counters[item] == maxorders]
        msg = ["report3"]
        msg.extend(maxitems)
        msg = ";".join(msg).encode()
        self.client_socket.send(msg)
        print("report3 generated")

    # function to report most popular cake bought with espresso
    def generate_report4(self):
        counters = {}
        orders = self.__read_orders()

        for order in orders:
            order = order.split(';')[3:]

            items = [item.split("-") for item in order]
            items = [item[0] for item in items]
            if "expresso" in items:
                continue

            for item in order:
                item = item.split('-')
                if item[0] in ["sansebastian","carrot","mosaic"]:
                    counters[item[0]] = counters.get(item[0],0) + int(item[1])

        maxorders = max(counters.values())
        maxitems = [item for item in counters if counters[item] == maxorders]
        msg = ["report4"]
        msg.extend(maxitems)
        msg = ";".join(msg).encode()
        self.client_socket.send(msg)
        print("report4 generated")
    


if __name__=="__main__":
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST,PORT))
    except socket.error:
        print("Could not bind")
        exit(1)
    
    print("Server started")
        

    files = os.listdir(FILEPATH)
    
    locks = {} # technically only need locks for writing operations
    for file in files:
        locks[file] = threading.RLock()

    while True:
        server.listen()
        clientSocket, clientAddress = server.accept()
        newThread = ClientThread(clientSocket, clientAddress, locks)
        newThread.start()
