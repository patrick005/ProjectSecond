# # # import time
# # # import zmq
# # # from zmq_handler import setup_subscriber
# # # from game_logic import * # game_logic 모듈 임포트

# # # context = zmq.Context()

# # # # relay_server.py로 게임 상태 플래그 발행 (PUB)
# # # flag_publisher_socket = context.socket(zmq.PUB)
# # # flag_publisher_socket.bind(f"tcp://*:6001") # relay_server.py의 ZMQ_SUB_PORT_FOR_FLAGS와 일치

# # # # gui.py로 GUI 상태 발행 (PUB)
# # # gui_publisher_socket = context.socket(zmq.PUB)
# # # gui_publisher_socket.bind(f"tcp://*:6002") # gui.py가 구독할 포트 (GUI_SUB_PORT)

# # # # C DB 서비스로 DB 업데이트 요청 전송 (PUSH)
# # # db_pusher_socket = context.socket(zmq.PUSH)
# # # db_pusher_socket.connect(f"tcp://localhost:6003") # C DB 서비스가 PULL할 포트 (ZMQ_DB_PULL_PORT)

# # # # relay_server.py로부터 클라이언트 액션 수신 (SUB)
# # # sub_socket = setup_subscriber() # zmq_handler.py에서 SUB 소켓 설정

# # # print("ZMQ 게임 서버 시작 - 메시지 대기 중...")
# # # print(f"게임 상태 플래그 발행 준비 완료 (tcp://*:6001)")
# # # print(f"GUI 상태 발행 준비 완료 (tcp://*:6002)")
# # # print(f"C DB 서비스로 요청 전송 준비 완료 (tcp://localhost:6003)")

# # # def send_game_flag_to_relay_server(flag):
# # #     """
# # #     ZMQ PUB 소켓을 통해 게임 상태 플래그를 relay_server.py로 발행합니다.
# # #     relay_server.py는 이 플래그를 받아 TCP로 클라이언트에게 전송합니다.
# # #     @param flag: 전송할 게임 상태 플래그 (0: 대기, 1: 진행)
# # #     """
# # #     flag_publisher_socket.send_string(f"GAME_STATE,{flag}")
# # #     print(f"[Main] Game flag {flag} published to relay server via ZMQ.")

# # # def send_gui_state_update(game_state_flag, p1_hp, p2_hp):
# # #     """
# # #     GUI에 게임 상태 및 HP 정보를 업데이트하기 위해 ZMQ PUB 소켓으로 메시지를 발행합니다.
# # #     @param game_state_flag: 게임 상태 (0: 대기/초기화, 1: 진행)
# # #     @param p1_hp: Player1의 현재 HP
# # #     @param p2_hp: Player2의 현재 HP
# # #     """
# # #     msg = f"GAME_STATE_GUI,{game_state_flag},{p1_hp}:{p2_hp}"
# # #     gui_publisher_socket.send_string(msg)

# # # def send_gui_action_trigger(player_role, action_type):
# # #     """
# # #     GUI에 특정 플레이어의 액션(예: 공격) 애니메이션을 트리거하도록 ZMQ PUB 소켓으로 메시지를 발행합니다.
# # #     @param player_role: 액션을 수행한 플레이어 (예: "player1")
# # #     @param action_type: 액션의 종류 (예: "ATTACK")
# # #     """
# # #     msg = f"ACTION_GUI,{player_role},{action_type}"
# # #     gui_publisher_socket.send_string(msg)
# # #     print(f"[Main] GUI Action Trigger published: {msg}")

# # # def send_gui_hit_trigger(hit_player_role):
# # #     """
# # #     GUI에 특정 플레이어가 피격 애니메이션을 트리거하도록 ZMQ PUB 소켓으로 메시지를 발행합니다.
# # #     @param hit_player_role: 피격당한 플레이어 (예: "player1")
# # #     """
# # #     msg = f"HIT_GUI,{hit_player_role}"
# # #     gui_publisher_socket.send_string(msg)
# # #     print(f"[Main] GUI Hit Trigger published: {msg}")

# # # def send_gui_game_result(result_text):
# # #     """
# # #     GUI에 게임 최종 결과를 전송합니다.
# # #     @param result_text: 게임 결과 메시지 (예: "Player1 Wins!", "Draw!")
# # #     """
# # #     msg = f"GAME_RESULT,{result_text}"
# # #     gui_publisher_socket.send_string(msg)
# # #     print(f"[Main] GUI Game Result published: {msg}")

