import socket 
from _thread import *
import constants
from threading import Event

server =  "192.168.18.2"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print("Mensagem de Erro: ", e)
    str(e)

s.listen()

print("Esperando conexões...")
games ={}
idCount = 0

def read_pos(str):
    #str = str.split(",")
    #return int(str[0]), int(str[0])
    x_str, y_str = str.split(',')
    x = int(x_str)
    y = int(y_str)
    return x, y

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])    

pos = [(200, 400), (205, 405)]

def thread_client(conn, player):
    global idCount

    """
    if overflowFlag:
        conn.send("Error: User Overflow")
        print(f"Conexão Perdida <{conn}>")
        conn.close()
        return
    """
    # A primeira mensagem será uma tupla com a posição inicial e o número do player (1 ou 2)
    firstMessage = f"{player}:{pos[player]}"

    print(firstMessage)

    ack = conn.send(str.encode(firstMessage))
    print("ack", ack)

    reply = (0,0)

    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            print("DATA: ", data)
            if idCount >= 2:
                pos[player] = data
                if player == 0:
                    reply = pos[0]
                else:
                    reply = pos[1]
                            
                print(f"Recebendo:", data)
                print(f"Enviando", reply)
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    print(f"Conexao Perdida com Player {player + 1}")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    
    idCount +=1
    p=0
    print("Conectado ao: ", addr)

    start_new_thread(thread_client, (conn, currentPlayer))
    #if(currentPlayer + 1 > 2):
    #    print("Limite de 2 jogadores ultrapassado. Espere alguem desconectar")
    #    start_new_thread(thread_client, (conn, currentPlayer, True))
    #else:
    #    start_new_thread(thread_client, (conn, currentPlayer, False))
    currentPlayer += 1
    #    print("Jogador Adicionado: ", currentPlayer)

