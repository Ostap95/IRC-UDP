import socket

CMD_REGISTER = "REGISTER"
MSG_REGISTER_OK = "REGISTER OK"
MSG_REGISTER_FAULT = "REGISTER FAULT"

SERVER_PORT = 5005

USER_DATA = []
addrs   = {} # dict: nome -> endereco. Ex: addrs["user"]=('127.0.0.1',17234)
clients = {} # dict: endereco -> nome. Ex: clients[('127.0.0.1',17234)]="user"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('', SERVER_PORT))

def registerPlayer(name, addr):
    if not name in addrs and not addr in clients:
      addrs[name] = addr
      clients[addr] = name
      responseToRegister(True, addr)
      return
    else:
      responseToRegister(False, addr)
      return

def responseToRegister(response, addr):
    if response:
        server.sendto(MSG_REGISTER_OK.encode(), addr)
    else:
        server.sendto(MSG_REGISTER_FAULT.encode(), addr)

while True:
    (msg, addr) = server.recvfrom(1024) # Buffer size
    cmd = msg.decode().split()
    if cmd[0] == CMD_REGISTER:
        registerPlayer(cmd[1], addr)

    if cmd[0] == "EXIT":
        server.exit()
