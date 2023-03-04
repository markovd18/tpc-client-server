import sys
from socket import *


def run(port: int):
    s = socket(AF_INET, SOCK_STREAM)  # IPv4, TCP
    s.connect(("127.0.0.1", 8080))  # Connect (host, port)

    s.send(b"GET / HTTP/1.0\n\n")  # Send request

    data = s.recv(10000)  # Get response
    print("Response: " + str(data.decode()))

    s.close()


run(8080)
