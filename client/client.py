# Assignment - 2
# Coffee Shop Application
# Eylul Begum Albayrak - 2385110
# Adam Mohammed I K - 2350775

# File that will run as the central python client

from tkinter import *
from tkinter import messagebox
from serverhandler import ServerHandler


class Login(Frame):
    def __init__(self, server):
        Frame.__init__(self)
        self.pack()
        self.master.title("Login")
        self.master.geometry("300x160")

        self.UsernameFrame = Frame(self)
        self.UsernameFrame.pack(padx=7, pady=7)

        self.UsernameLabel = Label(self.UsernameFrame, text="User Name", font=("Arial", 10))
        self.UsernameLabel.pack(side=LEFT, padx=5, pady=5)

        self.UsernameEntry = Entry(self.UsernameFrame)
        self.UsernameEntry.pack(side=LEFT, padx=5, pady=5)

        self.PasswordFrame = Frame(self)
        self.PasswordFrame.pack(padx=7, pady=7)

        self.PasswordLabel = Label(self.PasswordFrame, text="Password", font=("Arial", 10))
        self.PasswordLabel.pack(side=LEFT, padx=5, pady=5)

        self.PasswordEntry = Entry(self.PasswordFrame, show="*")
        self.PasswordEntry.pack(side=LEFT, padx=5, pady=5)

        self.ButtonFrame = Frame(self)
        self.ButtonFrame.pack(padx=7, pady=7)

        self.LoginButton = Button(self.ButtonFrame, text="Login", font=("Arial", 10),
                                  command=lambda: self.LoginButtonPressed(server))
        self.LoginButton.pack(side=BOTTOM, padx=5, pady=5)

    def LoginButtonPressed(self, server):
        username = self.UsernameEntry.get()
        password = self.PasswordEntry.get()

        if username == "":
            messagebox.showerror(title="Error", message="Please Enter Username Details!")
        elif password == "":
            messagebox.showerror(title="Error", message="Please Enter Password Details!")
        elif username == "" and password == "":
            messagebox.showerror(title="Error", message="Please Enter Username and Password Details!")
        else:
            role = server.login(username, password)
            if role == "barista\n":
                self.destroy()
                BaristaWindow = BaristaPanel(username, server)
                BaristaWindow.mainloop()
            elif role == "manager\n":
                self.destroy()
                ManagerWindow = ManagerPanel(server)
                ManagerWindow.mainloop()
            else:
                messagebox.showerror(title="Error", message="Employee Record Not Found!")


