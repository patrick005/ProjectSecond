import zmq
import time

context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:6000")  # 중개 서버의 PUB 포트
sub_socket.subscribe("")

players = []
players_hp = {}
actions_order = []  # 순서대로 (ip, action) 저장
MAX_HP = 100
DAMAGE = 10
game_started = False

print("ZMQ 구독 서버 시작 - 메시지 대기 중...")

def process_round():
    first_ip, first_action = actions_order[0]
    second_ip, second_action = actions_order[1]

    print(f"\n[라운드 처리 순서]")
    print(f"1. {first_ip}: {first_action}")
    print(f"2. {second_ip}: {second_action}")

    if first_action == "ATTACK" and second_action == "ATTACK":
        players_hp[second_ip] -= DAMAGE
        print(f"{first_ip}가 먼저 공격! {second_ip}가 피격됨. HP: {players_hp[second_ip]}")
    elif first_action == "ATTACK" and second_action == "MOVEMENT":
        print(f"{first_ip}가 공격했지만 {second_ip}가 회피 성공!")
    elif first_action == "MOVEMENT" and second_action == "ATTACK":
        print(f"{second_ip}가 공격했지만 {first_ip}가 회피 성공!")
    elif first_action == "MOVEMENT" and second_action == "MOVEMENT":
        print("둘 다 회피. 아무 일 없음.")

    # 체력 0 확인
    for ip in players:
        players_hp[ip] = max(0, players_hp[ip])
        if players_hp[ip] <= 0:
            print(f"\n=== 게임 종료 ===")
            print(f"승자: {players[1] if ip == players[0] else players[0]}")
            return False  # 게임 종료

    actions_order.clear()
    return True  # 다음 라운드 진행

while True:
    msg = sub_socket.recv_string()
    parts = msg.split(',')

    if len(parts) == 2:
        ip = parts[0].strip()
        action = parts[1].strip().upper()

        if ip not in players:
            players.append(ip)
            players_hp[ip] = MAX_HP
            print(f"[{ip}] 플레이어 등록")

        if not game_started and len(players) == 2:
            print("\n두 명의 플레이어가 접속했습니다. 게임 시작!")
            print("플레이어 목록:", players)
            game_started = True

        if game_started:
            # 한 플레이어가 중복 입력 못 하도록
            if any(entry[0] == ip for entry in actions_order):
                continue
            actions_order.append((ip, action))

            if len(actions_order) == 2:
                keep_going = process_round()
                if not keep_going:
                    break
