import zmq
import time

# ZMQ 설정
context = zmq.Context()
recv_socket = context.socket(zmq.PULL)
recv_socket.bind("tcp://*:7755")  # ESP8266에서 전송

pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:6000")  # Python GUI에서 SUB

players = []
printed_players = set()
players_hp = {}
game_started = False

MAX_HP = 100
DAMAGE = 10

print("서버 시작 - 센서 수신 대기 중...")

try:
    while True:
        try:
            msg = recv_socket.recv(zmq.NOBLOCK).decode()

            parts = msg.split(',')
            if len(parts) == 1:
                # 메시지 형태: "ATTACK" 또는 "MOVEMENT"
                action = parts[0].strip()
                sender_ip = recv_socket.getsockopt(zmq.LAST_ENDPOINT).decode()  # 기본적으로는 여기서 IP 추출 어려움
                print(f"[수신됨] 행동: {action} - (실제 IP 식별은 별도 필요)")
                continue

            # 메시지 형태: ip,gx,gy,gz 또는 ip,ATTACK
            ip = parts[0].strip()

            # 플레이어 등록
            if ip not in players:
                players.append(ip)
                players_hp[ip] = MAX_HP
                print(f"접속한 플레이어 IP: {ip}")

            # 게임 시작
            if not game_started and len(players) == 2:
                print("\n두 명의 플레이어가 접속했습니다. 게임 시작!")
                print("플레이어 IP 목록:")
                for p in players:
                    print("-", p)
                pub_socket.send_string("START")
                game_started = True

            # 센서 기반 메시지
            if len(parts) == 4:
                # 센서 메시지 처리 (gx, gy, gz)
                gx, gy, gz = map(float, parts[1:])
                pub_socket.send_string(f"{gx},{gy},{gz}")
                continue

            # 공격/이동 메시지 처리
            if len(parts) == 2:
                action = parts[1].strip().upper()

                if action == "ATTACK":
                    if len(players) < 2:
                        continue
                    # 공격자: ip, 상대방: 다른 IP
                    attacker = ip
                    target = players[1] if players[0] == ip else players[0]

                    players_hp[target] -= DAMAGE
                    players_hp[target] = max(0, players_hp[target])  # 최소 0

                    print(f"{attacker}가 {target}를 공격! {target} HP: {players_hp[target]}")
                    pub_socket.send_string(f"DAMAGE,{target},{players_hp[target]}")

                    if players_hp[target] <= 0:
                        print("\n=== 게임 종료 ===")
                        print(f"승자: {attacker}")
                        pub_socket.send_string(f"WINNER,{attacker}")
                        break
                    
                elif action == "MOVEMENT":
                    print(f"{ip} 움직임 감지 (회피)")
                    pub_socket.send_string(f"MOVEMENT,{ip}")

        except zmq.Again:
            time.sleep(0.01)

except KeyboardInterrupt:
    print("서버 종료 중...")
