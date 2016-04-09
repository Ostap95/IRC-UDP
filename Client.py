import socket
import sys
import select
from GameLogic import *
## client
MSG_REGISTER = "REGISTER"
MSG_OK_RESPONSE = "OK"

SERVER_IP = "localhost"
SERVER_PORT = 5005



client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Select will wait for the socket and console input
inputs = [sock, sys.stdin]

board = GameLogic()
while True:
    ins, outs, exs = select.select(inputs,[],[])
    #select devolve para a lista ins quem esta a espera de ler
    for i in ins:
      # i == sys.stdin - alguem escreveu na consola, vamos ler e enviar
      if i == sys.stdin:
        # sys.stdin.readline() le da consola
        msg = sys.stdin.readline()
        # envia mensagem da consola para o servidor
        client.sendto(msg.encode(),(SERVER_IP,SERVER_PORT))
      # i == sock - o servidor enviou uma mensagem para o socket
      elif i == sock:
        (msg,addr) = client.recvfrom(1024)
        message = msg.decode().split()
        if message[0] == MSG_REGISTER:
            if message[1] == MSG_OK_RESPONSE:
                print "Registado com sucesso"
            else:
                print "Registo falhou. O jogador ja esta registado no servidor"
