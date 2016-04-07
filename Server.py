import socket

UDP_IP = "localhost"
UDP_PORT = 5005

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(1024) # Buffer size
        print "received message:", data

    return

if __name__ == "__main__":
    main()
