# relay_server.py - TCP 클라이언트와 ZMQ 서버 간의 중개 서버
import socket
import threading
import zmq
import time

# TCP 설정
TCP_PORT = 7755 # 클라이언트 (ESP8266)가 연결할 포트 (client.cpp와 일치)
BUFFER_SIZE = 1024 # 수신 버퍼 크기

# ZMQ 설정 (main.py <-> relay_server.py)
# main.py에서 액션을 받아오는 SUB 소켓
ZMQ_SUB_PORT_FOR_ACTIONS = "6000"
# main.py로 클라이언트 액션을 발행하는 PUB 소켓
ZMQ_PUB_PORT_FOR_ACTIONS = "6000"

# main.py에서 게임 상태 플래그를 받아오는 SUB 소켓
ZMQ_SUB_PORT_FOR_FLAGS = "6001"
# 클라이언트에게 게임 상태 플래그를 전송하기 위해 ZMQ에서 받은 플래그를 저장할 변수
current_game_state_flag = '0' # 초기값: '0' (대기)

# ZMQ 컨텍스트
context = zmq.Context()

# 클라이언트 액션을 main.py로 발행하는 PUB 소켓
publisher_socket = context.socket(zmq.PUB)
publisher_socket.bind(f"tcp://*:{ZMQ_PUB_PORT_FOR_ACTIONS}")
print(f"[Relay] Publishing client actions on tcp://*:{ZMQ_PUB_PORT_FOR_ACTIONS}")

# main.py로부터 게임 상태 플래그를 구독하는 SUB 소켓
subscriber_socket = context.socket(zmq.SUB)
subscriber_socket.connect(f"tcp://localhost:{ZMQ_SUB_PORT_FOR_FLAGS}")
subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, "GAME_STATE") # "GAME_STATE" 주제 구독
print(f"[Relay] Subscribing to game state on tcp://localhost:{ZMQ_SUB_PORT_FOR_FLAGS}")

# 활성 클라이언트 연결을 저장하는 딕셔너리: {IP: socket_object}
connected_clients = {}
# 연결된 클라이언트의 IP 주소를 저장하는 셋 (중복 방지)
connected_client_ips = set()

# ZMQ 메시지 수신 (게임 상태 플래그)
def zmq_subscriber_thread():
    global current_game_state_flag
    while True:
        try:
            msg = subscriber_socket.recv_string()
            parts = msg.split(',')
            if len(parts) == 2 and parts[0] == "GAME_STATE":
                new_flag = parts[1].strip()
                if new_flag != current_game_state_flag:
                    current_game_state_flag = new_flag
                    print(f"[Relay] ZMQ Game State Flag updated to: {current_game_state_flag}")
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM: # Context termination
                break
            print(f"[Relay Error] ZMQ Subscriber error: {e}")
        except Exception as e:
            print(f"[Relay Error] Unexpected ZMQ subscriber error: {e}")
        time.sleep(0.01) # CPU 사용률 줄이기

# 모든 연결된 클라이언트에게 현재 게임 상태 플래그를 전송
def send_game_flag_to_clients(flag_byte):
    """
    모든 연결된 TCP 클라이언트에게 현재 게임 상태 플래그(1바이트 문자열)를 전송합니다.
    """
    # connected_clients 딕셔너리를 순회하면서 클라이언트 소켓에 플래그 전송
    # 순회 중 딕셔너리 변경을 피하기 위해 items()를 리스트로 변환하여 사용
    for client_ip, client_sock in list(connected_clients.items()): 
        try:
            # print(f"[Relay] Sending flag '{flag_byte}' to {client_ip}") # 디버깅용
            client_sock.sendall(flag_byte.encode()) # '0' 또는 '1' 문자열을 바이트로 변환하여 전송. sendall은 모든 데이터를 보장
        except BrokenPipeError:
            print(f"[Relay] Client {client_ip} disconnected (BrokenPipeError). Removing.")
            # 연결이 끊긴 소켓을 안전하게 제거 (현재 순회 중이므로, 다음 반복에서 문제 없을 것)
            if client_ip in connected_clients:
                del connected_clients[client_ip]
            connected_client_ips.discard(client_ip)
        except Exception as e:
            print(f"[Relay Error] Failed to send flag to {client_ip}: {e}")
            if client_ip in connected_clients:
                del connected_clients[client_ip]
            connected_client_ips.discard(client_ip)

