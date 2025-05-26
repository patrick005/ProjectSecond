# # # # game_logic.py - 게임의 핵심 로직을 처리하는 모듈
# # # import time
# # # import threading
# # # import zmq # ZMQ 임포트

# # # players = {}
# # # players_hp = {"player1": 100, "player2": 100}
# # # actions_order = []
# # # action_time = {}

# # # movement_window = 0.1
# # # action_timeout = 0.5

# # # game_started = False

# # # def send_gui_state_update(gui_socket, game_state_flag, p1_hp, p2_hp):
# # #     msg = f"GAME_STATE_GUI,{game_state_flag},{p1_hp}:{p2_hp}"
# # #     gui_socket.send_string(msg)

# # # def send_gui_hit_trigger(gui_socket, hit_player_role):
# # #     msg = f"HIT_GUI,{hit_player_role}"
# # #     gui_socket.send_string(msg)

# # # def send_gui_game_result(gui_socket, result_text):
# # #     msg = f"GAME_RESULT,{result_text}"
# # #     gui_socket.send_string(msg)

# # # def send_db_update_request(db_socket, ip, result_type):
# # #     """
# # #     C DB 서비스로 DB 업데이트 요청을 ZMQ PUSH 소켓으로 전송합니다.
# # #     @param db_socket: main.py로부터 전달받은 DB PUSH 소켓
# # #     @param ip: 클라이언트 IP 주소
# # #     @param result_type: "WIN", "LOSE", "DRAW" 중 하나
# # #     """
# # #     msg = f"{ip},{result_type}"
# # #     db_socket.send_string(msg)
# # #     print(f"[Game Logic] DB Update Request (PUSH) sent: {msg}")


# # # def process_round(gui_publisher_socket, db_pusher_socket): # DB PUSH 소켓 인자 추가
# # #     global players, players_hp, actions_order, action_time, game_started
    
# # #     if len(actions_order) < 2:
# # #         print("[Game Logic Error] process_round 호출 시 액션이 부족합니다.")
# # #         reset_game() # 비정상 상황 시 게임 리셋
# # #         return False

# # #     p1_role, action1 = actions_order[0]
# # #     p2_role, action2 = actions_order[1]
# # #     t1 = action_time[p1_role]
# # #     t2 = action_time[p2_role]

# # #     player1_ip = get_ip_by_role("player1")
# # #     player2_ip = get_ip_by_role("player2")

# # #     player1_action_data = (players[player1_ip], actions_order[0][1], action_time[players[player1_ip]]) if players[player1_ip] == p1_role else (players[player2_ip], actions_order[1][1], action_time[players[player2_ip]])
# # #     player2_action_data = (players[player2_ip], actions_order[1][1], action_time[players[player2_ip]]) if players[player2_ip] == p2_role else (players[player1_ip], actions_order[0][1], action_time[players[player1_ip]])

# # #     # 공격 판정 (이전과 동일)
# # #     if player1_action_data[1] == "ATTACK":
# # #         if player2_action_data[1] == "MOVEMENT" and (abs(player1_action_data[2] - player2_action_data[2]) <= movement_window):
# # #             print(f"[{player2_action_data[0]}] MOVEMENT! {player1_action_data[0]}'s ATTACK missed.")
# # #         else:
# # #             players_hp[player2_action_data[0]] -= 10
# # #             send_gui_hit_trigger(gui_publisher_socket, player2_action_data[0])
# # #             print(f"[{player1_action_data[0]}] ATTACK hit! {player2_action_data[0]} HP: {players_hp[player2_action_data[0]]}")

# # #     if player2_action_data[1] == "ATTACK":
# # #         if player1_action_data[1] == "MOVEMENT" and (abs(player2_action_data[2] - player1_action_data[2]) <= movement_window):
# # #             print(f"[{player1_action_data[0]}] MOVEMENT! {player2_action_data[0]}'s ATTACK missed.")
# # #         else:
# # #             players_hp[player1_action_data[0]] -= 10
# # #             send_gui_hit_trigger(gui_publisher_socket, player1_action_data[0])
# # #             print(f"[{player2_action_data[0]}] ATTACK hit! {player1_action_data[0]} HP: {players_hp[player1_action_data[0]]}")

