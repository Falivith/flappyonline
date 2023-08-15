import socket 
from _thread import *
import constants
import threading

server = constants.ip
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print("Mensagem de Erro: ", e)
    str(e)

s.listen(2)

print("Esperando conexao, Servidor Inciado")


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[0])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])    


pos = [(200, 400), (205, 805)]


def thread_client(conn, player, overflowFlag):

    if overflowFlag:
        conn.send("Error: User Overflow")
        print(f"Conexão Perdida <{conn}>")
        conn.close()
        return

    # A primeira mensagem será uma tupla com a posição inicial e o número do player (1 ou 2)

    firstMessage = f"{player}:{pos[player]}"

    conn.sendall(str.encode(firstMessage))

    reply = ""

    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            #reply = data.decode("utf-8")
            pos[player] = data
            
            if not data:
                print("Desconectado")
                break
            else:
                if player == 1:
                    reply = pos[0]
                    print(f"Recebendo de P0:", data)
                    print(f"Enviando para P0", reply)
                else:
                    reply = pos[1]
                    print(f"Recebendo de P1:", data)
                    print(f"Enviando para P1", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    print(f"Conexao Perdida com Player {player + 1}")
    conn.close()

    with currentPlayer_lock:
        global currentPlayer
        currentPlayer -= 1


currentPlayer = 0


currentPlayer_lock = threading.Lock()

while True:
    conn, addr = s.accept()
    print("Conectado ao: ", addr)

    if(currentPlayer + 1 > 2):
        print("Limite de 2 jogadores ultrapassado. Espere alguem desconectar")
        start_new_thread(thread_client, (conn, currentPlayer, True))
    else:
        start_new_thread(thread_client, (conn,currentPlayer, False))
        currentPlayer += 1
        print("Jogador Adicionado: ", currentPlayer)
