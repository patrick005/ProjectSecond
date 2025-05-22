import zmq
import time

context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:6000")
sub_socket.subscribe("")

class Player:
    def __init__(self, ip):
        self.ip = ip
        self.hp = 100
        self.last_action = None
        self.last_time = 0

    def is_alive(self):
        return self.hp > 0

players = {}
player_order = []
actions_order = []
game_started = False
DAMAGE = 10
EVADE_WINDOW = 0.1  # 초

def process_round():
    global actions_order

    p1, p2 = player_order
    a1 = players[p1]
    a2 = players[p2]

    ip1, action1, time1 = actions_order[0]
    ip2, action2, time2 = actions_order[1]

    print(f"\n[라운드 처리]")
    print(f"1. {ip1} → {action1} @ {time1:.3f}")
    print(f"2. {ip2} → {action2} @ {time2:.3f}")

    attacker, defender = (a1, a2) if ip1 == p1 else (a2, a1)
    attacker_action, defender_action = (action1, action2) if attacker.ip == ip1 else (action2, action1)
    attacker_time, defender_time = (time1, time2) if attacker.ip == ip1 else (time2, time1)

    # 회피 판정
    evade_success = (
        defender_action == "MOVEMENT" and
        0 < attacker_time - defender_time <= EVADE_WINDOW
    )

    if attacker_action == "ATTACK":
        if defender_action == "ATTACK":
            # 먼저 공격한 사람이 타격
            defender.hp = max(0, defender.hp - DAMAGE)
            print(f"{attacker.ip}가 먼저 공격! {defender.ip} HP 감소 → {defender.hp}")
        elif evade_success:
            print(f"{defender.ip}가 회피 성공! {attacker.ip}의 공격 무효")
        else:
            defender.hp = max(0, defender.hp - DAMAGE)
            print(f"{attacker.ip}의 공격 명중! {defender.ip} HP 감소 → {defender.hp}")
    elif attacker_action == "MOVEMENT" and defender_action == "ATTACK":
        if attacker_time < defender_time and (
            0 < defender_time - attacker_time <= EVADE_WINDOW
        ):
            print(f"{attacker.ip}가 회피 성공! {defender.ip}의 공격 무효")
        else:
            attacker.hp = max(0, attacker.hp - DAMAGE)
            print(f"{defender.ip}의 공격 명중! {attacker.ip} HP 감소 → {attacker.hp}")
    else:
        print("서로 회피하거나 공격 없음")

    actions_order = []

    if not a1.is_alive() or not a2.is_alive():
        winner = a1 if a1.is_alive() else a2
        print(f"\n=== 게임 종료 ===")
        print(f"승자: {winner.ip}")
        return False
    return True

print("ZMQ 구독 서버 시작 - 메시지 대기 중...")

while True:
    msg = sub_socket.recv_string()
    parts = msg.split(',')
    if len(parts) != 2:
        continue

    ip = parts[0].strip()
    action = parts[1].strip().upper()
    now = time.time()

    if ip not in players:
        players[ip] = Player(ip)
        if ip not in player_order:
            player_order.append(ip)
            print(f"[{ip}] 플레이어 등록")

    if len(player_order) == 2 and not game_started:
        print("\n두 명의 플레이어가 접속했습니다. 게임 시작!")
        print(f"player1: {player_order[0]}")
        print(f"player2: {player_order[1]}")
        game_started = True

    if not game_started: 
        # or ip not in player_order :
        continue

    # 중복 입력 방지
    if any(entry[0] == ip for entry in actions_order):
        continue

    actions_order.append((ip, action, now))

    if len(actions_order) == 2:
        process_round()
        if not process_round():
            break
