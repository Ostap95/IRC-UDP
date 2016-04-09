import socket

CMD_REGISTER = "REGISTER"
MSG_REGISTER_OK = "REGISTER OK"
MSG_REGISTER_FAULT = "REGISTER FAULT"
MSG_SEND = "SEND"



SERVER_PORT = 5005
SERVER_HOST = "localhost"

# TIMEOUT sera' implementado no client
USER_DATA = []
# ex. como as mensagens sao sequenciais msgNumber deve bater certo com msgID enviada pelo cliente
addrs   = {} # dict: nome -> endereco. Ex: addrs["user"]=('127.0.0.1',17234)
clients = {} # dict: endereco -> [nome,msgID,lastReturn] Ex: clients[('127.0.0.1',17234)]=["user", msgID, lastReturn]
# msgID representa o id da mensagem que tem de receber a seguir
# lastReturn representa o ultimo valor de retorno enviado para este cliente
# estes argumentos sao mais mais facil de utilizar na lista de clients porque e' mais facil indexar por endereco
games = []# dict : client1 -> client2 ex. games["Daniel"] = ["Ostap"]
#

#INIT
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_HOST, SERVER_PORT))

def addToClients(addr,nome ):
    # add in register player
    clients[addr] = [nome,0,0]

def registerPlayer(name, addr):
    if not name in addrs and not addr in clients:
      addrs[name] = addr
      addToClients(addr,name)
      SEND("REG_OK",MSG_REGISTER_OK,addr)
      return
    else:
      SEND("REG_FAULT",MSG_REGISTER_FAULT,addr)
      return
"""
def responseToRegister(response, addr):
    ## retirar esta mensagem e' inutil SEND e' melhor
    if response:
        server.sendto(MSG_REGISTER_OK.encode(), addr)
    else:
        server.sendto(MSG_REGISTER_FAULT.encode(), addr)
"""

def SEND(msgPrefix, msg="", addr):
    # check if param msg can stay in the middle of other params
    # msg defaults to none in case we want to send the prefix only
    # prefix example: SEND with no params
    # can be used to redirect messages
    MSG = msgPrefix + " " + msg
    server.sendto(MSG.encode(), addr)
    return MSG

def matchNameLookup (name,delet=False):
    """ returns name for a given player in a match
    if no player found returns error
    boolean delet defaults to false and is used to remove an ingoing game from list if true"""
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

def matchAddrLookup (addr):
    """ args-> address of latest incoming message
    returns addrs for destination client of a given ongoing game"""
    nome=clients[addr][0]
    lookupName = matchNameLookup(nome)
    if (lookupName==""):
        return ""
    for i in addrs:
        if i == lookupName:
            return addrs[i];

def checkMsgID(addr,msgID,ret):
    """ addr is address, msgID is sync number
    esta funcao serve para sincronizacao das mensagens"""
    #so' deve de ser < ou >  por 1 TODO check
    if(clients[addr][1] > msgID) # se for maior e' necessario cliente reenviar
        SEND ( "NACK", clients[addr][1],addr) ## sends NACK with msgID

    elif(clients[addr][1] < msgID) # se for menor e' necessario servidor reenviar
        SEND ( clients[addr][2],addr) ## resends last message

    msgID = clients[addr][1] #resets msgID

def setLastReturn(addr, returnVal):
    clients[addr][2] = returnVal;

def getLastReturn(addr):
    return clients[addr][2];

def incrementMessageID(addr):
    clients[addr][2] +=1;

def play(addr, DestName):
     """ """

def listNames():
    buff=""; #tamanho de recvfrom 1024, ver consequencias em clients
    for i in addrs:
        buff += i + " "; # dividir por um espaco para poder fazer split em clnt
    return buff;


##### MAIN #####
while True:
    #TODO dbug after completing client search for TODO's
    # cmd[1] vai ser msgID-> id especifico da mensagem para sincronizacao
    # logo, a mensagem em si começa  a partir do cmd[2]
    msg, addr = server.recvfrom(1024) # Buffer size - recvfrom returns tuple
    cmd = msg.decode().split() ##cmd = tuple
    checkMsgID(addr, cmd[1]) # client should resend all messages from this id onward
    # checkMsgID sends NACK

    if cmd[0] == "ACK":
        # msg_counter para um dado elemento na lista e' incrementado
        # n existe codigo em ACK, pois e' igual para todas as mensagens (checkMsgID)
    elif cmd[0] == "REGISTER":
        ret = registerPlayer(cmd[2], addr) # funcao ja tem REG_OK
    elif cmd[0] == "LIST":
        buf=listNames()
        ret=SEND("LIST_RETURN",buf,addr)
    elif cmd[0] == "PLAY":
        destCliAddr = addrs[cmd[2]]
        ret = SEND("ACCEPT", cmd[2], destCliAddr)
        games[cmd[2]] = clients[addr][0] ## adds new item to game dict with {"passiveGamer":"gameRequester" } - passive gamer receives gameRequest
    elif cmd[0] == "CHOICE":
        #redirects message
        addrCliDest=matchAddrLookup(addr)
        ret=SEND("CHOICE",cmd[2],addrCliDest)
    ## OK and NOW must send their
    elif cmd[0] == "OK":
        addrCliDest = addrs[cmd[2]]
        ret = SEND("OK", addrCliDest)
    elif cmd[0] == "NO":
        addrCliDest = addrs[cmd[2]]
        del games[addr[0]] ## delets from games list added in PLAY
        ret = SEND("NO", addrCliDest)
    elif cmd[0] == "WINNER":
        #redirects message
        addrPlayer2 = matchAddrLookup(addr)
        ret = SEND("WIN", cmd[2],addrPlayer2)
    elif cmd[0] == "ERROR":
        # TODO what to do with this error message
        print "error in " + addr
    elif cmd[0] == "EXIT":
        addrCliDest = matchAddrLookup(addr)
        ret = SEND("ACK",addrCliDest)
        del games[clients[addr][0]] # delets game
    else:
        ret = SEND("ERROR", "wrong input", addr) # resends message for wrong input

    setLastReturn(addr, ret)
    incrementMsgID(addr)
