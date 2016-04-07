import socket
from GameLogic import *

UDP_IP = "localhost"
UDP_PORT = 5005

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    board = GameLogic()
    sock.sendto("REGISTER Name", (UDP_IP, UDP_PORT))

if __name__ == "__main__":
    main()
