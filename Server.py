import socket

CMD_REGISTER = "REG"
MSG_REGISTER_OK = "REG_OK"
MSG_REGISTER_FAULT = "REG_FAULT"
MSG_NOT_LOGGED = "NOTLOGGED"
CMD_LIST = "LIST"
MSG_LIST_RETURN = "LIST_RETURN"
CMD_PLAY = "PLAY"
MSG_INVITE = "ACCEPT"
MSG_RECEIVED = "ACK"
MSG_INVITE_RESPOSNE = "INVITE"
MSG_ACCEPT_INVITE = "OK"
MSG_REJECT_INVITE = "NO"
MSG_CHOICE = "CHOICE"
MSG_UNRECOGNIZED = "UNRECOGNIZED"
MSG_WINNER = "WINNER"
MSG_TIE = "TIE"
MSG_CHOICE_RECEIVED = "RECEIVED"
MSG_RESET_GAME = "RESET_GAME"

SERVER_PORT = 5005
SERVER_HOST = "127.0.0.1"

addrs = {} # dict: nome -> endereco. Ex: addrs["user"]=('127.0.0.1',17234)
clients = {} # dict: endereco -> [nome,msgID,lastReturn] Ex: clients[('127.0.0.1',17234)]=["user","estado", "player who invited to play"]
# msgID representa o id da mensagem que tem de receber a seguir
# lastReturn representa o ultimo valor de retorno enviado para este cliente
# estes argumentos sao mais mais facil de utilizar na lista de clients porque e' mais facil indexar por endereco
games = {} # dict: client1->client2 ex: games["Daniel"] = ["Ostap"]
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_HOST, SERVER_PORT))

""" Registers the player """
def registerPlayer(name, addr):
    if not name in addrs and not addr in clients:
      addrs[name] = addr
      clients[addr] = [name, "livre", ""]
      Send(MSG_REGISTER_OK, addr) # Sends REG_OK to the client
      return
    else:
      Send(MSG_REGISTER_FAULT, addr) # sends REG_FAULT to the client
      return

""" Sends a particular message to the specific address
 msg: Message | info: additional information to the Message | addr: Adrress to send """
def Send(msg, addr, info = ""):
    MSG = msg + info
    server.sendto(MSG.encode(), addr)
    return


""" args-> address of latest incoming message
returns addrs for destination client of a given ongoing game"""
def matchAddrLookup (addr):
    name=clients[addr][0] # Name of the client
    opponentName = clients[addr][2]
    return addrs[opponentName]


""" Lists player names and their state """
def listNames():
    buff=""; #tamanho de recvfrom 1024, ver consequencias em clients
    for key in clients:
        buff += clients[key][0] + ":" + clients[key][1] + " "; # dividir por um espaco para poder fazer split em clnt
    return buff;

def deleteGame(playerName):
    for i in games.keys():
        if i == playerName or games[i] == playerName:
            del games[i]

""" Invites second player """
def invitePlayer(mainPlayerAddress, playerToInvite):
    mainPlayerName = clients[mainPlayerAddress][0]
    playerToInviteAdress = addrs[playerToInvite]
    if clients[playerToInviteAdress][1] == "livre" and clients[mainPlayerAddress][1] == "livre":
        clients[playerToInviteAdress][2] = mainPlayerName
        Send(MSG_RECEIVED, mainPlayerAddress)
        Send(MSG_INVITE + " " + mainPlayerName, playerToInviteAdress);
    else:
        Send(MSG_INVITE + " " + MSG_REJECT_INVITE, mainPlayerAddress)


"""" Responds to invite from a player """
def respondToInvite(playerAddr, response):
    playerToRespond = clients[playerAddr][2] #
    addressToRespond = addrs[playerToRespond]
    if response == MSG_ACCEPT_INVITE: # If the player accepts the invite
        clients[playerAddr][1] = "ocupado" # change player state
        clients[addressToRespond][1] = "ocupado" # change player state
        games[playerToRespond] = clients[playerAddr][0] # Fills the game dictionary
        clients[addressToRespond][2] = clients[playerAddr][0]
    Send(MSG_RECEIVED, playerAddr)
    Send(MSG_INVITE_RESPOSNE + " " + response, addressToRespond)

def forwardChoice(playerAddr, choice):
    opponentAddr = matchAddrLookup(playerAddr)
    #Send(MSG_RECEIVED, playerAddr)
    Send(MSG_CHOICE + " " + choice, opponentAddr)

def choiceReceived(addr):
    Send(MSG_RECEIVED, addr)
    opponentAddr = matchAddrLookup(addr)
    Send(MSG_RECEIVED, opponentAddr)

def winnerAnnounce(addr):
    name = clients[addr][0]
    opponentAddr = matchAddrLookup(addr)
    clients[addr][1] = "livre"
    clients[opponentAddr][1] = "livre"
    deleteGame(name)
    Send(MSG_RECEIVED, addr)
    Send(MSG_WINNER, opponentAddr)

def gameTie(addr):
    name = clients[addr][0]
    opponentAddr = matchAddrLookup(addr)
    clients[addr][1] = "livre"
    clients[opponentAddr][1] = "livre"
    deleteGame(name)
    Send(MSG_RECEIVED, addr)
    Send(MSG_TIE, opponentAddr)

def resetGame(addr):
    name = clients[addr][0]
    opponentAddr = matchAddrLookup(addr)
    clients[addr][1] = "livre"
    clients[opponentAddr][1] = "livre"
    Send(MSG_RECEIVED, addr)
    deleteGame(name)

""" Main Loop """
while True:
    (msg, addr) = server.recvfrom(1024) # Buffer size
    cmd = msg.decode().split()
    if cmd[0] == CMD_REGISTER:
        registerPlayer(cmd[1], addr)
        continue # Skips for not entering the second if condition and go to the last else statement

    if addr in clients:
        if cmd[0] == CMD_LIST:
            pList = listNames()
            Send(MSG_LIST_RETURN + " " + pList, addr)
        elif cmd[0] == CMD_PLAY:
            invitePlayer(addr, cmd[1])
        elif cmd[0] == MSG_INVITE_RESPOSNE:
            respondToInvite(addr, cmd[1])
        elif cmd[0] == MSG_CHOICE:
            forwardChoice(addr, cmd[1])
        elif cmd[0] == MSG_WINNER:
            winnerAnnounce(addr)
        elif cmd[0] == MSG_TIE:
            gameTie(addr)
        elif cmd[0] == MSG_CHOICE_RECEIVED:
            choiceReceived(addr)
        elif cmd[0] == MSG_RESET_GAME:
            resetGame(addr)
        else:
            Send(MSG_UNRECOGNIZED, addr)
    else:
        Send(MSG_NOT_LOGGED, addr)
