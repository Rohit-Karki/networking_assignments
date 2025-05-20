# Your Python code must use the low-level socket API for networking and you must use the version of Python that is
# installed on the test machine (version 3.6).

import sys
import socket
import selectors
import types

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65430  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Accepting connection")
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
