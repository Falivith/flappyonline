import socket 
from _thread import * 
import sys

server = "192.168.18.2"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Esperando conexao, Servidor Inciado")

def thread_client(conn):
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Desconectado")
                break
            else:
                print("Recebido: ", reply)
                print("Enviando: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break


while True:
    conn, addr = s.accept()
    print("Conectado ao: ", addr)

    start_new_thread(thread_client, (conn, ))

