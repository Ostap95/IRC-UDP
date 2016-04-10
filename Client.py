import socket
import sys
import select
from GameLogic import *

MSG_REGISTER = "REG"
MSG_REG_OK_RESPONSE = "REG_OK"
MSG_REG_FAULT_RESPONSE = "REG_FAULT"

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005

MESSAGE_EXPECTED = ""


""" Prints the registration information based on the message received from the server """
def RegistrationInfo(msg):
    if msg == MSG_REG_OK_RESPONSE:
        print "Registado com sucesso"
    elif msg == MSG_REG_FAULT_RESPONSE:
        print "Registo falhou. O jogador ja esta registado no servidor"

""" MessageInterpreter interpretes the message received from the server"""
def MessageInterpreter(msg):
    if msg.find(MSG_REGISTER, len(message)): # Registration Message
        RegistrationInfo(msg)

""" Message to be sent to the server """
def sendMessage(socket, msg, server):
    socket.sendto(msg.encode(), server)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(2) # timeout set to 2 seconds
# Select will wait for the socket and console input
inputs = [client, sys.stdin]

board = GameLogic()
while True:
    ins, outs, exs = select.select(inputs,[],[])
    #select devolve para a lista ins quem esta a espera de ler
    start = 0
    for i in ins:
      # i == sys.stdin - alguem escreveu na consola, vamos ler e enviar
      if i == sys.stdin:
        # sys.stdin.readline() le da consola
        msg = sys.stdin.readline()
        # envia mensagem da consola para o servidor
        sendMessage(client, msg, (SERVER_IP,SERVER_PORT))
      # i == sock - o servidor enviou uma mensagem para o socket

      try:
        (msg,addr) = client.recvfrom(1024)
        message = msg.decode()
        MessageInterpreter(message)
      except socket.timeout:
        print "Servidor Indisponivel no momento"