# # # def send_db_update_request(ip, result_type):
# # #     """
# # #     C DB 서비스로 DB 업데이트 요청을 ZMQ PUSH 소켓으로 전송합니다.
# # #     @param ip: 클라이언트 IP 주소
# # #     @param result_type: "WIN", "LOSE", "DRAW" 중 하나
# # #     """
# # #     msg = f"{ip},{result_type}" # "IP,RESULT_TYPE" 형식
# # #     db_pusher_socket.send_string(msg)
# # #     print(f"[Main] DB Update Request (PUSH) sent: {msg}")


# # # # 초기 게임 상태 전송 (GUI 대기 상태)
# # # send_game_flag_to_relay_server(0)
# # # send_gui_state_update(0, players_hp["player1"], players_hp["player2"])


# # # while True:
# # #     try:
# # #         msg = sub_socket.recv_string(zmq.DONTWAIT)
# # #     except zmq.Again:
# # #         # 메시지가 없을 때도 GUI는 계속 업데이트되어야 함 (애니메이션 등)
# # #         send_gui_state_update(game_started, players_hp["player1"], players_hp["player2"])
# # #         time.sleep(0.01) # 짧은 지연
# # #         continue

# # #     parts = msg.split(',')

# # #     if len(parts) != 2:
# # #         print(f"잘못된 ZMQ 메시지 포맷: {msg}")
# # #         continue

# # #     ip = parts[0].strip()
# # #     action = parts[1].strip().upper() # 액션을 대문자로 변환

# # #     # 플레이어 할당 로직
# # #     if ip not in players:
# # #         if "player1" not in players.values():
# # #             players[ip] = "player1"
# # #             print(f"[{ip}] 할당: player1")
# # #         elif "player2" not in players.values():
# # #             players[ip] = "player2"
# # #             print(f"[{ip}] 할당: player2")
# # #         else:
# # #             print(f"[{ip}] 접속 시도: 플레이어 슬롯이 모두 찼습니다.")
# # #             continue

# # #     # 게임 시작 조건 확인 및 플래그 전송
# # #     if not game_started and len(players) == 2:
# # #         print("\n게임 시작!")
# # #         game_started = True
# # #         send_game_flag_to_relay_server(1) # 클라이언트에게 1 (게임 중) 전송
# # #         send_gui_state_update(1, players_hp["player1"], players_hp["player2"])
# # #         # 게임 시작 후 첫 라운드 시작 전 짧은 대기 (선택 사항)
# # #         time.sleep(0.5) 

# # #     # 게임 시작 여부에 따라 액션 처리 로직 변경
# # #     if not game_started: # 게임 대기 중 (두 플레이어가 모두 접속하기 전)
# # #         if action == "ACCEPT":
# # #             # print(f"[{players.get(ip, 'Unknown')}] 게임 대기 중 ACCEPT 수신.")
# # #             pass # ACCEPT 메시지는 게임 시작 전에는 단순히 클라이언트의 존재를 알리는 용도로 무시
# # #         else:
# # #             print(f"[{players.get(ip, 'Unknown')}] 게임 시작 전 '{action}' 액션 수신. (무시)")
# # #         continue # 게임 시작 전에는 다음 메시지를 대기

# # #     # 게임이 시작되었고 해당 IP가 등록된 플레이어인 경우에만 액션 처리
# # #     if game_started and ip in players:
# # #         player = players[ip]

# # #         # 유효한 게임 진행 액션만 처리
# # #         if action not in ["ATTACK", "MOVEMENT"]:
# # #             print(f"[{player}] 유효하지 않은 게임 진행 액션입니다. 무시: {action}")
# # #             continue

# # #         # 이미 해당 라운드에서 액션을 보냈는지 확인
# # #         if any(entry[0] == player for entry in actions_order):
# # #             # print(f"[{player}] 이미 액션을 보냈습니다. 무시: {action}")
# # #             continue

# # #         actions_order.append((player, action))
# # #         action_time[player] = time.time()

# # #         print(f"[{player}] 액션 수신: {action}")

# # #         # GUI 액션 트리거
# # #         if action == "ATTACK":
# # #             send_gui_action_trigger(player, "ATTACK")
# # #         # MOVEMENT에 대한 GUI 액션이 있다면 여기에 추가

# # #         # 두 플레이어 모두 액션을 보냈을 때 라운드 처리
# # #         if len(actions_order) == 2:
# # #             game_active_after_round = process_round(gui_publisher_socket, db_pusher_socket)

# # #             # 게임이 종료된 경우
# # #             if not game_active_after_round: # process_round에서 False를 반환 (게임 종료)
# # #                 game_started = False # 메인 스크립트의 game_started 플래그를 False로 설정
# # #                 send_game_flag_to_relay_server(0) # 클라이언트에게 0 (대기) 전송
# # #                 # GUI에는 최종 HP와 함께 0 (대기) 상태를 전송하여 초기화된 HP를 보여주고 대기 메시지를 표시
# # #                 send_gui_state_update(0, players_hp["player1"], players_hp["player2"])
# # #                 print("게임이 종료되었습니다. 새로운 게임을 기다립니다.")

