import socket
import sys
import select
import signal
import time
from GameLogic import *

MSG_REGISTER = "REG"
MSG_REG_OK_RESPONSE = "REG_OK"
MSG_REG_FAULT_RESPONSE = "REG_FAULT"

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFF_SIZE = 1024 # Buffer size

LAST_MSG = ["",]

global tries

""" Functions that is responsible for timeout situations """
def timeOutHandler(s, f):
    global tries
    if tries < 2:
        sendMessage(client, LAST_MSG[0], (SERVER_IP,SERVER_PORT))
        tries += 1
    else:
        print "Servidor Offline"

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
    LAST_MSG[0] = msg
    socket.sendto(msg.encode(), server)
    signal.alarm(3) # Sets the alarm for 3 seconds, meaning that the client waits for 3 seconds for the server response.
    # If the server haven't given any response whithin 3 seconds, then the client tries more 2 times to resent the message
    # After it, client displays a message saying that the server is offline

signal.signal(signal.SIGALRM, timeOutHandler) # Timeout signal handler
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket used to communicate with the server
# Select will wait for the socket and console input
inputs = [client, sys.stdin]
board = GameLogic()
while True:
    ins, outs, exs = select.select(inputs,[],[],0)
    #select devolve para a lista ins quem esta a espera de ler
    for i in ins:
        # i == sys.stdin - alguem escreveu na consola, vamos ler e enviar
        if i == sys.stdin:
            # sys.stdin.readline() le da consola
            msg = sys.stdin.readline()
            # envia mensagem da consola para o servidor
            sendMessage(client, msg, (SERVER_IP,SERVER_PORT))
            tries = 0
            # i == client - o servidor enviou uma mensagem para o socket
        if i == client:
            (msg,addr) = client.recvfrom(BUFF_SIZE)
            signal.alarm(0) # Resets the timeout, since the message was received
            message = msg.decode()
            MessageInterpreter(message)
