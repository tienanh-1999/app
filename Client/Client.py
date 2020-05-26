import socket
HEADER_LENGTH = 10

HOST = "127.0.0.1"
PORT = 5050

class Client:
    def __init__(self):
        self.socket = None

    def Connect(self):
        #This method will connect client socket to server socket 
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        res = self.Receive_message()['data']
        if res == 'done':
            self.close_response()
            return False

        return True
        
    def Receive_message(self):
        #This method is used to receive message from server

        message_header = self.socket.recv(HEADER_LENGTH)

        if not len(message_header):
            self.close()
            return {'header': None,'data': None}

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': self.socket.recv(message_length).decode('utf-8')}

    def Send_message(self, message):
        #This method is used to send message to server
        #Arg: message: a string object

        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(message_header + message)        

    def Register(self, username, password):
        #Register services

        self.Send_message("Register")
        self.Send_message(username)
        self.Send_message(password)

        message_recv = self.Receive_message()
        if message_recv['data'] == "Successed":
            return True
        else:
            return False

    def Login(self, username, password):
        # Login 

        self.Send_message("Login")
        self.Send_message(username)
        self.Send_message(password)

        message_recv = self.Receive_message()
        if message_recv['data'] == "Successed":
            return True
        else:
            return False

    def showFriend(self):
        self.Send_message("showFriend")
        response = self.Receive_message()['data']
        if response == "Successed":
            length = self.socket.recv(HEADER_LENGTH)
            length = int(length.decode('utf-8').strip())
            friendDict = {}
            for _ in range(length):
                username = self.Receive_message()['data']
                status = self.Receive_message()['data']
                friendDict[username] = status
            return friendDict

        else:
            return None

    def showFriendRequest(self):
        self.Send_message("showFriendRequest")
        response = self.Receive_message()['data']
        if response == "Successed":
            length = self.socket.recv(HEADER_LENGTH)
            length = int(length.decode('utf-8').strip())
            requestList = []
            for _ in range(length):
                username = self.Receive_message()['data']
                #status = self.Receive_message()['data']
                requestList.append(username)
            return requestList

        else:
            return None
            
    def acceptFriendRequest(self, username2):
        self.Send_message("acceptFriendRequest")
        self.Send_message(username2)
        response = self.Receive_message()['data']
        if response == "Successed":
            return True
        else:
            return False
        
    def rejectFriendRequest(self, username2):
        self.Send_message("rejectFriendRequest")
        self.Send_message(username2)
        response = self.Receive_message()['data']
        if response == "Successed":
            return True
        else:
            return False

    def addFriend(self, username2):
        self.Send_message("addFriend")
        self.Send_message(username2)
        response = self.Receive_message()['data']
        if response == "Successed":
            return True
        else:
            return False

    def sendFile(self):
        self.Send_message("sendFile")
        with open("file_test/course.pdf", "rb") as f:
            data = f.read()
        numByte = len(data)
        print("num byte: ", numByte)
        len_pieces = []
        len_pieces += [1024]*int(numByte/1024)
        len_pieces.append(numByte - int(numByte/1024)*1024)
        print("pieces: ", len_pieces)
        self.Send_message(str(len(len_pieces)))  # send the number of pieces
        f = open("file_test/sem_183.png", "rb")
        for piece in len_pieces:
            piece_data = f.read(piece)
            self.socket.send(piece_data)
        f.close()
        print("closed")

    def shutdown(self):
        self.Send_message("shutdown")

    def close(self):
        self.Send_message('done')
        self.socket.close()

    def close_response(self):
        self.socket.close()

    def Run(self):
        self.Connect()
        while True:
            cmd = input("Command pls: ")
            self.Send_message(cmd)
            if cmd == 'done':
                self.socket.close()
                break
            self.Register()

