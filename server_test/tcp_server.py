# tcp_server.py
import socket

server_ip = "192.168.0.43"
server_port = 4796

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((server_ip, server_port))
sock.listen(1)
print("Waiting for connection...")

conn, addr = sock.accept()
print("Connected by", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Received:", data.decode())

conn.close()