# # # main.py
# # import time
# # import zmq
# # from zmq_handler import setup_subscriber
# # from game_logic import * # game_logic 모듈 임포트

# # context = zmq.Context()

# # # ZMQ PUB/PUSH 소켓 설정 (기존과 동일)
# # flag_publisher_socket = context.socket(zmq.PUB)
# # flag_publisher_socket.bind(f"tcp://*:6001")

# # gui_publisher_socket = context.socket(zmq.PUB)
# # gui_publisher_socket.bind(f"tcp://*:6002")

# # db_pusher_socket = context.socket(zmq.PUSH)
# # db_pusher_socket.connect(f"tcp://localhost:6003")

# # # relay_server.py로부터 클라이언트 액션 수신 (SUB) (기존과 동일)
# # sub_socket = setup_subscriber()

# # print("ZMQ 게임 서버 시작 - 메시지 대기 중...")
# # print(f"게임 상태 플래그 발행 준비 완료 (tcp://*:6001)")
# # print(f"GUI 상태 발행 준비 완료 (tcp://*:6002)")
# # print(f"C DB 서비스로 요청 전송 준비 완료 (tcp://localhost:6003)")

# # # 초기 게임 상태 전송 (GUI 대기 상태)
# # send_game_flag_to_relay_server(0) # 0: 게임 대기
# # send_gui_state_update(gui_publisher_socket, 0, players_hp["player1"], players_hp["player2"])


# # while True:
# #     try:
# #         msg = sub_socket.recv_string(zmq.DONTWAIT)
# #     except zmq.Again:
# #         # 메시지가 없을 때도 GUI는 계속 업데이트되어야 함 (애니메이션 등)
# #         send_gui_state_update(gui_publisher_socket, 1 if game_started else 0, players_hp["player1"], players_hp["player2"])
# #         time.sleep(0.01) # 짧은 지연
# #         continue

# #     parts = msg.split(',')

# #     if len(parts) != 2:
# #         print(f"잘못된 ZMQ 메시지 포맷: {msg}")
# #         continue

# #     ip = parts[0].strip()
# #     action = parts[1].strip().upper() # 액션을 대문자로 변환

# #     # 플레이어 할당 로직
# #     # game_started가 False일 때만 새로운 플레이어 할당을 시도
# #     if not game_started and ip not in players:
# #         if "player1" not in players.values():
# #             players[ip] = "player1"
# #             print(f"[{ip}] 할당: player1")
# #         elif "player2" not in players.values():
# #             players[ip] = "player2"
# #             print(f"[{ip}] 할당: player2")
# #         else:
# #             print(f"[{ip}] 접속 시도: 플레이어 슬롯이 모두 찼습니다. (게임 대기 중)")
# #             send_game_flag_to_relay_server(0) 
# #             continue
# #     elif game_started and ip not in players:
# #         # 게임이 이미 시작되었는데 새로운 IP가 접속 시도할 경우
# #         print(f"[{ip}] 접속 시도: 게임이 이미 시작되었습니다. (액션 무시)")
# #         send_game_flag_to_relay_server(1) # 게임 진행 중 플래그 전송 (클라이언트 동기화)
# #         continue

# #     # 게임 시작 조건 확인 및 플래그 전송
# #     # 두 플레이어가 모두 접속하고 game_started가 False일 때만 게임 시작
# #     if not game_started and len(players) == 2:
# #         print("\n게임 시작!")
# #         game_started = True
# #         send_game_flag_to_relay_server(1) # 클라이언트에게 1 (게임 중) 전송
# #         send_gui_state_update(gui_publisher_socket, 1, players_hp["player1"], players_hp["player2"])
# #         time.sleep(0.5) # 게임 시작 후 짧은 대기 (선택 사항)
# #         continue # 게임 시작 메시지 전송 후 다음 루프에서 액션 처리 시작

# #     # 게임 시작 여부에 따라 액션 처리 로직 변경
# #     if not game_started: # 게임 대기 중 (두 플레이어가 모두 접속하기 전 또는 게임 종료 후 초기화된 상태)
# #         if action == "ACCEPT":
# #             pass # ACCEPT 메시지는 게임 시작 전에는 단순히 클라이언트의 존재를 알리는 용도로 무시
# #         else:
# #             print(f"[{players.get(ip, 'Unknown')}] 게임 시작 전 '{action}' 액션 수신. (무시)")
# #         continue 

# #     # 게임이 시작되었고 해당 IP가 등록된 플레이어인 경우에만 액션 처리
# #     if game_started and ip in players:
# #         player_role = players[ip]
# #         current_time = time.time()

