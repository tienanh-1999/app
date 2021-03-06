import Client
from getpass import getpass


class UI:
    def __init__(self, client):
        self.state = 0
        self.client = client

    def Run(self):
        while True:
            if self.state == 0:
                cmd = input("Register/Login??? ")
                if cmd == "register":
                    self.client.Connect()
                    username = input("Username: ")
                    password = getpass("Password: ")
                    if not self.client.Register(username, password):
                        self.client.close()
                    else:
                        self.state = 1
                elif cmd == "login":
                    self.client.Connect()
                    username = input("Username: ")
                    password = getpass("Password: ")
                    if not self.client.Login(username, password):
                        self.client.close()
                    else:
                        self.state = 1

            elif self.state == 1:
                cmd = input("Command: ")
                if cmd == "done":
                    self.client.close()
                    self.state = 2

                elif cmd == "add":
                    username = input("Input username: ")
                    if self.client.addFriend(username):
                        print("success")
                    else:
                        print("failed")

                elif cmd == "accept":
                    username = input("Input username: ")
                    if self.client.acceptFriendRequest(username):
                        print("success")
                    else:
                        print("failed")

                elif cmd == "reject":
                    username = input("Input username: ")
                    if self.client.rejectFriendRequest(username):
                        print("success")
                    else:
                        print("failed")

                elif cmd == "friend":
                    friend = self.client.showFriend()
                    print(friend)

                elif cmd == "request":
                    request = self.client.showFriendRequest()
                    print(request)

                elif cmd == "file":
                    file = input("Input file name: ")
                    if self.client.sendFile(file):
                        print("success")
                    else:
                        print("file does not exist")

                elif cmd == "shutdown":
                    self.client.shutdown()
                    return

            elif self.state == 2:
                break
