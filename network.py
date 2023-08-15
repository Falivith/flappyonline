import socket 

server = "192.168.18.2" #ip do servidor
port = 5555

# -----------------Network----------------------#
class Network:
    def __init__(self,server = "192.168.18.2" ,port = 5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server,self.port)
        self.pos = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
        
    def getPos(self):
        return self.pos
    
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

# --------------- End Network-------------------#