# #         # 새로운 액션 처리 함수 호출
# #         game_active_after_action = process_player_action(player_role, action, current_time, gui_publisher_socket, db_pusher_socket)

# #         # 게임이 종료된 경우 (game_logic에서 game_started가 False로 초기화됨)
# #         if not game_active_after_action: 
# #             send_game_flag_to_relay_server(0) 
# #             send_gui_state_update(gui_publisher_socket, 0, players_hp["player1"], players_hp["player2"])
# #             print("게임이 종료되었습니다. 새로운 게임을 기다립니다.")
# # # main.py
# # import time
# # import zmq
# # from zmq_handler import setup_subscriber
# # from game_logic import * # game_logic 모듈 임포트 (모든 함수와 변수 임포트)

# # # --- ZMQ 컨텍스트 및 소켓 설정 ---
# # context = zmq.Context()

# # # 게임 상태 플래그를 relay_server.py로 발행하는 PUB 소켓
# # flag_publisher_socket = context.socket(zmq.PUB)
# # flag_publisher_socket.bind(f"tcp://*:6001")

# # # GUI로 게임 상태, 액션, 결과 등을 발행하는 PUB 소켓
# # gui_publisher_socket = context.socket(zmq.PUB)
# # gui_publisher_socket.bind(f"tcp://*:6002")

# # # DB_manager.c로 게임 결과를 PUSH하는 소켓
# # db_pusher_socket = context.socket(zmq.PUSH)
# # db_pusher_socket.connect(f"tcp://localhost:6003")

# # # relay_server.py로부터 클라이언트 액션을 수신하는 SUB 소켓
# # sub_socket = setup_subscriber()

# # print("ZMQ 게임 서버 시작 - 메시지 대기 중...")
# # print(f"게임 상태 플래그 발행 준비 완료 (tcp://*:6001)")
# # print(f"GUI 상태 발행 준비 완료 (tcp://*:6002)")
# # print(f"C DB 서비스로 요청 전송 준비 완료 (tcp://localhost:6003)")

# # # --- 초기 게임 상태 전송 (GUI 및 클라이언트 대기 상태) ---
# # # relay_server.py로 게임 대기 플래그 전송
# # # game_logic.py의 send_game_flag_to_relay_server 함수가 없으므로 직접 전송
# # flag_publisher_socket.send_string("GAME_STATE,0") 
# # # GUI에 초기 HP 및 대기 상태 전송
# # send_gui_state_update(gui_publisher_socket, 0, players_hp["player1"], players_hp["player2"])


# # # --- 메인 게임 루프 ---
# # while True:
# #     try:
# #         # ZMQ 메시지를 논블로킹 방식으로 수신
# #         msg = sub_socket.recv_string(zmq.DONTWAIT)
# #         current_time = time.time() # 메시지 수신 즉시 정확한 타임스탬프 기록
# #     except zmq.Again:
# #         # 메시지가 없을 때도 GUI는 계속 업데이트되어야 함 (애니메이션 등)
# #         # 게임이 시작되었으면 1, 아니면 0 상태로 GUI 업데이트
# #         send_gui_state_update(gui_publisher_socket, 1 if game_started else 0, players_hp["player1"], players_hp["player2"])
# #         time.sleep(0.01) # 짧은 지연으로 CPU 사용률 관리
# #         continue # 다음 루프 반복

# #     parts = msg.split(',')

# #     if len(parts) != 2:
# #         print(f"잘못된 ZMQ 메시지 포맷: {msg}")
# #         continue

# #     ip = parts[0].strip()
# #     action = parts[1].strip().upper() # 액션을 대문자로 변환

# #     # --- 플레이어 할당 로직 ---
# #     # game_started가 False일 때만 새로운 플레이어 할당을 시도
# #     if not game_started:
# #         if ip not in players: # 새로운 IP라면 할당 시도
# #             if "player1" not in players.values():
# #                 players[ip] = "player1"
# #                 print(f"[{ip}] 할당: player1")
# #             elif "player2" not in players.values():
# #                 players[ip] = "player2"
# #                 print(f"[{ip}] 할당: player2")
# #             else:
# #                 print(f"[{ip}] 접속 시도: 플레이어 슬롯이 모두 찼습니다. (게임 대기 중)")
# #                 # 슬롯이 찼지만 게임 시작 전이므로 대기 플래그 유지
# #                 flag_publisher_socket.send_string("GAME_STATE,0") 
# #                 continue # 다음 메시지 대기
        
