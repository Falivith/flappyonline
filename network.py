import socket
import constants

server = "192.168.18.2"
port = 5555

# -----------------Network----------------------#


class Network:
    def __init__(self, server = "192.168.18.2", port = 5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.player, self.pos = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            response = self.client.recv(2048).decode()
            player_and_pos = response.split(":")
            return player_and_pos[0], constants.convert_string_in_tuple(player_and_pos[1])
        except:
            print("Erro na conexão com o servidor.")
            pass
        
    def getPos(self):
        return self.pos
    
    
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    #def ready(self, player):
    #    self.ready_flags[player] = True
    #    return all(self.ready_flags)  # Return True if both players are ready

# --------------- End Network-------------------#