# # #     for p in ["player1", "player2"]:
# # #         players_hp[p] = max(players_hp[p], 0)
    
# # #     print(f"Current HP - Player1: {players_hp['player1']}, Player2: {players_hp['player2']}")
# # #     send_gui_state_update(gui_publisher_socket, 1, players_hp["player1"], players_hp["player2"])

# # #     # 게임 종료 판정
# # #     if players_hp["player1"] <= 0 or players_hp["player2"] <= 0:
# # #         winner_ip = None
# # #         loser_ip = None
# # #         result_message = ""

# # #         if players_hp["player1"] > players_hp["player2"]: # P1 승리
# # #             winner_ip = get_ip_by_role("player1")
# # #             loser_ip = get_ip_by_role("player2")
# # #             result_message = f"Player1 ({winner_ip}) Wins!"
# # #             print(f"\n게임 종료! Player1 승리!")
# # #             send_db_update_request(db_pusher_socket, winner_ip, "WIN") # 승자 DB 업데이트 요청
# # #             send_db_update_request(db_pusher_socket, loser_ip, "LOSE") # 패자 DB 업데이트 요청
# # #         elif players_hp["player2"] > players_hp["player1"]: # P2 승리
# # #             winner_ip = get_ip_by_role("player2")
# # #             loser_ip = get_ip_by_role("player1")
# # #             result_message = f"Player2 ({winner_ip}) Wins!"
# # #             print(f"\n게임 종료! Player2 승리!")
# # #             send_db_update_request(db_pusher_socket, winner_ip, "WIN") # 승자 DB 업데이트 요청
# # #             send_db_update_request(db_pusher_socket, loser_ip, "LOSE") # 패자 DB 업데이트 요청
# # #         else: # 무승부
# # #             result_message = "Draw!"
# # #             print("\n게임 종료! 무승부!")
# # #             send_db_update_request(db_pusher_socket, get_ip_by_role("player1"), "DRAW") # P1 무승부 DB 업데이트 요청
# # #             send_db_update_request(db_pusher_socket, get_ip_by_role("player2"), "DRAW") # P2 무승부 DB 업데이트 요청
        
# # #         send_gui_game_result(gui_publisher_socket, result_message)
# # #         reset_game()
# # #         return False

# # #     actions_order.clear()
# # #     action_time.clear()
# # #     return True

# # # def reset_game():
# # #     global players, players_hp, actions_order, action_time
# # #     players = {}
# # #     players_hp = {"player1": 100, "player2": 100}
# # #     actions_order = []
# # #     action_time = {}

# # # def get_ip_by_role(role):
# # #     for ip, name in players.items():
# # #         if name == role:
# # #             return ip
# # #     return None

# # # game_logic.py
# # import time
# # import threading
# # import zmq # ZMQ 임포트

# # players = {}
# # players_hp = {"player1": 100, "player2": 100}
# # # actions_order와 action_time은 이제 실시간 처리되므로 직접적인 버퍼링 역할은 감소합니다.
# # # 하지만 쿨타임 및 특정 액션 간의 상호작용을 위해 여전히 유지될 수 있습니다.
# # actions_order = [] # 이 리스트는 이제 필요 없음. 각 플레이어의 마지막 액션만 관리
# # action_time = {
# #     "player1": 0, # 각 플레이어의 마지막 액션 시간을 기록
# #     "player2": 0
# # }

# # movement_window = 0.1
# # attack_cooldown = 0.5 # 공격 쿨타임 추가 (0.5초)

# # game_started = False 

# # # 기존 송신 함수들은 동일하게 유지
# # def send_gui_state_update(gui_socket, game_state_flag, p1_hp, p2_hp):
# #     msg = f"GAME_STATE_GUI,{game_state_flag},{p1_hp}:{p2_hp}"
# #     gui_socket.send_string(msg)

# # def send_gui_hit_trigger(gui_socket, hit_player_role):
# #     msg = f"HIT_GUI,{hit_player_role}"
# #     gui_socket.send_string(msg)

# # def send_gui_game_result(gui_socket, result_text):
# #     msg = f"GAME_RESULT,{result_text}"
# #     gui_socket.send_string(msg)

# # def send_db_update_request(db_socket, ip, result_type):
# #     msg = f"{ip},{result_type}"
# #     db_socket.send_string(msg)
# #     print(f"[Game Logic] DB Update Request (PUSH) sent: {msg}")

