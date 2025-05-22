# main.py
# 게임 실행 메인 스크립트
import time
from zmq_handler import setup_subscriber    #ZMQ 구독 소켓(subscriber) 설정 함수
from game_logic import *                    #게임 관련 전역 변수와 함수들이 정의된 모듈
from db_manager import init_db              #DB 초기화 함수. 게임 결과 저장을 위한 DB 설정
from relay_server import send_flag_to_clients  # TCP 플래그 전송 함수 임포트

sub_socket = setup_subscriber() #ZMQ 구독 소켓 생성. 이 소켓을 통해 클라이언트 메시지 수신
init_db()   #DB초기화 및 테이블 생성 준비

print("ZMQ 게임 서버 시작 - 메시지 대기 중...")

while True:
    msg = sub_socket.recv_string()  
    parts = msg.split(',')  #메시지를 쉼표로 나눠 IP와 액션을 분리

    if len(parts) != 2: #형식이 잘못된 메시지는 무시 (continue로 루프 처음으로 돌아감)
        continue

    ip = parts[0].strip()   #공백 제거 후 IP 주소와 행동(Action)을 변수에 저장
    action = parts[1].strip().upper()   #행동은 대문자로 변환 (일관성 유지 목적),원래는 대문자로 보내지는 값이긴함 혹시몰라

    #처음 보는 IP일 경우, 두 명까지 player1, player2로 등록
    if ip not in players:
        if "player1" not in players.values():
            players[ip] = "player1"
        elif "player2" not in players.values():
            players[ip] = "player2"

    #플레이어가 두 명 등록되면 게임 시작
    if not game_started and len(players) == 2:
        print("\n게임 시작!")
        game_started = True# 게임 시작 플래그 설정//////////////////
        send_flag_to_clients(1)  # 게임 시작: flag 1 전송

    #게임이 시작되고 해당 IP가 등록된 플레이어일 경우만 진행
    if game_started and ip in players:
        player = players[ip]
        if any(entry[0] == player for entry in actions_order):
            continue
        actions_order.append((player, action))
        action_time[player] = time.time()

        #첫 번째 플레이어의 액션이 오면 타이머 시작 (예: 상대방이 제한 시간 내 반응하지 않을 경우 처리)
        if len(actions_order) == 1:
            start_timeout_timer()
        elif len(actions_order) == 2:
            process_round()