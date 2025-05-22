# relay_server.py
# TCP 중개 서버
import socket           #TCP 네트워킹을 위한 기본 파이썬 모듈
import threading        #클라이언트 여러 명을 동시에 처리하기 위한 스레드 지원
import zmq              #ZeroMQ 메시징 라이브러리

TCP_HOST = '0.0.0.0'     # 모든 인터페이스에서 접속 허용
TCP_PORT = 7755          # TCP 서버가 클라이언트를 받는 포트
ZMQ_PUB_PORT = 6000      # 퍼블리셔(PUB)가 메시지를 보내는 ZMQ 포트

context = zmq.Context()     #ZMQ 컨텍스트 생성
pub_socket = context.socket(zmq.PUB)        #PUB 소켓 생성 (퍼블리셔 역할)
pub_socket.bind(f"tcp://*:{ZMQ_PUB_PORT}")  #TCP 포트 6000에서 바인딩: 구독자(SUB)가 이 주소로 접속 가능

client_sockets = {}  # {ip: conn}

#클라이언트 한 명을 처리하는 함수
def handle_client(conn, addr):
    client_ip = addr[0]                     #conn: TCP 연결 소켓, addr: (IP, 포트) 형태의 클라이언트 주소
    print(f"[{client_ip}] TCP 연결됨")      #클라이언트 IP를 따로 저장하여 로그에 출력
    client_sockets[client_ip] = conn    #클라이언트 IP와 연결 소켓을 딕셔너리에 저장

#연결이 유지되는 동안 메시지를 계속 수신, data가 없으면 (연결 종료) 루프 탈출
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                decoded_data = data.decode('utf-8').strip()     #수신한 데이터를 UTF-8 문자열로 디코딩 후 공백 제거
                pub_socket.send_string(f"{client_ip},{decoded_data}")   #메시지를 "IP,메시지" 형식으로 구성하여 ZMQ PUB 소켓을 통해 송신
            #클라이언트가 강제 종료하는 경우 예외 발생 → 연결 종료
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"에러: {e}")
                break

    if client_ip in client_sockets:
        del client_sockets[client_ip]
    print(f"[{client_ip}] 연결 종료됨")

def send_flag_to_clients(flag):
    for ip, conn in client_sockets.items():
        try:
            conn.sendall(str(flag).encode('utf-8'))
        except Exception as e:
            print(f"[{ip}] 플래그 전송 실패: {e}")

print(f"TCP 중개 서버 시작 - 포트 {TCP_PORT}")

#TCP 소켓 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    #SO_REUSEADDR : 서버 재시작 시 "포트 점유 중" 오류 방지
    tcp_server.bind((TCP_HOST, TCP_PORT))       #IP 및 포트에 서버 소켓 연결
    tcp_server.listen()     #클라이언트 연결 대기 상태 진입

    while True:
        conn, addr = tcp_server.accept()    #클라이언트가 접속하면 accept()로 연결 수락
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True) #새 스레드를 만들어 handle_client()로 해당 클라이언트를 처리, daemon=True: 메인 스레드가 종료되면 자동으로 같이 종료
        thread.start() 