# # # 새로운 액션 처리 함수: process_player_action
# # def process_player_action(player_role, action_type, current_action_time, gui_publisher_socket, db_pusher_socket):
# #     global players, players_hp, action_time, game_started

# #     # 게임이 시작되지 않았다면 액션 무시
# #     if not game_started:
# #         print(f"[{player_role}] 게임 시작 전 액션 수신. 무시: {action_type}")
# #         return True # 게임이 아직 진행 중이라고 판단 (대기 중)

# #     # 쿨타임 체크 (빠른 액션 입력 시나리오에 중요)
# #     # 공격 쿨타임 적용
# #     if action_type == "ATTACK" and (current_action_time - action_time[player_role] < attack_cooldown):
# #         # print(f"[{player_role}] 공격 쿨타임 중. 액션 무시: {action_type}")
# #         return True

# #     # 이동 쿨타임 (필요 시 추가)
# #     # if action_type == "MOVEMENT" and (current_action_time - action_time[player_role] < movement_cooldown):
# #     #     print(f"[{player_role}] 이동 쿨타임 중. 액션 무시: {action_type}")
# #     #     return True

# #     action_time[player_role] = current_action_time # 마지막 액션 시간 업데이트

# #     print(f"[{player_role}] 액션 수신: {action_type}")

# #     opponent_role = "player2" if player_role == "player1" else "player1"

# #     # GUI 액션 트리거
# #     if action_type == "ATTACK":
# #         send_gui_action_trigger(player_role, "ATTACK")
        
# #         # 상대방의 마지막 액션과 비교하여 공격 판정 (회피 로직)
# #         # MOVEMENT 액션 판정: 상대방이 MOVEMENT를 수행했고, 그 MOVEMENT가 공격 타이밍과 근접할 경우
# #         # 실제 구현에서는 MOVEMENT의 지속 시간을 고려해야 합니다. 여기서는 간략화합니다.
        
# #         # 상대방의 마지막 액션이 MOVEMENT였고, 그 MOVEMENT가 일정 시간 내에 발생했다면 회피 판정
# #         # 여기서는 단순히 MOVEMENT가 '지금' 발생했는지 여부를 판정하기 어렵습니다.
# #         # 따라서, MOVEMENT는 상대방의 '회피' 개념보다는 '위치 이동' 개념으로 간주하고,
# #         # ATTACK은 일단 상대방에게 데미지를 주는 것으로 구현합니다.
# #         # 만약 MOVEMENT가 회피의 의미를 갖는다면, 해당 MOVEMENT가 일정 시간 동안 유지되는지 또는
# #         # 상대방의 액션이 감지된 직후에 발생하는지에 대한 복잡한 로직이 필요합니다.
        
# #         # 여기서는 스트리트 파이터처럼 공격이 들어오면 일단 맞는 형태로 구현합니다.
# #         players_hp[opponent_role] -= 10
# #         send_gui_hit_trigger(gui_publisher_socket, opponent_role)
# #         print(f"[{player_role}] ATTACK hit! {opponent_role} HP: {players_hp[opponent_role]}")

# #     elif action_type == "MOVEMENT":
# #         # MOVEMENT에 대한 특정 로직이 있다면 여기에 추가 (예: 위치 변경, 방어력 증가 등)
# #         print(f"[{player_role}] MOVEMENT 액션 수행.")
# #         pass # 현재는 MOVEMENT가 데미지에 직접적인 영향을 주지 않음

# #     # HP는 0 미만으로 내려가지 않도록 보장
# #     for p in ["player1", "player2"]:
# #         players_hp[p] = max(players_hp[p], 0)
    
# #     print(f"Current HP - Player1: {players_hp['player1']}, Player2: {players_hp['player2']}")
# #     send_gui_state_update(gui_publisher_socket, 1, players_hp["player1"], players_hp["player2"])

# #     # 게임 종료 판정
# #     if players_hp["player1"] <= 0 or players_hp["player2"] <= 0:
# #         winner_ip = None
# #         loser_ip = None
# #         result_message = ""