# #         # 게임 시작 조건 확인 및 플래그 전송
# #         # 두 플레이어가 모두 접속하고 game_started가 False일 때만 게임 시작
# #         if len(players) == 2:
# #             print("\n게임 시작!")
# #             game_started = True
# #             flag_publisher_socket.send_string("GAME_STATE,1") # 클라이언트에게 1 (게임 중) 전송
# #             send_gui_state_update(gui_publisher_socket, 1, players_hp["player1"], players_hp["player2"])
# #             time.sleep(0.5) # 게임 시작 후 짧은 대기 (선택 사항)
# #             continue # 게임 시작 메시지 전송 후 다음 루프에서 액션 처리 시작
# #         else: # 아직 플레이어 할당 중이거나 한 명만 접속한 상태
# #             if action == "ACCEPT":
# #                 pass # ACCEPT 메시지는 게임 시작 전에는 단순히 클라이언트의 존재를 알리는 용도로 무시
# #             else:
# #                 print(f"[{players.get(ip, 'Unknown')}] 게임 시작 전 '{action}' 액션 수신. (무시)")
# #             continue # 게임 시작 전에는 액션 처리하지 않고 다음 메시지 대기
    
# #     # --- 게임이 시작되었고, 해당 IP가 등록된 플레이어인 경우에만 액션 처리 ---
# #     if game_started and ip in players:
# #         # 게임 로직 모듈의 액션 처리 함수 호출
# #         # gui_publisher_socket과 db_pusher_socket을 인자로 전달
# #         game_active_after_action = process_player_action(ip, action, current_time, gui_publisher_socket, db_pusher_socket)

# #         # 게임이 종료된 경우 (game_logic에서 game_started가 False로 초기화됨)
# #         if not game_active_after_action: 
# #             flag_publisher_socket.send_string("GAME_STATE,0") # 클라이언트에게 0 (게임 대기) 전송
# #             send_gui_state_update(gui_publisher_socket, 0, players_hp["player1"], players_hp["player2"])
# #             print("게임이 종료되었습니다. 새로운 게임을 기다립니다.")

# #     elif game_started and ip not in players:
# #         # 게임이 이미 시작되었는데 등록되지 않은 IP가 접속 시도할 경우
# #         print(f"[{ip}] 접속 시도: 게임이 이미 시작되었습니다. (액션 무시)")
# #         flag_publisher_socket.send_string("GAME_STATE,1") # 게임 진행 중 플래그 전송 (클라이언트 동기화)

# ####################################################274~380

# import time
# import zmq
# from zmq_handler import setup_subscriber
# import game_logic # game_logic 모듈 전체 임포트
# import gui # gui 모듈 전체 임포트

# # --- ZMQ 컨텍스트 및 소켓 설정 ---
# context = zmq.Context()

# # 게임 상태 플래그를 relay_server.py로 발행하는 PUB 소켓
# flag_publisher_socket = context.socket(zmq.PUB)
# flag_publisher_socket.bind(f"tcp://*:6001")

# # GUI로 게임 상태, 액션, 결과 등을 발행하는 PUB 소켓 (이제 main.py에서 직접 사용하지 않음)
# # gui_publisher_socket = context.socket(zmq.PUB)
# # gui_publisher_socket.bind(f"tcp://*:6002")
# # print(f"GUI 상태 발행 준비 완료 (tcp://*:6002)") # 이 라인도 제거

# # DB_manager.c로 게임 결과를 PUSH하는 소켓
# db_pusher_socket = context.socket(zmq.PUSH)
# db_pusher_socket.connect(f"tcp://localhost:6003")

# # relay_server.py로부터 클라이언트 액션을 수신하는 SUB 소켓
# sub_socket = setup_subscriber()

# print("ZMQ 게임 서버 시작 - 메시지 대기 중...")
# print(f"게임 상태 플래그 발행 준비 완료 (tcp://*:6001)")
# print(f"C DB 서비스로 요청 전송 준비 완료 (tcp://localhost:6003)")

# # --- 초기 게임 상태 전송 (GUI 및 클라이언트 대기 상태) ---
# flag_publisher_socket.send_string("GAME_STATE,0")
# # GUI에 초기 HP 및 대기 상태 전송 (이제 game_logic에서 직접 gui를 호출하므로 main에서는 제거)
# # game_logic.send_gui_state_update(gui_publisher_socket, 0, game_logic.players_hp["player1"], game_logic.players_hp["player2"])
# gui.update_hp(game_logic.players_hp["player1"], game_logic.players_hp["player2"])
# gui.set_game_state(0) # GUI를 대기 상태로 설정


