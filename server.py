import socket
import time
from config import make_pos, read_pos, ip
from threading import Event
from _thread import *

server =  ip
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print("Mensagem de Erro: ", e)
    str(e)

s.listen()

print("Esperando conexões...")
games = {}
idCount = 0

pos = [(200, 200), (200, 200)]

players_ready = [False, False]

def thread_client(conn, player):
    global players_ready
    global currentPlayer

    # A primeira mensagem será uma tupla com a posição inicial e o número do player (1 ou 2)
    firstMessage = f"{player}:{pos[player]}"

    print("Primeira Mensagem: ", firstMessage)

    conn.send(str.encode(firstMessage))

    reply = (0,0)

    data1 = ""
    while True:
        try:
            while data1 != "Ready":
                data1 = conn.recv(2048).decode()
                conn.send(b"Not")
                print(f"Não enviado para {player + 1}")

            players_ready[player] = True
            print(f"Player {player + 1} pronto.")

            while not all(players_ready):
                pass

            conn.send(b"Yes")
            print(f"Início do jogo.")

            conn.recv(2048).decode()
        except:
            break

        while True:
            try:
                data = read_pos(conn.recv(2048).decode())
                if data == (0,0):
                    players_ready = [False,False]
                    reply = data
                    data1 = ""
                    conn.sendall(str.encode(make_pos(reply)))
                    break
                else:
                    pos[player] = data
                    if player == 1:
                        reply = pos[0]
                    else:
                        reply = pos[1]
                                
                    print(f"Recebendo:", data)
                    print(f"Enviando", reply)
                conn.sendall(str.encode(make_pos(reply)))
            except:
                break
    currentPlayer -= 1
    conn.close()
    print(f"Conexao Perdida com Player {player + 1}")

currentPlayer = 0

while True:
    conn, addr = s.accept()
    
    print("Conectado ao: ", addr)

    start_new_thread(thread_client, (conn, currentPlayer))
    currentPlayer += 1