# #         if players_hp["player1"] > players_hp["player2"]: # P1 승리
# #             winner_ip = get_ip_by_role("player1")
# #             loser_ip = get_ip_by_role("player2")
# #             result_message = f"Player1 ({winner_ip}) Wins!"
# #             print(f"\n게임 종료! Player1 승리!")
# #             send_db_update_request(db_pusher_socket, winner_ip, "WIN")
# #             send_db_update_request(db_pusher_socket, loser_ip, "LOSE")
# #         elif players_hp["player2"] > players_hp["player1"]: # P2 승리
# #             winner_ip = get_ip_by_role("player2")
# #             loser_ip = get_ip_by_role("player1")
# #             result_message = f"Player2 ({winner_ip}) Wins!"
# #             print(f"\n게임 종료! Player2 승리!")
# #             send_db_update_request(db_pusher_socket, winner_ip, "WIN")
# #             send_db_update_request(db_pusher_socket, loser_ip, "LOSE")
# #         else: # 무승부
# #             result_message = "Draw!"
# #             print("\n게임 종료! 무승부!")
# #             send_db_update_request(db_pusher_socket, get_ip_by_role("player1"), "DRAW")
# #             send_db_update_request(db_pusher_socket, get_ip_by_role("player2"), "DRAW")
        
# #         send_gui_game_result(gui_publisher_socket, result_message)
# #         reset_game_state_and_players() # 게임 종료 시 모든 상태 초기화
# #         return False # 게임 종료 시 False 반환
    
# #     return True # 게임이 아직 진행 중임을 알림

# # def reset_game_state_and_players():
# #     global players, players_hp, action_time, game_started
# #     players = {} # 플레이어 할당 초기화
# #     players_hp = {"player1": 100, "player2": 100}
# #     action_time = {"player1": 0, "player2": 0} # 액션 시간도 초기화
# #     game_started = False # 게임 상태를 명시적으로 False로 설정
# #     print("[Game Logic] 게임 상태 및 플레이어 정보 초기화 완료.")

# # def get_ip_by_role(role):
# #     for ip, name in players.items():
# #         if name == role:
# #             return ip
# #     return None
# # # game_logic.py - 게임의 핵심 로직을 처리하는 모듈
# # import time
# # import collections # deque 사용을 위해 임포트

# # # --- 전역 변수 ---
# # players = {} # {client_ip: "player1" or "player2"}
# # players_hp = {"player1": 100, "player2": 100}

# # # 각 플레이어의 최근 액션 기록 (액션 타입, 타임스탬프)
# # # 판정 윈도우 내의 액션들을 추적하기 위함
# # # collections.deque를 사용하여 효율적인 삽입/삭제
# # player_actions_history = {
# #     "player1": collections.deque(),
# #     "player2": collections.deque()
# # }

# # # --- 판정 관련 상수 ---
# # PROCESS_WINDOW_SEC = 0.2  # 모든 커맨드에 대한 판정 기준 시간 (0.2초)
# # EVASION_WINDOW_SEC = 0.1  # 공격에 대한 회피/동시 공격 판정 기준 시간 (0.1초)
# # ATTACK_COOLDOWN_SEC = 0.5 # 공격 쿨타임 (0.5초)

# # # 각 플레이어의 마지막 액션 시간 (쿨타운 체크용)
# # last_action_time = {
# #     "player1": 0,
# #     "player2": 0
# # }

# # game_started = False # 게임 시작 여부 플래그

# # # --- ZMQ 메시지 송신 헬퍼 함수 (main.py의 소켓을 통해 전송) ---
# # def send_gui_state_update(gui_socket, game_state_flag, p1_hp, p2_hp):
# #     """GUI에 게임 상태 및 HP 업데이트 메시지를 전송합니다."""
# #     msg = f"GAME_STATE_GUI,{game_state_flag},{p1_hp}:{p2_hp}"
# #     gui_socket.send_string(msg)
# #     # print(f"[Game Logic] GUI State Update sent: {msg}") # 디버깅용

# # def send_gui_hit_trigger(gui_socket, hit_player_role):
# #     """GUI에 피격 애니메이션 트리거 메시지를 전송합니다."""
# #     msg = f"HIT_GUI,{hit_player_role}"
# #     gui_socket.send_string(msg)
# #     # print(f"[Game Logic] GUI Hit Trigger sent: {msg}") # 디버깅용