# # --- 메인 게임 루프 ---
# gui_running = True # GUI 루프를 제어할 플래그
# while gui_running: # GUI가 종료되면 main 루프도 종료
#     try:
#         # ZMQ 메시지를 논블로킹 방식으로 수신
#         msg = sub_socket.recv_string(zmq.DONTWAIT)
#         current_time = time.time() # 메시지 수신 즉시 정확한 타임스탬프 기록
#     except zmq.Again:
#         # 메시지가 없을 때도 GUI는 계속 업데이트되어야 함 (애니메이션 등)
#         # 게임이 시작되었으면 1, 아니면 0 상태로 GUI 업데이트 (이제 game_logic에서 직접 gui를 호출)
#         # gui.update_hp(game_logic.players_hp["player1"], game_logic.players_hp["player2"]) # GUI HP 업데이트는 액션 발생 시, 또는 주기적으로 main에서 직접 호출
        
#         # GUI 프레임 업데이트 호출
#         gui_running = gui.run_gui_frame() # gui.run_gui_frame()이 False를 반환하면 종료
#         if not gui_running: # GUI 종료 신호가 오면 break
#             break 

#         time.sleep(0.01) # 짧은 지연으로 CPU 사용률 관리
#         continue # 다음 루프 반복

#     parts = msg.split(',')

#     if len(parts) != 2:
#         print(f"잘못된 ZMQ 메시지 포맷: {msg}")
#         # GUI 프레임 업데이트 호출 (오류 발생 시에도 GUI는 계속 동작)
#         gui_running = gui.run_gui_frame()
#         if not gui_running: break
#         continue

#     ip = parts[0].strip()
#     action = parts[1].strip().upper() # 액션을 대문자로 변환

#     # --- 플레이어 할당 로직 ---
#     if not game_logic.game_started:
#         if ip not in game_logic.players:
#             if "player1" not in game_logic.players.values():
#                 game_logic.players[ip] = "player1"
#                 print(f"[{ip}] 할당: player1")
#             elif "player2" not in game_logic.players.values():
#                 game_logic.players[ip] = "player2"
#                 print(f"[{ip}] 할당: player2")
#             else:
#                 print(f"[{ip}] 접속 시도: 플레이어 슬롯이 모두 찼습니다. (게임 대기 중)")
#                 flag_publisher_socket.send_string("GAME_STATE,0")
#                 # GUI 상태 업데이트 (슬롯이 찼을 때도 대기 상태 유지)
#                 gui.update_hp(game_logic.players_hp["player1"], game_logic.players_hp["player2"])
#                 gui.set_game_state(0)
#                 # GUI 프레임 업데이트 호출
#                 gui_running = gui.run_gui_frame()
#                 if not gui_running: break
#                 continue
        
#         if len(game_logic.players) == 2:
#             print("\n게임 시작!")
#             game_logic.game_started = True # game_logic 모듈의 game_started 변경
#             flag_publisher_socket.send_string("GAME_STATE,1") # 클라이언트에게 1 (게임 중) 전송
#             # GUI에 게임 상태 업데이트 (game_logic에서 직접 호출하므로 이 부분은 삭제)
#             # game_logic.send_gui_state_update(gui_publisher_socket, 1, game_logic.players_hp["player1"], game_logic.players_hp["player2"])
#             gui.set_game_state(1) # GUI를 게임 중 상태로 설정
#             # 카운트다운 추가 (5, 4, 3, 2, 1)
#             for i in range(5, 0, -1):
#                 gui.set_countdown(i)
#                 gui.run_gui_frame() # 카운트다운 화면 업데이트
#                 time.sleep(1)
#             gui.set_countdown(0) # 카운트다운 완료

#             gui.update_hp(game_logic.players_hp["player1"], game_logic.players_hp["player2"]) # 게임 시작 시 HP 업데이트
#             # GUI 프레임 업데이트 호출
#             gui_running = gui.run_gui_frame()
#             if not gui_running: break
#             time.sleep(0.5) # 게임 시작 후 짧은 대기 (선택 사항)
#             continue
#         else:
#             if action == "ACCEPT":
#                 pass
#             else:
#                 print(f"[{game_logic.players.get(ip, 'Unknown')}] 게임 시작 전 '{action}' 액션 수신. (무시)")
#             # GUI 프레임 업데이트 호출
#             gui_running = gui.run_gui_frame()
#             if not gui_running: break
#             continue
    
#     # --- 게임이 시작되었고, 해당 IP가 등록된 플레이어인 경우에만 액션 처리 ---
#     if game_logic.game_started and ip in game_logic.players:
#         # 게임 로직 모듈의 액션 처리 함수 호출 (gui_publisher_socket은 더 이상 전달하지 않음)
#         game_active_after_action = game_logic.process_player_action(ip, action, current_time, db_pusher_socket)

