# # server.py
# # 서버 코드
# # 라즈베리파이에서 규모가 커지면 docker로 묶어서 배포를 염두해 둘 것
# # 최종 디버깅이 끝나면 bash 파일에 넣어서 부팅시 서버 구동되게 지정할 것

# # Raspberry Pi (receiver.py)
# import zmq
# import threading
# import time

# def process_data(device_id, data):
#     """수신된 데이터를 처리하는 함수 (비동기 처리 예시)"""
#     print(f"[{device_id}] Received: {data}")
#     time.sleep(0.1) # 데이터 처리 시뮬레이션

# def receiver():
#     context = zmq.Context()
#     pull_socket = context.socket(zmq.PULL)
#     pull_socket.bind("tcp://*:4796")

#     while True:
#         try:
#             message = pull_socket.recv_json()
#             device_id = message.get("device_id", "Unknown")
#             data = message.get("data")
#             if data:
#                 # 각 장치에서 받은 데이터를 별도의 스레드에서 처리 (비동기 처리)
#                 threading.Thread(target=process_data, args=(device_id, data)).start()
#         except zmq.error.ContextTerminated:
#             break
#         except Exception as e:
#             print(f"Error receiving data: {e}")

# if __name__ == "__main__":
#     receiver_thread = threading.Thread(target=receiver)
#     receiver_thread.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("\nReceiver stopped.")
#     finally:
#         context.term()

#import zmq 
#import threading
#import time
#
#def process_data(device_id, data):
#    """수신된 데이터를 처리하는 함수 (비동기 처리 예시)"""
#    print(f"[{device_id}] Received from {device_id}: {data}")
#    time.sleep(0.1) # 데이터 처리 시뮬레이션
#
#def receiver():
#    context = zmq.Context()
#    pull_socket = context.socket(zmq.PULL)
#    pull_socket.bind("tcp://*:4796")
#
#    while True:
#        try:
#            message = pull_socket.recv_json()
#            device_id = message.get("device_id", "Unknown")
#            data = message.get("data")
#            if data:
#                threading.Thread(target=process_data, args=(device_id, data)).start()
#        except zmq.error.ContextTerminated:
#            break
#        except Exception as e:
#            print(f"Error receiving data: {e}")
#
#if __name__ == "__main__":
#    receiver_thread = threading.Thread(target=receiver)
#    receiver_thread.start()
#
#    try:
#        while True:
#            time.sleep(1)
#    except KeyboardInterrupt:
#        print("\nServer stopped.")
#    finally:
#        context.term()



# import socket

# # 서버 IP 주소 및 포트
# SERVER_IP = '0.0.0.0'  # 모든 인터페이스에서 수신
# SERVER_PORT = 4796

# def run_server():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((SERVER_IP, SERVER_PORT))
#     server_socket.listen(1)  # 최대 1개의 연결 대기
#     print(f"서버가 {SERVER_IP}:{SERVER_PORT} 에서 연결을 대기 중입니다...")

#     while True:
#         client_socket, client_address = server_socket.accept()
#         print(f"클라이언트 {client_address} 연결됨.")
#         try:
#             while True:
#                 data = client_socket.recv(1024)
#                 if not data:
#                     break
#                 decoded_data = data.decode('utf-8')
#                 print(f"수신된 데이터: {decoded_data}")
#         except Exception as e:
#             print(f"오류 발생: {e}")
#         finally:
#             client_socket.close()
#             print(f"클라이언트 {client_address} 연결 종료.")

# if __name__ == "__main__":
#     run_server()

# import zmq
# import socket

# # ZMQ 설정
# context = zmq.Context()
# receiver = context.socket(zmq.PULL)
# port = 7755  # ESP8266 코드와 동일한 포트 번호 사용
# receiver.bind(f"tcp://*:{port}")
# print(f"ZMQ receiver listening on port {port}...")

# while True:
#     try:
#         # ESP8266로부터 데이터 수신 (TCP 소켓 데이터 그대로 수신)
#         message = receiver.recv_string()

#         # 접속된 클라이언트 IP 주소 확인 (ESP8266의 IP 주소)
#         client_ip = ""
#         try:
#             # ESP8266가 연결될 때의 소켓 정보를 얻는 것은 ZMQ의 직접적인 기능이 아니므로,
#             # TCP 연결 시의 정보를 별도로 관리해야 합니다.
#             # 이 예시에서는 ESP8266의 IP 주소를 직접 출력합니다.
#             # 실제 환경에서는 연결 관리를 통해 IP 주소를 추적해야 할 수 있습니다.
#             # 가장 간단한 방법은 ESP8266가 보내는 데이터에 자신의 IP 주소를 포함시키는 것입니다.
#             client_ip = socket.gethostbyname(socket.gethostname()) # 라즈베리파이 자신의 IP를 임시로 사용
#         except socket.gaierror:
#             client_ip = "Unknown"

#         print(f"Client IP: {client_ip}, Received: {message}")

#     except zmq.error.ContextTerminated:
#         break
#     except KeyboardInterrupt:
#         break

# receiver.close()
# context.term()

import socket

HOST = '0.0.0.0'  # 모든 인터페이스에서 수신 대기
PORT = 7755       # ESP8266 코드와 동일한 포트 번호

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"TCP Server listening on port {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                decoded_data = data.decode('utf-8').strip()
                print(f"Client IP: {addr[0]}, Received: {decoded_data}")