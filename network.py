
import socket 

server = "192.168.18.2" #ip do servidor
port = 5555

# -----------------Network----------------------#
class Network:
    def __init__(self,server,port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server,self.port)
        self.id = self.connect()
        self.connect()
        print(self.id)
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

n = Network(server, port)
print(n.send("Hello"))
print(n.send("World"))

# --------------- End Network-------------------#