#         # 게임이 종료된 경우
#         if not game_active_after_action:
#             flag_publisher_socket.send_string("GAME_STATE,0")
#             # GUI에 게임 상태 업데이트 (game_logic에서 직접 호출하므로 이 부분은 삭제)
#             # game_logic.send_gui_state_update(gui_publisher_socket, 0, game_logic.players_hp["player1"], game_logic.players_hp["player2"])
#             gui.set_game_state(0) # GUI를 대기 상태로 설정
#             gui.update_hp(game_logic.players_hp["player1"], game_logic.players_hp["player2"]) # 게임 종료 후 최종 HP 반영
#             print("게임이 종료되었습니다. 새로운 게임을 기다립니다.")
#     elif game_logic.game_started and ip not in game_logic.players:
#         print(f"[{ip}] 접속 시도: 게임이 이미 시작되었습니다. (액션 무시)")
#         flag_publisher_socket.send_string("GAME_STATE,1")
    
#     # 메시지 처리 후에도 GUI 프레임 업데이트는 계속 호출
#     gui_running = gui.run_gui_frame() # 매 루프마다 GUI 업데이트
#     if not gui_running: break

# # GUI 종료 및 Pygame 종료
# pygame.quit()
# sys.exit()
import time
import zmq
from zmq_handler import setup_subscriber
import game_logic # game_logic 모듈 전체 임포트
import gui # gui 모듈 전체 임포트
import pygame # pygame을 사용하여 GUI 종료 신호를 처리하기 위함

# --- ZMQ 컨텍스트 및 소켓 설정 ---
context = zmq.Context()

# 게임 상태 플래그를 relay_server.py로 발행하는 PUB 소켓
flag_publisher_socket = context.socket(zmq.PUB)
flag_publisher_socket.bind(f"tcp://*:6001")

# DB_manager.c로 게임 결과를 PUSH하는 소켓
db_pusher_socket = context.socket(zmq.PUSH)
db_pusher_socket.connect(f"tcp://localhost:6003")

# relay_server.py로부터 클라이언트 액션을 수신하는 SUB 소켓
sub_socket = setup_subscriber()

print("ZMQ 게임 서버 시작 - 메시지 대기 중...")
print(f"게임 상태 플래그 발행 준비 완료 (tcp://*:6001)")
print(f"C DB 서비스로 요청 전송 준비 완료 (tcp://localhost:6003)")

# --- 초기 게임 상태 전송 (GUI 및 클라이언트 대기 상태) ---
flag_publisher_socket.send_string("GAME_STATE,0")
gui.update_hp(game_logic.players_hp["player1"], game_logic.players_hp["player2"])
gui.set_game_state(0) # GUI를 대기 상태로 설정

# --- 메인 게임 루프 ---
gui_running = True # GUI 루프를 제어할 플래그
game_end_process_active = False # 게임 종료 후 처리 활성화 플래그
game_end_time = 0 # 게임 종료 시간 기록

