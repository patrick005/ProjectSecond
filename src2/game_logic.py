# game_logic.py
# 게임 로직 처리
import time
import threading
from db_manager import update_stats, update_draw
from relay_server import send_flag_to_clients  # TCP 플래그 전송 함수 불러오기


players = {}        #접속한 클라이언트 IP와 "player1"/"player2" 역할 매핑
players_hp = {"player1": 100, "player2": 100}       #두 플레이어의 체력
actions_order = []      #순서대로 입력된 (플레이어, 행동) 리스트
action_time = {}        #각 플레이어의 행동 입력 시간 저장
movement_window = 0.1   #회피 허용 시간(0.1초 이내에 MOVEMENT가 먼저 입력되면 회피 성공)
action_timeout = 0.5    #행동 미 입력시 자동 처리 대기 시간 (0.5초)
game_started = False    #게임 시작 여부
timeout_timer = None    #해당 타이머 객체

#라운드 처리 (2명 행동 입력 or 타임아웃)
def process_round():
    global timeout_timer, players, players_hp, actions_order, action_time, game_started
    #타임아웃 타이머가 있으면 종료
    if timeout_timer:
        timeout_timer.cancel()
        timeout_timer = None

    #상대방 입력 없이 한 명만 "ATTACK" 하면 무조건 적중 → 상대 HP -10
    if len(actions_order) == 1:
        acting_player, action = actions_order[0]
        other_player = "player2" if acting_player == "player1" else "player1"
        if action == "ATTACK":
            players_hp[other_player] -= 10

    #양쪽 모두 입력된 경우, 두 사람의 행동과 타이밍을 가져옴
    else:
        p1, action1 = actions_order[0]
        p2, action2 = actions_order[1]
        t1 = action_time[p1]
        t2 = action_time[p2]

        #player1이 ATTACK, player2가 MOVEMENT이고 player2가 빠르면 회피 성공 상대방보다 0.1초 이상 먼저 MOVEMENT 입력
        if action1 == "ATTACK":
            if action2 == "MOVEMENT" and (t1 - t2 <= movement_window):
                pass
            else:
                players_hp[p2] -= 10

        #player2이 ATTACK, player1가 MOVEMENT이고 player2가 빠르면 회피 성공 상대방보다 0.1초 이상 먼저 MOVEMENT 입력
        if action2 == "ATTACK":
            if action1 == "MOVEMENT" and (t2 - t1 <= movement_window):
                pass
            else:
                players_hp[p1] -= 10

    #체력은 0 아래로 내려가지 않게 보정
    for p in ["player1", "player2"]:
        players_hp[p] = max(players_hp[p], 0)

    # 승패/무승부 판단
    if players_hp["player1"] <= 0 or players_hp["player2"] <= 0:
        winner = None
        if players_hp["player1"] > players_hp["player2"]:
            winner = get_ip_by_role("player1")
        elif players_hp["player2"] > players_hp["player1"]:
            winner = get_ip_by_role("player2")
        if winner:
            update_stats(players, winner)#
        else:
            update_draw(players)
        reset_game()
        # 게임 종료 플래그 설정//////////////////
        return False

    #다음 라운드 준비
    actions_order.clear()
    action_time.clear()
    return True

#게임 상태 전체 초기화
def reset_game():
    global players, players_hp, actions_order, action_time, game_started, timeout_timer
    if timeout_timer:
        timeout_timer.cancel()
        timeout_timer = None

    send_flag_to_clients(0)  # 게임 종료: flag 0 전송

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
    timeout_timer.start()   #일정 시간(0.5초) 동안 두 번째 입력이 없으면 process_round()를 자동 호출

def get_ip_by_role(role):
    return [ip for ip, name in players.items() if name == role][0]
    #"player1"/"player2"에 해당하는 IP 주소를 찾아서 반환