# # def send_gui_game_result(gui_socket, result_text):
# #     """GUI에 게임 결과 메시지를 전송합니다."""
# #     msg = f"GAME_RESULT,{result_text}"
# #     gui_socket.send_string(msg)
# #     # print(f"[Game Logic] GUI Game Result sent: {msg}") # 디버깅용

# # def send_db_update_request(db_socket, ip, result_type):
# #     """C DB 서비스로 DB 업데이트 요청을 ZMQ PUSH 소켓으로 전송합니다."""
# #     msg = f"{ip},{result_type}"
# #     db_socket.send_string(msg)
# #     print(f"[Game Logic] DB Update Request (PUSH) sent: {msg}")

# # def send_gui_action_trigger(gui_socket, player_role, action_type):
# #     """GUI에 특정 플레이어의 액션 애니메이션 트리거 메시지를 전송합니다."""
# #     msg = f"ACTION_GUI,{player_role},{action_type}"
# #     gui_socket.send_string(msg)
# #     # print(f"[Game Logic] GUI Action Trigger sent: {msg}") # 디버깅용

# # # --- 게임 로직 핵심 함수 ---
# # def process_player_action(player_ip, action_type, current_action_time, gui_publisher_socket, db_pusher_socket):
# #     """
# #     단일 플레이어 액션을 처리하고 게임 상태를 업데이트합니다.
# #     새로운 판정 로직을 포함합니다.
# #     """
# #     global players, players_hp, player_actions_history, last_action_time, game_started

# #     player_role = players.get(player_ip)
# #     if not player_role:
# #         print(f"[Game Logic Error] Unknown IP: {player_ip} tried to perform action {action_type}.")
# #         return True # 게임이 진행 중이라고 가정하고 다음 루프를 기다림

# #     # 게임이 시작되지 않았다면 액션 무시 -> main에서 이미 필터링 함
# #     # if not game_started:
# #     #     print(f"[{player_role}] 게임 시작 전 액션 수신. 무시: {action_type}")
# #     #     return True # 게임이 아직 진행 중이라고 판단 (대기 중)

# #     # 쿨타임 체크 (공격 쿨타임 적용)
# #     if action_type == "ATTACK" and (current_action_time - last_action_time[player_role] < ATTACK_COOLDOWN_SEC):
# #         print(f"[{player_role}] 공격 쿨타임 중. 액션 무시: {action_type}")
# #         return True
    
# #     # 마지막 액션 시간 업데이트
# #     last_action_time[player_role] = current_action_time

# #     print(f"[{player_role}] 액션 수신: {action_type} (Time: {current_action_time:.4f})")

# #     opponent_role = "player2" if player_role == "player1" else "player1"

# #     # --- 액션 기록 및 정리 ---
# #     # 현재 액션 기록 추가
# #     player_actions_history[player_role].append((action_type, current_action_time))
    
# #     # 판정 윈도우 밖의 오래된 액션 기록 정리 (양쪽 플레이어 모두)
# #     for role in ["player1", "player2"]:
# #         while player_actions_history[role] and \
# #               player_actions_history[role][0][1] < current_action_time - PROCESS_WINDOW_SEC:
# #             player_actions_history[role].popleft()

# #     # --- 판정 로직 ---
# #     if action_type == "ATTACK":
# #         send_gui_action_trigger(gui_publisher_socket, player_role, "ATTACK") # 공격 애니메이션 즉시 트리거

# #         # 1. 상대방의 회피 (MOVEMENT) 체크
# #         evaded = False
# #         for op_action, op_time in list(player_actions_history[opponent_role]): # 리스트로 복사하여 순회 중 변경 방지
# #             if op_action == "MOVEMENT" and \
# #                abs(current_action_time - op_time) <= EVASION_WINDOW_SEC:
# #                 print(f"[{opponent_role}] MOVEMENT! [{player_role}]의 ATTACK을 회피했습니다. (공격 시간: {current_action_time:.4f}, 회피 시간: {op_time:.4f})")
# #                 send_gui_action_trigger(gui_publisher_socket, opponent_role, "MOVEMENT") # 회피 애니메이션 트리거
# #                 evaded = True
# #                 break # 회피 성공 시 더 이상 체크할 필요 없음