# TCP 클라이언트 처리 스레드 함수
def handle_client(client_socket, addr):
    client_ip = addr[0]
    print(f"[Relay] Connected by {client_ip}")
    connected_clients[client_ip] = client_socket
    connected_client_ips.add(client_ip) # IP 목록에 추가

    try:
        # 클라이언트 연결 시 현재 게임 상태 플래그를 바로 전송
        # 이렇게 하면 클라이언트가 접속하자마자 최신 게임 상태를 알 수 있습니다.
        send_game_flag_to_clients(current_game_state_flag)

        while True:
            # TCP 소켓의 recv()는 블로킹될 수 있으므로, 일정 시간 타임아웃 설정 (옵션)
            # client_socket.settimeout(0.1) # 0.1초 타임아웃
            data = client_socket.recv(BUFFER_SIZE)
            if not data: # 클라이언트 연결 끊김
                print(f"[Relay] Client {client_ip} disconnected.")
                break
            
            message = data.decode('utf-8').strip() # 수신된 바이트를 문자열로 디코딩, 공백 제거
            if message:
                print(f"[Relay] Received from {client_ip}: {message}")
                # 수신된 액션과 클라이언트 IP를 main.py로 ZMQ PUB 발행
                publisher_socket.send_string(f"{client_ip},{message}")

            # 주기적으로 게임 상태 플래그를 클라이언트에 전송 (게임 상태 동기화)
            # 매 루프마다 전송하면 불필요한 네트워크 트래픽이 발생할 수 있으므로,
            # 특정 간격으로만 전송하도록 개선하거나, ZMQ 구독 스레드에서 플래그 변경 시에만 전송하는 방식으로 고려
            # 여기서는 현재 구현의 주기적 전송 방식을 유지합니다.
            send_game_flag_to_clients(current_game_state_flag)
            time.sleep(0.05) # 너무 빠른 송신 방지 및 CPU 부하 감소

    except ConnectionResetError:
        print(f"[Relay] Client {client_ip} forcibly disconnected by peer.")
    except socket.timeout:
        # recv() 타임아웃 발생 시 (논블로킹처럼 동작)
        pass 
    except Exception as e:
        print(f"[Relay Error] Handling client {client_ip} error: {e}")
    finally:
        # 클라이언트 소켓 닫기
        client_socket.close()
        # 연결된 클라이언트 목록에서 제거
        if client_ip in connected_clients: # 안전하게 제거
            del connected_clients[client_ip]
        connected_client_ips.discard(client_ip)


# 메인 서버 함수
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 포트 재사용
    server_socket.bind(('', TCP_PORT))
    server_socket.listen(5) # 최대 5개의 대기 연결

    print(f"[Relay] TCP server listening on port {TCP_PORT}")

    # ZMQ 구독자 스레드 시작
    zmq_sub_thread = threading.Thread(target=zmq_subscriber_thread, daemon=True)
    zmq_sub_thread.start()

    while True:
        try:
            client_socket, addr = server_socket.accept() # 클라이언트 연결 대기
            # 각 클라이언트를 위한 새로운 스레드 시작
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_handler.start()
        except KeyboardInterrupt:
            print("[Relay] Server shutting down.")
            break
        except Exception as e:
            print(f"[Relay Error] Accepting new connection error: {e}")
    
    server_socket.close()
    context.term() # ZMQ 컨텍스트 종료

if __name__ == "__main__":
    main()
