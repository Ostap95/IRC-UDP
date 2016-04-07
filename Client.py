import socket

UDP_IP = "localhost"
UDP_PORT = 5005

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("Oi", (UDP_IP, UDP_PORT))

if __name__ == "__main__":
    main()
