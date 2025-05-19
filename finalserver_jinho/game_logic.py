import time
import threading
from db_manager import update_stats, update_draw

players = {}
players_hp = {"player1": 100, "player2": 100}
actions_order = []
action_time = {}
movement_window = 0.1
action_timeout = 0.5
game_started = False
timeout_timer = None

def process_round():
    global timeout_timer, players, players_hp, actions_order, action_time, game_started
    if timeout_timer:
        timeout_timer.cancel()
        timeout_timer = None

    if len(actions_order) == 1:
        acting_player, action = actions_order[0]
        other_player = "player2" if acting_player == "player1" else "player1"
        if action == "ATTACK":
            players_hp[other_player] -= 10
    else:
        p1, action1 = actions_order[0]
        p2, action2 = actions_order[1]
        t1 = action_time[p1]
        t2 = action_time[p2]

        if action1 == "ATTACK":
            if action2 == "MOVEMENT" and (t1 - t2 <= movement_window):
                pass
            else:
                players_hp[p2] -= 10

        if action2 == "ATTACK":
            if action1 == "MOVEMENT" and (t2 - t1 <= movement_window):
                pass
            else:
                players_hp[p1] -= 10

    for p in ["player1", "player2"]:
        players_hp[p] = max(players_hp[p], 0)

    if players_hp["player1"] <= 0 or players_hp["player2"] <= 0:
        winner = None
        if players_hp["player1"] > players_hp["player2"]:
            winner = get_ip_by_role("player1")
        elif players_hp["player2"] > players_hp["player1"]:
            winner = get_ip_by_role("player2")
        if winner:
            update_stats(players, winner)
        else:
            update_draw(players)
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

def start_timeout_timer():
    global timeout_timer
    if timeout_timer:
        timeout_timer.cancel()
    timeout_timer = threading.Timer(action_timeout, lambda: process_round())
    timeout_timer.start()

def get_ip_by_role(role):
    return [ip for ip, name in players.items() if name == role][0]
