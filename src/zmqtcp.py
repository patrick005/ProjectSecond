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
    print(f"[{client_ip}] TCP 연결됨")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"[{client_ip}] TCP 연결 종료")
                    break
                decoded_data = data.decode('utf-8').strip()
                print(f"[{client_ip}] TCP 수신: {decoded_data}")
                pub_socket.send_string(f"{client_ip},{decoded_data}")
            except ConnectionResetError:
                print(f"[{client_ip}] 연결이 비정상 종료됨")
                break

print(f"TCP 중개 서버 시작 - 포트 {TCP_PORT} 대기")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server.bind((TCP_HOST, TCP_PORT))
    tcp_server.listen()

    while True:
        conn, addr = tcp_server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()