# #         if evaded:
# #             # 회피 성공했으므로 HP 감소 없음
# #             pass 
# #         else:
# #             # 2. 상대방의 동시 공격 (ATTACK) 체크
# #             opponent_attack_found = False
# #             for op_action, op_time in list(player_actions_history[opponent_role]):
# #                 if op_action == "ATTACK" and \
# #                    abs(current_action_time - op_time) <= EVASION_WINDOW_SEC:
# #                     opponent_attack_found = True
# #                     # 동시 공격 발생: 누가 먼저 공격했는지 판정
# #                     if current_action_time < op_time: # 현재 플레이어가 먼저 공격
# #                         print(f"[{player_role}] ATTACK 성공! [{opponent_role}]의 공격보다 빠릅니다. (본인: {current_action_time:.4f}, 상대: {op_time:.4f})")
# #                         players_hp[opponent_role] -= 10
# #                         send_gui_hit_trigger(gui_publisher_socket, opponent_role)
# #                         break # 공격 성공했으므로 더 이상 체크할 필요 없음
# #                     else: # 상대방이 먼저 공격했거나 거의 동시 (상대방 공격이 우선)
# #                         print(f"[{player_role}]의 ATTACK은 무시됩니다. [{opponent_role}]이(가) 먼저 공격했습니다. (본인: {current_action_time:.4f}, 상대: {op_time:.4f})")
# #                         # 상대방의 공격은 이미 main.py에서 처리되었거나 곧 처리될 것임
# #                         # 여기서는 현재 플레이어의 공격만 무시하고 종료
# #                         break # 공격 무시했으므로 더 이상 체크할 필요 없음
            
# #             if not opponent_attack_found:
# #                 # 3. 일반 공격 성공 (회피도 없고 동시 공격도 아님)
# #                 print(f"[{player_role}] ATTACK 성공! {opponent_role} HP: {players_hp[opponent_role]}")
# #                 players_hp[opponent_role] -= 10
# #                 send_gui_hit_trigger(gui_publisher_socket, opponent_role)

# #     elif action_type == "MOVEMENT":
# #         send_gui_action_trigger(gui_publisher_socket, player_role, "MOVEMENT") # 이동 애니메이션 트리거
# #         print(f"[{player_role}] MOVEMENT 액션 수행.")
# #         # MOVEMENT 자체는 HP 변화 없음. 회피 판정에서만 영향

# #     # HP는 0 미만으로 내려가지 않도록 보장
# #     for p in ["player1", "player2"]:
# #         players_hp[p] = max(players_hp[p], 0)
    
# #     print(f"Current HP - Player1: {players_hp['player1']}, Player2: {players_hp['player2']}")
# #     send_gui_state_update(gui_publisher_socket, 1, players_hp["player1"], players_hp["player2"])

# #     # --- 게임 종료 판정 ---
# #     if players_hp["player1"] <= 0 or players_hp["player2"] <= 0:
# #         winner_ip = None
# #         loser_ip = None
# #         result_message = ""

# #         if players_hp["player1"] > players_hp["player2"]: # P1 승리
# #             winner_ip = get_ip_by_role("player1")
# #             loser_ip = get_ip_by_role("player2")
# #             result_message = f"Player1 ({winner_ip}) Wins!"
# #             print(f"\n게임 종료! Player1 승리!")
# #             send_db_update_request(db_pusher_socket, winner_ip, "WIN")
# #             send_db_update_request(db_pusher_socket, loser_ip, "LOSE")
# #         elif players_hp["player2"] > players_hp["player1"]: # P2 승리
# #             winner_ip = get_ip_by_role("player2")
# #             loser_ip = get_ip_by_role("player1")
# #             result_message = f"Player2 ({winner_ip}) Wins!"
# #             print(f"\n게임 종료! Player2 승리!")
# #             send_db_update_request(db_pusher_socket, winner_ip, "WIN")
# #             send_db_update_request(db_pusher_socket, loser_ip, "LOSE")
# #         else: # 무승부
# #             result_message = "Draw!"
# #             print("\n게임 종료! 무승부!")
# #             send_db_update_request(db_pusher_socket, get_ip_by_role("player1"), "DRAW")
# #             send_db_update_request(db_pusher_socket, get_ip_by_role("player2"), "DRAW")
        
