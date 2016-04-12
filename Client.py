import socket
import sys
import select
import signal
import time
from GameLogic import *

MSG_REGISTER = "REG"
MSG_REG_OK_RESPONSE = "REG_OK"
MSG_REG_FAULT_RESPONSE = "REG_FAULT"
MSG_LIST = "LIST"
MSG_LIST_RESPONSE = "LIST_RETURN"
MSG_INVITE = "ACCEPT"
MSG_RECEIVED = "ACK"
MSG_ACCEPT_INVITE = "OK"
MSG_REJECT_INVITE = "NO"
MSG_INVITE_RESPONSE = "INVITE"
MSG_CHOICE = "CHOICE"


SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFF_SIZE = 1024 # Buffer size

LAST_MSG = [""] # Last message sent by the client to the server

global tries # Number of times that the client tried to resent the message
global board

""" Functions that is responsible for timeout situations """
def timeOutHandler(s, f):
    global tries # Number of times that the client tried to resent the message
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

""" Prints the Player list received from the server """
def printPlayerList(msg):
    msg = msg.split()
    print "------- Online Players -------"
    for i in range(1,len(msg)):
        print msg[i]
    print "------------------------------"

def acceptInvite(msg):
    msg = msg.split()
    name = msg[1]
    print name + " Convidou-o para jogar. Aceitar? "

def inviteResponse(msg):
    msg = msg.split()
    if msg[1] == MSG_ACCEPT_INVITE:
        print "Jogo Aceite"
        board.currentBoard()
    elif msg[1] == MSG_REJECT_INVITE:
        print "Jogo recusado"

""" See if the previous sent message corresponds to start a game or choice play """
def  checkGame(msg):
    if (MSG_INVITE_RESPONSE + " " + MSG_ACCEPT_INVITE in LAST_MSG[0] and MSG_RECEIVED in msg):
        board.currentBoard()
    elif MSG_CHOICE in msg:
        playChoiceGame(msg) # Starts the game as player 2

""" Checks if the client have sended choice message """
def checkChoice(msg):
    if MSG_CHOICE in msg:
        playChoiceGame(msg)

def receiveChoiceGame(msg):
    message = msg.split()
    play = int(message[1])
    board.play( (play-1)/3  , (play-1) % 3, 2)
    board.currentBoard()


def playChoiceGame(msg):
    message = msg.split()
    play = int(message[1])
    board.play( (play-1)/3  , (play-1) % 3, 1)
    board.currentBoard()

""" MessageInterpreter interpretes the message received from the server"""
def MessageInterpreter(msg):
    if MSG_REGISTER in msg: # Registration Message
        RegistrationInfo(msg)
    if MSG_LIST_RESPONSE in msg:
        printPlayerList(msg) # List Message
    if MSG_INVITE in msg:
        acceptInvite(msg)
    if MSG_INVITE_RESPONSE in msg:
        inviteResponse(msg)
    if MSG_CHOICE in msg:
        msg = msg.split()
        print "Choice: " + msg[1]

""" Message to be sent to the server """
def sendMessage(socket, msg, server):
    LAST_MSG[0] = msg
    socket.sendto(msg.encode(), server)
    signal.alarm(3) # Sets the alarm for 3 seconds, meaning that the client waits for 3 seconds for the server response.
    # If the server haven't given any response whithin 3 seconds, then the client tries more 2 times to resent the message
    # After it, client displays a message saying that the server is offline
    checkChoice(msg) # Checks if the player sended the choice message
""" ----------------------------------------------------------"""
signal.signal(signal.SIGALRM, timeOutHandler) # Timeout signal handler
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket used to communicate with the server
# Select will wait for the socket and console input
inputs = [client, sys.stdin]
board = GameLogic() # Game Board
""" ----------------------------------------------------------"""

""" --------------------- Main Loop --------------------------"""
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
            tries = 0 # Resets the timeout tries
            # i == client - o servidor enviou uma mensagem para o socket
        if i == client:
            (msg,addr) = client.recvfrom(BUFF_SIZE)
            signal.alarm(0) # Resets the timeout, since the message was received
            message = msg.decode()
            checkGame(message)
            MessageInterpreter(message)
""" ----------------------------------------------------------"""