class BaristaPanel(Frame):
    def __init__(self, username, server):
        Frame.__init__(self)
        self.pack()
        self.master.title("Barista Panel")
        self.master.geometry("350x575")
        self.Barista = username

        self.CoffeeFrame = Frame(self)
        self.CoffeeFrame.pack(padx=7, pady=7)

        self.CoffeeLabel = Label(self.CoffeeFrame, text="COFFEES", font=("Arial", 12))
        self.CoffeeLabel.pack(side=TOP, padx=5, pady=5)

        self.coffeesmap = {"Latte": "latte",
                           "Cappuccino": "cappuccino",
                           "Americano": "americano",
                           "Espresso": "espresso"}

        self.Coffees = [["Latte", IntVar(), StringVar()], ["Cappuccino", IntVar(), StringVar()],
                        ["Americano", IntVar(), StringVar()], ["Espresso", IntVar(), StringVar()]]

        for coffee in self.Coffees:
            frame = Frame(self.CoffeeFrame)
            frame.pack(padx=7, pady=7, side=TOP)

            self.CoffeeSelection = Checkbutton(frame, text=coffee[0], variable=coffee[1])
            self.CoffeeSelection.pack(padx=7, pady=7, side=LEFT)

            self.CoffeeSelectionEntry = Entry(frame, textvariable=coffee[2])
            self.CoffeeSelectionEntry.config(state=DISABLED)
            self.CoffeeSelectionEntry.pack(padx=7, pady=7, side=RIGHT)

            self.CoffeeSelection.configure(
                command=lambda c=coffee[1], e=self.CoffeeSelectionEntry: self.EnableTextArea(c, e))
            if coffee[1].get():
                coffee[2].set(str(self.CoffeeSelectionEntry.get()))

        self.CakeFrame = Frame(self)
        self.CakeFrame.pack(padx=7, pady=7)

        self.CakeLabel = Label(self.CakeFrame, text="CAKES", font=("Arial", 12))
        self.CakeLabel.pack(side=TOP, padx=5, pady=5)

        self.cakesmap = {"San Sebastian Cheesecake": "sansebastian",
                         "Mosaic Cake": "mosaic",
                         "Carrot Cake": "carrot"}

        self.Cakes = [("San Sebastian Cheesecake", IntVar(), StringVar()), ("Mosaic Cake", IntVar(), StringVar()),
                      ("Carrot Cake", IntVar(), StringVar())]

        for cake in self.Cakes:
            frame = Frame(self.CakeFrame)
            frame.pack(padx=7, pady=7, side=TOP)

            self.CakeSelection = Checkbutton(frame, text=cake[0], variable=cake[1])
            self.CakeSelection.pack(padx=7, pady=7, side=LEFT)

            self.CakeSelectionEntry = Entry(frame, textvariable=cake[2])
            self.CakeSelectionEntry.config(state=DISABLED)
            self.CakeSelectionEntry.pack(padx=7, pady=7, side=RIGHT)

            self.CakeSelection.configure(command=lambda c=cake[1], e=self.CakeSelectionEntry: self.EnableTextArea(c, e))
            if cake[1].get():
                cake[2].set(str(self.CakeSelectionEntry.get()))

        self.DiscountFrame = Frame(self)
        self.DiscountFrame.pack(side=TOP, padx=5, pady=5)
        self.DiscountLabel = Label(self.DiscountFrame, text="Discount Code, if any")
        self.DiscountLabel.pack(side=LEFT, padx=5, pady=5)
        self.DiscountEntry = Entry(self.DiscountFrame)
        self.DiscountEntry.pack(padx=7, pady=7, side=RIGHT)

        self.ButtonsFrame = Frame(self)
        self.ButtonsFrame.pack(side=TOP, padx=5, pady=5)
        self.CreateButton = Button(self.ButtonsFrame, text="Create", command=self.CreateButtonPressed)
        self.CreateButton.pack(padx=7, pady=7, side=LEFT)
        self.CloseButton = Button(self.ButtonsFrame, text="Close", command=self.CloseButtonPressed)
        self.CloseButton.pack(padx=7, pady=7, side=RIGHT)

    def CreateButtonPressed(self):
        listcoffee = []

        for coffee in self.Coffees:
            if coffee[1].get():
                c = str(self.coffeesmap[coffee[0]])
                n = str(coffee[2].get())
                elem = c + '-' + n
                listcoffee.append(elem)

        listcake = []

        for cake in self.Cakes:
            if cake[1].get():
                c = str(self.cakesmap[cake[0]])
                n = str(cake[2].get())
                elem = c + '-' + n
                listcake.append(elem)

        discount = ""
        if self.DiscountEntry.get() == "":
            discount = "nodiscount"
        else:
            discount = self.DiscountEntry.get()

        listorder = []

        listorder.append(self.Barista)
        listorder.extend(listcoffee)
        listorder.extend(listcake)

        order = ";".join(listorder)
        print(order)
        server.order(order, discount)

    def CloseButtonPressed(self):
        self.quit()
        server.close_connection()

    def EnableTextArea(self, value, entry):
        if not value.get():
            entry.configure(state=DISABLED)
        else:
            entry.configure(state=NORMAL)


class ManagerPanel(Frame):
    def __init__(self, server):
        Frame.__init__(self)
        self.pack()
        self.master.title("Manager Panel")
        self.master.geometry("500x300")

        self.ReportFrame = Frame(self)
        self.ReportFrame.pack(padx=7, pady=7)

        self.ReportLabel = Label(self.ReportFrame, text="REPORTS", font=("Arial", 12))
        self.ReportLabel.pack(side=TOP, padx=5, pady=5)

        self.Reports = [("(1) What is the most popular overall?", IntVar()),
                        ("(2) Which barista has the highest number of orders?", IntVar()),
                        ("(3) What is the most popular product for the orders with the discount code?",
                         IntVar()),
                        ("(4) What is the most popular cake that is bought with espresso?", IntVar())]

        for report in self.Reports:
            frame = Frame(self.ReportFrame)
            frame.pack(padx=7, pady=7, side=TOP)
            self.ReportSelection = Checkbutton(frame, text=report[0], variable=report[1])
            self.ReportSelection.pack(padx=7, pady=7, side=LEFT)

        self.ButtonsFrame = Frame(self)
        self.ButtonsFrame.pack(side=TOP, padx=5, pady=5)
        self.CreateButton = Button(self.ButtonsFrame, text="Create", command=self.CreateButtonPressed)
        self.CreateButton.pack(padx=7, pady=7, side=LEFT)
        self.CloseButton = Button(self.ButtonsFrame, text="Close", command=self.CloseButtonPressed)
        self.CloseButton.pack(padx=7, pady=7, side=RIGHT)

    def CreateButtonPressed(self):
        if self.Reports[0][1].get():
            print(self.Reports[0][0], ": ", server.get_report(1))
        if self.Reports[1][1].get():
            print(self.Reports[1][0], ": ", server.get_report(2))
        if self.Reports[2][1].get():
            print(self.Reports[2][0], ": ", server.get_report(3))
        if self.Reports[3][1].get():
            print(self.Reports[3][0], ": ", server.get_report(4))

    def CloseButtonPressed(self):
        self.quit()
        server.close_connection()


def getServer():
    server = ServerHandler()
    result = server.connect()
    print("[CONNECTION] Result of connect call main:", result)
    return server, result


# this is where you run the program
if __name__ == '__main__':
    server, result = getServer()

    if result:
        LoginWindow = Login(server)
        LoginWindow.mainloop()