# #         send_gui_game_result(gui_publisher_socket, result_message)
# #         reset_game_state_and_players() # 게임 종료 시 모든 상태 초기화
# #         return False # 게임 종료 시 False 반환
    
# #     return True # 게임이 아직 진행 중임을 알림

# # # --- 게임 상태 관리 헬퍼 함수 ---
# # def reset_game_state_and_players():
# #     """게임 상태 및 플레이어 정보를 초기화합니다."""
# #     global players, players_hp, player_actions_history, last_action_time, game_started
# #     players = {} # 플레이어 할당 초기화
# #     players_hp = {"player1": 100, "player2": 100}
# #     player_actions_history = { # 액션 기록 초기화
# #         "player1": collections.deque(),
# #         "player2": collections.deque()
# #     }
# #     last_action_time = {"player1": 0, "player2": 0} # 마지막 액션 시간도 초기화
# #     game_started = False # 게임 상태를 명시적으로 False로 설정
# #     print("[Game Logic] 게임 상태 및 플레이어 정보 초기화 완료.")

# # def get_ip_by_role(role):
# #     """역할에 해당하는 플레이어의 IP 주소를 반환합니다."""
# #     for ip, name in players.items():
# #         if name == role:
# #             return ip
# #     return None

# #############################################################################270~475

# import time
# import gui # gui 모듈 임포트

# # --- 전역 게임 상태 변수 ---
# game_started = False
# players = {} # IP: player_role (e.g., "192.168.0.100": "player1")
# players_hp = {"player1": 100, "player2": 100}
# last_attack_time = {"player1": 0, "player2": 0}
# attack_cooldown = 1.0 # 공격 쿨타임 1초

# # --- 게임 로직 함수 ---

# # GUI 업데이트 함수 (이제 ZMQ를 통해 보내지 않고 gui 모듈의 함수를 직접 호출)
# # main.py에서 gui_publisher_socket을 인자로 넘기지 않으므로, 이 함수는 필요 없음
# # def send_gui_state_update(gui_publisher_socket, state, p1_hp, p2_hp):
# #     msg = f"GAME_STATE_GUI,{state},{p1_hp}:{p2_hp}"
# #     gui_publisher_socket.send_string(msg)

# def process_player_action(player_ip, action_type, current_time, db_pusher_socket):
#     global game_started
    
#     player_role = players.get(player_ip)

#     if not player_role:
#         print(f"[Game Logic Error] Unknown IP: {player_ip} tried to perform action {action_type}.")
#         return True # 게임이 진행 중이라고 가정하고 다음 루프를 기다림

#     # 게임이 시작되지 않았다면 액션 무시 -> main에서 이미 필터링 함. 이 부분 주석처리
#     # if not game_started:
#     #     print(f"[{player_role}] 게임 시작 전 액션 수신. 무시: {action_type}")
#     #     return True # 게임이 아직 진행 중이라고 판단 (대기 중)


#     # --- 액션 처리 ---
#     if action_type == "ATTACK":
#         if (current_time - last_attack_time[player_role]) >= attack_cooldown:
#             last_attack_time[player_role] = current_time
#             print(f"[{player_role}] 공격! (HP: P1:{players_hp['player1']}, P2:{players_hp['player2']})")
            
#             # GUI에 공격 애니메이션 요청
#             gui.trigger_action_animation(player_role, "ATTACK")

#             # 상대방에게 피해 주기
#             target_player_role = "player2" if player_role == "player1" else "player1"
#             damage = 10 # 기본 데미지
#             players_hp[target_player_role] -= damage
#             print(f"[{target_player_role}] 피격! 남은 HP: {players_hp[target_player_role]}")
            
#             # GUI에 피격 애니메이션 요청
#             gui.trigger_hit_animation(target_player_role)
            
#             # GUI에 HP 업데이트 요청
#             gui.update_hp(players_hp["player1"], players_hp["player2"])

#             # 게임 종료 판정
#             if players_hp[target_player_role] <= 0:
#                 winner = player_role # 공격자가 승리
#                 print(f"\n--- 게임 종료! 승자: {winner} ---")
                
#                 # GUI에 게임 결과 전송
#                 gui.set_game_result(f"Winner: {winner}")
                
