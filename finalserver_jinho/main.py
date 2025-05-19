import time
from zmq_handler import setup_subscriber
from game_logic import players, players_hp, actions_order, action_time, game_started, process_round, start_timeout_timer, reset_game
from db_manager import init_db

sub_socket = setup_subscriber()
init_db()

print("ZMQ 게임 서버 시작 - 메시지 대기 중...")

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
        elif "player2" not in players.values():
            players[ip] = "player2"

    if not game_started and len(players) == 2:
        print("\n게임 시작!")
        game_started = True

    if game_started and ip in players:
        player = players[ip]
        if any(entry[0] == player for entry in actions_order):
            continue
        actions_order.append((player, action))
        action_time[player] = time.time()

        if len(actions_order) == 1:
            start_timeout_timer()
        elif len(actions_order) == 2:
            process_round()
