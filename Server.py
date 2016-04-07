import socket

UDP_IP = "localhost"
UDP_PORT = 5005

USER_DATA = []

def registerPlayer(playName):
    USER_DATA.append(playName)
    return

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(1024) # Buffer size
        print "received message:", data
        if(data.find("REGISTER"),len(data) > 0):
            registerPlayer(data[9:len(data)])

        for data in USER_DATA:
            print data

    return

if __name__ == "__main__":
    main()
