import zmq
import time
import threading
import sqlite3  # ✅ SQLite 사용

context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:6000")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

players = {}  # IP → player1 / player2
players_hp = {"player1": 100, "player2": 100}
actions_order = []
action_time = {}
movement_window = 0.1
action_timeout = 1.5
game_started = False
timeout_timer = None

# ✅ DB 연결 및 초기화
conn = sqlite3.connect("player_stats.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            client_ip TEXT PRIMARY KEY NOT NULL,
            total INTEGER NOT NULL DEFAULT 0,
            win INTEGER NOT NULL DEFAULT 0,
            lose INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()

init_db()

def update_stats(winner_ip):
    for ip in players:
        cursor.execute("SELECT * FROM stats WHERE client_ip = ?", (ip,))
        row = cursor.fetchone()

        if row is None:
            cursor.execute("INSERT INTO stats (client_ip, total, win, lose) VALUES (?, 0, 0, 0)", (ip,))
        
        if ip == winner_ip:
            cursor.execute("UPDATE stats SET win = win + 1, total = total + 1 WHERE client_ip = ?", (ip,))
        else:
            cursor.execute("UPDATE stats SET lose = lose + 1, total = total + 1 WHERE client_ip = ?", (ip,))

    conn.commit()

print("ZMQ 구독 서버 시작 - 메시지 대기 중...")

def process_round():
    global timeout_timer
    if timeout_timer:
        timeout_timer.cancel()
        timeout_timer = None

    if len(actions_order) == 1:
        acting_player, action = actions_order[0]
        other_player = "player2" if acting_player == "player1" else "player1"
        print(f"\n[단독 행동 처리] {acting_player} → {action}")

        if action == "ATTACK":
            players_hp[other_player] -= 10
            print(f"{other_player}가 반응하지 못해 피격! HP: {players_hp[other_player]}")
        elif action == "MOVEMENT":
            print(f"{acting_player}가 회피했지만 상대가 반응 없음. 아무 일 없음.")
    else:
        p1, action1 = actions_order[0]
        p2, action2 = actions_order[1]
        print(f"\n[라운드 처리 순서]")
        print(f"1. {p1}: {action1}")
        print(f"2. {p2}: {action2}")

        t1 = action_time[p1]
        t2 = action_time[p2]

        if action1 == "ATTACK":
            if action2 == "MOVEMENT" and (t1 - t2 <= movement_window):
                print(f"{p1}의 공격은 {p2}의 회피로 무시됨!")
            else:
                players_hp[p2] -= 10
                print(f"{p1}가 {p2}를 공격! HP: {players_hp[p2]}")

        if action2 == "ATTACK":
            if action1 == "MOVEMENT" and (t2 - t1 <= movement_window):
                print(f"{p2}의 공격은 {p1}의 회피로 무시됨!")
            else:
                players_hp[p1] -= 10
                print(f"{p2}가 {p1}를 공격! HP: {players_hp[p1]}")

    for p in ["player1", "player2"]:
        players_hp[p] = max(players_hp[p], 0)

    if players_hp["player1"] <= 0 or players_hp["player2"] <= 0:
        print("\n=== 게임 종료 ===")
        winner = None
        if players_hp["player1"] > players_hp["player2"]:
            winner = [ip for ip, name in players.items() if name == "player1"][0]
            print("승자: player1")
        elif players_hp["player2"] > players_hp["player1"]:
            winner = [ip for ip, name in players.items() if name == "player2"][0]
            print("승자: player2")
        else:
            print("무승부")

        if winner:
            update_stats(winner)
        else:
            # 무승부면 둘 다 패배로 치지 않음, total만 증가
            for ip in players:
                cursor.execute("SELECT * FROM stats WHERE client_ip = ?", (ip,))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO stats (client_ip, total, win, lose) VALUES (?, 0, 0, 0)", (ip,))
                cursor.execute("UPDATE stats SET total = total + 1 WHERE client_ip = ?", (ip,))
            conn.commit()

        reset_game()
        return False

    actions_order.clear()
    action_time.clear()
    return True

def reset_game():
    global players, players_hp, actions_order, action_time, game_started, timeout_timer
    if timeout_timer:
        timeout_timer.cancel()
        timeout_timer = None
    players = {}
    players_hp = {"player1": 100, "player2": 100}
    actions_order = []
    action_time = {}
    game_started = False
    print("\n--- 새 게임 대기 중 ---")

def start_timeout_timer():
    global timeout_timer
    if timeout_timer:
        timeout_timer.cancel()
    timeout_timer = threading.Timer(action_timeout, lambda: process_round())
    timeout_timer.start()

while True:
    msg = sub_socket.recv_string()
    parts = msg.split(',')

    if len(parts) != 2:
        continue

    ip = parts[0].strip()
    action = parts[1].strip().upper()

    if ip not in players:
        if "player1" not in players.values():
            players[ip] = "player1"
            print(f"[{ip}] player1로 등록")
        elif "player2" not in players.values():
            players[ip] = "player2"
            print(f"[{ip}] player2로 등록")

    if not game_started and len(players) == 2:
        print("\n두 명의 플레이어가 접속했습니다. 게임 시작!")
        print("플레이어 목록:", players)
        game_started = True

    if game_started and ip in players:
        player = players[ip]

        if any(entry[0] == player for entry in actions_order):
            continue

        actions_order.append((player, action))
        action_time[player] = time.time()

        if len(actions_order) == 1:
            start_timeout_timer()

        if len(actions_order) == 2:
            process_round()