while gui_running: # GUI가 종료되면 main 루프도 종료
    try:
        # ZMQ 메시지를 논블로킹 방식으로 수신
        msg = sub_socket.recv_string(zmq.DONTWAIT)
        current_time = time.time() # 메시지 수신 즉시 정확한 타임스탬프 기록
    except zmq.Again:
        # 메시지가 없을 때도 GUI는 계속 업데이트되어야 함 (애니메이션 등)
        
        # 게임 종료 후 10초 대기 로직
        if game_end_process_active:
            if time.time() - game_end_time >= 10:
                print("게임 종료 후 10초 경과. 초기 대기 상태로 돌아갑니다.")
                game_end_process_active = False
                game_logic.game_started = False # 게임 상태 초기화
                game_logic.players.clear() # 플레이어 정보 초기화
                game_logic.players_hp["player1"] = 100 # HP 초기화
                game_logic.players_hp["player2"] = 100 # HP 초기화
                game_logic.last_attack_time["player1"] = 0
                game_logic.last_attack_time["player2"] = 0
                flag_publisher_socket.send_string("GAME_STATE,0") # 클라이언트에게 대기 상태 전송
                gui.set_game_state(0) # GUI도 대기 상태로 초기화
                gui.update_hp(game_logic.players_hp["player1"], game_logic.players_hp["player2"]) # GUI HP도 초기화
        
        # GUI 프레임 업데이트 호출
        gui_running = gui.run_gui_frame() # gui.run_gui_frame()이 False를 반환하면 종료
        if not gui_running:
            break 

        time.sleep(0.01) # 짧은 지연으로 CPU 사용률 관리
        continue # 다음 루프 반복

    parts = msg.split(',')

    if len(parts) != 2:
        print(f"잘못된 ZMQ 메시지 포맷: {msg}")
        # GUI 프레임 업데이트 호출 (오류 발생 시에도 GUI는 계속 동작)
        gui_running = gui.run_gui_frame()
        if not gui_running: break
        continue

    ip = parts[0].strip()
    action = parts[1].strip().upper() # 액션을 대문자로 변환

    # --- 플레이어 할당 로직 ---
    # 게임 종료 후 대기 중에는 새로운 플레이어 할당을 시도해야 함
    if not game_logic.game_started and not game_end_process_active: # 게임 종료 처리 중이 아닐 때만
        if ip not in game_logic.players:
            if "player1" not in game_logic.players.values():
                game_logic.players[ip] = "player1"
                print(f"[{ip}] 할당: player1")
            elif "player2" not in game_logic.players.values():
                game_logic.players[ip] = "player2"
                print(f"[{ip}] 할당: player2")
            else:
                print(f"[{ip}] 접속 시도: 플레이어 슬롯이 모두 찼습니다. (게임 대기 중)")
                flag_publisher_socket.send_string("GAME_STATE,0")
                gui.update_hp(game_logic.players_hp["player1"], game_logic.players_hp["player2"])
                gui.set_game_state(0)
                gui_running = gui.run_gui_frame()
                if not gui_running: break
                continue
        
        # 두 플레이어가 모두 접속하고 game_started가 False일 때만 게임 시작
        if len(game_logic.players) == 2:
            print("\n게임 시작 준비! 카운트다운 시작...")
            flag_publisher_socket.send_string("GAME_STATE,0") # 카운트다운 중에는 아직 게임 시작 아님
            gui.set_game_state(2) # GUI를 카운트다운 상태로 설정

            # 카운트다운 (5, 4, 3, 2, 1)
            for i in range(5, 0, -1):
                gui.set_countdown(i)
                gui_running = gui.run_gui_frame() # 카운트다운 화면 업데이트
                if not gui_running: break # GUI 종료 신호
                time.sleep(1)
            
            if not gui_running: break # GUI 종료 신호가 왔으면 루프 종료
            
            gui.set_countdown(0) # 카운트다운 완료
            game_logic.game_started = True # game_logic 모듈의 game_started 변경
            flag_publisher_socket.send_string("GAME_STATE,1") # 클라이언트에게 1 (게임 중) 전송
            gui.set_game_state(1) # GUI를 게임 중 상태로 설정
            gui.update_hp(game_logic.players_hp["player1"], game_logic.players_hp["player2"]) # 게임 시작 시 HP 업데이트
            
            print("게임 시작!")
            # time.sleep(0.5) # 게임 시작 후 짧은 대기 (선택 사항)
            continue
        else: # 아직 플레이어 할당 중이거나 한 명만 접속한 상태
            if action == "ACCEPT":
                pass
            else:
                print(f"[{game_logic.players.get(ip, 'Unknown')}] 게임 시작 전 '{action}' 액션 수신. (무시)")
            gui_running = gui.run_gui_frame()
            if not gui_running: break
            continue
    
    # --- 게임이 시작되었고, 해당 IP가 등록된 플레이어인 경우에만 액션 처리 ---
    # game_end_process_active가 True이면 액션 무시 (게임 종료 처리 중)
    if game_logic.game_started and ip in game_logic.players and not game_end_process_active:
        # 게임 로직 모듈의 액션 처리 함수 호출 (gui_publisher_socket은 더 이상 전달하지 않음)
        game_active_after_action = game_logic.process_player_action(ip, action, current_time, db_pusher_socket)

        # game_logic.process_player_action이 False를 반환하면 게임 종료
        if not game_active_after_action: 
            print("게임이 종료되었습니다. 10초 후 새로운 게임을 기다립니다.")
            game_end_process_active = True # 게임 종료 처리 활성화
            game_end_time = time.time() # 게임 종료 시간 기록
            # GUI는 이미 game_logic.show_game_result에서 게임 종료 상태로 변경됨
            # flag_publisher_socket.send_string("GAME_STATE,0") # 클라이언트에게 대기 상태 전송은 10초 후에
            # gui.set_game_state(0) # GUI 초기화는 10초 후에
            # gui.update_hp(...) # GUI HP 업데이트도 10초 후에
    elif (game_logic.game_started or game_end_process_active) and ip not in game_logic.players:
        print(f"[{ip}] 접속 시도: 게임이 이미 시작되었거나 종료 처리 중입니다. (액션 무시)")
        # 게임 진행 중 플래그 전송 (클라이언트 동기화, 게임 종료 처리 중일 때도 게임 플래그 1을 유지하여 클라이언트 액션 무시)
        flag_publisher_socket.send_string("GAME_STATE,1" if game_logic.game_started else "GAME_STATE,0") # 게임 상태에 따라 적절한 플래그 전송
    
    # 메시지 처리 후에도 GUI 프레임 업데이트는 계속 호출
    gui_running = gui.run_gui_frame() # 매 루프마다 GUI 업데이트
    if not gui_running: break

# GUI 종료 및 Pygame 종료
pygame.quit()
sys.exit()
