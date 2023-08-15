import socket 
from _thread import * 
import sys

server = "192.168.18.2" #ip do servidor
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Esperando conexao, Servidor Inciado")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[0])
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])    

pos = [(200,400),(205,805)]
def thread_client(conn,player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""

    #mantem loop para receber conexoes
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            #reply = data.decode("utf-8")
            pos[player] = data
            
            if not data:
                print("Desconectado")
                break
            else:
                if player==1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Recebido: ", data)
                print("Enviando: ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    print("Conexao Perdida")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Conectado ao: ", addr)

    start_new_thread(thread_client, (conn,currentPlayer))
    currentPlayer += 1

