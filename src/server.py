import zmq

context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:6000")  # 중개 서버의 ZMQ PUB 포트
sub_socket.subscribe("")  # 모든 메시지 구독

players = []
players_hp = {}
game_started = False
MAX_HP = 100
DAMAGE = 10

print("ZMQ 구독 서버 시작 - 중개 서버 메시지 대기 중...")

while True:
    msg = sub_socket.recv_string()
    parts = msg.split(',')
    if len(parts) >= 2:
        sender_ip = parts[0].strip()
        action = parts[1].strip().upper()

        # 플레이어 등록 (IP 주소 기반)
        if sender_ip not in players:
            players.append(sender_ip)
            players_hp[sender_ip] = MAX_HP
            print(f"[{sender_ip}] 플레이어 등록")

        if not game_started and len(players) == 2:
            print("\n두 명의 플레이어가 접속했습니다. 게임 시작!")
            print("플레이어 IP 목록:", players)
            # GUI로 시작 메시지 전송 (기존 pub_socket이 있다면 사용)
            # pub_socket.send_string("START")
            game_started = True

        if action == "ATTACK":
            if len(players) == 2:
                target_ip = players[1] if players[0] == sender_ip else players[0]
                if target_ip in players_hp:
                    players_hp[target_ip] -= DAMAGE
                    players_hp[target_ip] = max(0, players_hp[target_ip])
                    print(f"[{sender_ip}]가 [{target_ip}]를 공격! [{target_ip}] HP: {players_hp[target_ip]}")
                    # GUI로 데미지 정보 전송 (기존 pub_socket이 있다면 사용)
                    # pub_socket.send_string(f"DAMAGE,{target_ip},{players_hp[target_ip]}")
                    if players_hp[target_ip] <= 0:
                        print("\n=== 게임 종료 ===")
                        print(f"승자: {sender_ip}")
                        # GUI로 승자 정보 전송 (기존 pub_socket이 있다면 사용)
                        # pub_socket.send_string(f"WINNER,{sender_ip}")
                        game_started = False
            else:
                print("두 명의 플레이어가 필요합니다.")

        elif action == "MOVEMENT":
            print(f"[{sender_ip}] 움직임 감지 (회피)")
            # GUI로 이동 정보 전송 (기존 pub_socket이 있다면 사용)
            # pub_socket.send_string(f"MOVEMENT,{sender_ip}")