#                 # DB에 게임 결과 저장
#                 db_pusher_socket.send_string(f"GAME_RESULT,{winner},{players_hp['player1']},{players_hp['player2']}")
                
#                 # 게임 상태 초기화
#                 game_started = False
#                 players.clear()
#                 players_hp["player1"] = 100
#                 players_hp["player2"] = 100
#                 last_attack_time["player1"] = 0
#                 last_attack_time["player2"] = 0

#                 return False # 게임 종료 신호
#         else:
#             print(f"[{player_role}] 공격 쿨타임 ({attack_cooldown}초) 중. 남은 시간: {attack_cooldown - (current_time - last_attack_time[player_role]):.2f}초")

#     elif action_type == "MOVEMENT":
#         print(f"[{player_role}] 이동!")
#         # GUI에 이동 애니메이션 요청
#         gui.trigger_action_animation(player_role, "MOVEMENT")

#     else:
#         print(f"[{player_role}] 알 수 없는 액션: {action_type}")
    
#     # 현재 HP 상태를 GUI에 주기적으로 업데이트
#     gui.update_hp(players_hp["player1"], players_hp["player2"])

#     return True # 게임 계속 진행 신호 (게임 종료 시 False 반환)
import time
import gui # gui 모듈 임포트

# --- 전역 게임 상태 변수 ---
game_started = False
players = {} # IP: player_role (e.g., "192.168.0.100": "player1")
players_hp = {"player1": 100, "player2": 100}
last_attack_time = {"player1": 0, "player2": 0}
attack_cooldown = 1.0 # 공격 쿨타임 1초

# --- 게임 로직 함수 ---

def process_player_action(player_ip, action_type, current_time, db_pusher_socket):
    global game_started
    
    player_role = players.get(player_ip)

    if not player_role:
        print(f"[Game Logic Error] Unknown IP: {player_ip} tried to perform action {action_type}.")
        return True # 게임이 진행 중이라고 가정하고 다음 루프를 기다림

    # --- 액션 처리 ---
    if action_type == "ATTACK":
        if (current_time - last_attack_time[player_role]) >= attack_cooldown:
            last_attack_time[player_role] = current_time
            print(f"[{player_role}] 공격! (HP: P1:{players_hp['player1']}, P2:{players_hp['player2']})")
            
            # GUI에 공격 애니메이션 요청
            gui.trigger_action_animation(player_role, "ATTACK")

            # 상대방에게 피해 주기
            target_player_role = "player2" if player_role == "player1" else "player1"
            damage = 10 # 기본 데미지
            players_hp[target_player_role] -= damage
            print(f"[{target_player_role}] 피격! 남은 HP: {players_hp[target_player_role]}")
            
            # GUI에 피격 애니메이션 요청
            gui.trigger_hit_animation(target_player_role)
            
            # GUI에 HP 업데이트 요청
            gui.update_hp(players_hp["player1"], players_hp["player2"])

            # 게임 종료 판정
            if players_hp[target_player_role] <= 0:
                winner = player_role # 공격자가 승리
                print(f"\n--- 게임 종료! 승자: {winner} ---")
                
                # GUI에 게임 결과 전송
                gui.show_game_result(f"Winner: {winner}") # gui.set_game_result 대신 show_game_result 호출
                
                # DB에 게임 결과 저장
                db_pusher_socket.send_string(f"GAME_RESULT,{winner},{players_hp['player1']},{players_hp['player2']}")
                
                # 게임 상태 초기화 (main.py에서 더 포괄적으로 처리할 것이므로, 여기서 game_started만 False로 변경)
                game_started = False 

                return False # 게임 종료 신호
        else:
            print(f"[{player_role}] 공격 쿨타임 ({attack_cooldown}초) 중. 남은 시간: {attack_cooldown - (current_time - last_attack_time[player_role]):.2f}초")

    elif action_type == "MOVEMENT":
        print(f"[{player_role}] 이동!")
        # GUI에 이동 애니메이션 요청
        gui.trigger_action_animation(player_role, "MOVEMENT")

    else:
        print(f"[{player_role}] 알 수 없는 액션: {action_type}")
    
    # 현재 HP 상태를 GUI에 주기적으로 업데이트
    gui.update_hp(players_hp["player1"], players_hp["player2"])

    return True # 게임 계속 진행 신호 (게임 종료 시 False 반환)
