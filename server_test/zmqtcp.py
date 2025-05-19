import socket
import threading
import zmq

TCP_HOST = '0.0.0.0'
TCP_PORT = 7755
ZMQ_PUB_PORT = 6000

context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(f"tcp://*:{ZMQ_PUB_PORT}")

def handle_client(conn, addr):
    client_ip = addr[0]
