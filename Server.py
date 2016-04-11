import socket

CMD_REGISTER = "REG"
MSG_REGISTER_OK = "REG_OK"
MSG_REGISTER_FAULT = "REG_FAULT"
CMD_LIST = "LIST"
MSG_LIST_RETURN = "LIST_RETURN"
CMD_PLAY = "PLAY"
MSG_INVITE = "ACCEPT"
MSG_RECEIVED = "ACK"
MSG_INVITE_RESPOSNE = "INVITE"


SERVER_PORT = 5005
SERVER_HOST = "127.0.0.1"

addrs = {} # dict: nome -> endereco. Ex: addrs["user"]=('127.0.0.1',17234)
clients = {} # dict: endereco -> [nome,msgID,lastReturn] Ex: clients[('127.0.0.1',17234)]=["user",msgID, lastReturn,"estado", "invite"]
# msgID representa o id da mensagem que tem de receber a seguir
# lastReturn representa o ultimo valor de retorno enviado para este cliente
# estes argumentos sao mais mais facil de utilizar na lista de clients porque e' mais facil indexar por endereco
games = {} # dict: client1->client2 ex: games["Daniel"] = ["Ostap"]
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_HOST, SERVER_PORT))

""" Registers the Player in client dictionary """
def addToClients(addr, name):
    clients[addr] = [name, 0, 0, "livre", " "]

""" Registers the player """
def registerPlayer(name, addr):
    if not name in addrs and not addr in clients:
      addrs[name] = addr
      addToClients(addr, name)
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

""" returns name for a given player in a match
    if no player found returns error
    boolean delet defaults to false and is used to remove an ingoing game from list if true"""
def matchNameLookup (name,delet=False):
    retName=""
    for i in games:
        if i == name:
            if delet == True:
                del games[name] ## this should delete name from dictionary
            retName = games[i];
            break;
        elif games[i] == name:
            if delet == True:
                del games[name] ## this should delete name from dictionary
            retName = i;
            break;
    return retName; # retorna "" se n encontra nome


""" args-> address of latest incoming message
returns addrs for destination client of a given ongoing game"""
def matchAddrLookup (addr):
    name=clients[addr][0]
    lookupName = matchNameLookup(name)
    if (lookupName==""):
        return ""
    for i in addrs:
        if i == lookupName:
            return addrs[i];


""" addr is address, msgID is sync number
esta funcao serve para sincronizacao das mensagens"""
def checkMsgID(addr,msgID,ret):
    #so' deve de ser < ou >  por 1 TODO check
    if(clients[addr][1] > msgID): # se for maior e' necessario cliente reenviar
        SEND ( "NACK", clients[addr][1],addr) ## sends NACK with msgID

    elif(clients[addr][1] < msgID): # se for menor e' necessario servidor reenviar
        SEND ( clients[addr][2],addr) ## resends last message

    msgID = clients[addr][1] #resets msgID


def setLastReturn(addr, returnVal):
    clients[addr][2] = returnVal;

def getLastReturn(addr):
    return clients[addr][2];

def incrementMessageID(addr):
    clients[addr][2] +=1;

""" Lists player names and their state """
def listNames():
    buff=""; #tamanho de recvfrom 1024, ver consequencias em clients
    for key in clients:
        buff += clients[key][0] + ":" + clients[key][3] + " "; # dividir por um espaco para poder fazer split em clnt
    return buff;

""" Invites second player """
def invitePlayer(mainPlayerAddress, playerToInvite):
    mainPlayerName = clients[mainPlayerAddress][0]
    playerToInviteAdress = addrs[playerToInvite]
    clients[playerToInviteAdress][4] = mainPlayerName
    Send(MSG_RECEIVED, mainPlayerAddress)
    Send(MSG_INVITE + " " + mainPlayerName, playerToInviteAdress);

"""" Responds to invite from a player """
def respondToInvite(player, response):
    playerToResponde = clients[player][4]
    addressToResponde = addrs[playerToResponde]
    Send(MSG_RECEIVED, player)
    Send(MSG_INVITE_RESPOSNE + " " + response, addressToResponde)

""" Main Loop """
while True:
    (msg, addr) = server.recvfrom(1024) # Buffer size
    cmd = msg.decode().split()
    if cmd[0] == CMD_REGISTER:
        registerPlayer(cmd[1], addr)

    elif cmd[0] == CMD_LIST:
        pList = listNames()
        Send(MSG_LIST_RETURN + " " + pList, addr)

    elif cmd[0] == CMD_PLAY:
        invitePlayer(addr, cmd[1])

    elif cmd[0] == MSG_INVITE_RESPOSNE:
        respondToInvite(addr, cmd[1])

    elif cmd[0] == "EXIT":
        server.close()
