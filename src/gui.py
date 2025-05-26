# # # gui.py
# # import pygame
# # import sys
# # import zmq
# # import os

# # # 초기화
# # pygame.init()

# # # 화면 설정
# # WIDTH, HEIGHT = 600, 400
# # GameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
# # pygame.display.set_caption("위대한 2조 동무들의 합동작업")

# # # 색상 정의
# # WHITE = (255, 255, 255)
# # BLACK = (0, 0, 0)
# # RED = (255, 0, 0)
# # GREEN = (0, 255, 0)
# # BLUE = (0, 0, 255)
# # HP_COLOR = (255, 0, 0) # HP바 색상

# # # 폰트 설정
# # try:
# #     font = pygame.font.SysFont('Malgun Gothic', 30) # 한글 폰트 (Windows 기준)
# #     hp_font = pygame.font.SysFont('Arial', 24)
# # except:
# #     print("Warning: Malgun Gothic or Arial font not found, using default.")
# #     font = pygame.font.SysFont(None, 30)
# #     hp_font = pygame.font.SysFont(None, 24)

# # # 이미지 로드 (현재 스크립트 파일의 디렉토리를 기준으로 images 폴더 지정)
# # script_dir = os.path.dirname(__file__)
# # image_dir = os.path.join(script_dir, 'images')

# # # 이미지 파일 이름 리스트 (movement 이미지 추가)
# # image_files = {
# #     'background': 'background.png',
# #     'player1_normal': 'player1_normal.png',
# #     'player1_attack': 'player1_attack.png',
# #     'player1_hit': 'player1_hit.png',
# #     'player1_movement': 'player1_movement.png', # MOVEMENT 이미지 추가
# #     'player2_normal': 'player2_normal.png',
# #     'player2_attack': 'player2_attack.png',
# #     'player2_hit': 'player2_hit.png',
# #     'player2_movement': 'player2_movement.png', # MOVEMENT 이미지 추가
# # }

# # # 로드된 이미지 저장 딕셔너리
# # loaded_images = {}

# # try:
# #     for key, filename in image_files.items():
# #         path = os.path.join(image_dir, filename)
# #         img = pygame.image.load(path)
# #         loaded_images[key] = img

# #     # 이미지 크기 조정
# #     loaded_images['background'] = pygame.transform.scale(loaded_images['background'], (WIDTH, HEIGHT))
    
# #     # 플레이어 이미지 크기 정의
# #     player_normal_size = (100, 100)
# #     player_attack_size = (120, 100) # 공격 시 약간 커지도록
# #     player_movement_size = (110, 100) # 이동 시 약간 다른 크기 (예시)

# #     # Player1 이미지 크기 조정
# #     loaded_images['player1_normal'] = pygame.transform.scale(loaded_images['player1_normal'], player_normal_size)
# #     loaded_images['player1_attack'] = pygame.transform.scale(loaded_images['player1_attack'], player_attack_size)
# #     loaded_images['player1_hit'] = pygame.transform.scale(loaded_images['player1_hit'], player_normal_size)
# #     loaded_images['player1_movement'] = pygame.transform.scale(loaded_images['player1_movement'], player_movement_size)

# #     # Player2 이미지 크기 조정 및 좌우 반전
# #     # Player2의 normal, hit, movement 이미지는 좌우 반전
# #     loaded_images['player2_normal'] = pygame.transform.flip(pygame.transform.scale(loaded_images['player2_normal'], player_normal_size), True, False)
# #     loaded_images['player2_hit'] = pygame.transform.flip(pygame.transform.scale(loaded_images['player2_hit'], player_normal_size), True, False)
# #     loaded_images['player2_movement'] = pygame.transform.flip(pygame.transform.scale(loaded_images['player2_movement'], player_movement_size), True, False)
    
# #     # Player2의 attack 이미지는 player2_attack.png가 있다면 그걸 쓰고, 없다면 player1_attack을 반전해서 사용
# #     if 'player2_attack' in image_files and os.path.exists(os.path.join(image_dir, image_files['player2_attack'])):
# #         loaded_images['player2_attack'] = pygame.transform.flip(pygame.transform.scale(loaded_images['player2_attack'], player_attack_size), True, False)
# #     else:
# #         print("Warning: player2_attack.png not found, using flipped player1_attack.png for Player2 attack.")
# #         loaded_images['player2_attack'] = pygame.transform.flip(pygame.transform.scale(loaded_images['player1_attack'], player_attack_size), True, False)


# # except pygame.error as e:
# #     print(f"이미지 로드 오류: {e}")
# #     print(f"이미지 파일이 '{image_dir}' 폴더에 있고, 이름이 올바른지 확인해주세요.")
# #     # 오류 발생 시 기본 색상으로 대체
# #     loaded_images['background'] = pygame.Surface((WIDTH, HEIGHT)); loaded_images['background'].fill(BLUE)
# #     loaded_images['player1_normal'] = pygame.Surface(player_normal_size); loaded_images['player1_normal'].fill(RED)
# #     loaded_images['player1_attack'] = pygame.Surface(player_attack_size); loaded_images['player1_attack'].fill(RED)
# #     loaded_images['player1_hit'] = pygame.Surface(player_normal_size); loaded_images['player1_hit'].fill(RED)
# #     loaded_images['player1_movement'] = pygame.Surface(player_movement_size); loaded_images['player1_movement'].fill(RED)
# #     loaded_images['player2_normal'] = pygame.Surface(player_normal_size); loaded_images['player2_normal'].fill(GREEN)
# #     loaded_images['player2_attack'] = pygame.Surface(player_attack_size); loaded_images['player2_attack'].fill(GREEN)
# #     loaded_images['player2_hit'] = pygame.Surface(player_normal_size); loaded_images['player2_hit'].fill(GREEN)
# #     loaded_images['player2_movement'] = pygame.Surface(player_movement_size); loaded_images['player2_movement'].fill(GREEN)


# # # FPS 설정
# # FPS = 30
# # FramePerSec = pygame.time.Clock()

# # # 플레이어 클래스
# # class Player(pygame.sprite.Sprite):
# #     def __init__(self, x, y, role):
# #         super().__init__()
# #         self.role = role # "player1" or "player2"
        
# #         self.normal_image = loaded_images[f'{role}_normal']
# #         self.attack_image = loaded_images[f'{role}_attack']
# #         self.hit_image = loaded_images[f'{role}_hit']
# #         self.movement_image = loaded_images[f'{role}_movement'] # MOVEMENT 이미지 속성 추가
        
# #         self.image = self.normal_image
# #         self.rect = self.image.get_rect()
# #         self.rect.center = (x, y)
# #         self.hp = 100 # 초기 HP
        
# #         self.original_x = x # 원래 x 위치 저장
# #         self.original_y = y # 원래 y 위치 저장

# #         self.atk_anim_active = False
# #         self.atk_anim_start_time = 0
# #         self.atk_anim_duration = 200 # ms
        
# #         self.hit_anim_active = False
# #         self.hit_anim_start_time = 0
# #         self.hit_anim_duration = 300 # ms

# #         self.mv_anim_active = False
# #         self.mv_anim_start_time = 0
# #         self.mv_anim_duration = 200 # ms
# #         self.mv_distance = 20 # 뒤로 물러나는 거리 (픽셀)

# #     def display_hp(self):
# #         hp_text = hp_font.render(f"HP: {self.hp}", True, HP_COLOR)
# #         return hp_text

# #     def draw(self, surface):
# #         current_image = self.image # 현재 애니메이션에 따라 변경될 이미지

# #         if self.atk_anim_active:
# #             current_image = self.attack_image
# #             if pygame.time.get_ticks() - self.atk_anim_start_time > self.atk_anim_duration:
# #                 self.atk_anim_active = False
# #                 self.image = self.normal_image # 애니메이션 종료 후 원본 이미지로 복귀
# #                 self.rect.center = (self.original_x, self.original_y)
# #         elif self.hit_anim_active:
# #             current_image = self.hit_image
# #             if pygame.time.get_ticks() - self.hit_anim_start_time > self.hit_anim_duration:
# #                 self.hit_anim_active = False
# #                 self.image = self.normal_image # 애니메이션 종료 후 원본 이미지로 복귀
# #                 self.rect.center = (self.original_x, self.original_y)
# #         elif self.mv_anim_active: # MOVEMENT 애니메이션 처리
# #             current_image = self.movement_image # MOVEMENT 이미지 사용
# #             current_time = pygame.time.get_ticks()
# #             if current_time - self.mv_anim_start_time < self.mv_anim_duration:
# #                 # 애니메이션 시간 동안 뒤로 이동
# #                 if self.role == "player1": # P1은 왼쪽, 뒤로 가면 x값이 줄어듦
# #                     self.rect.center = (self.original_x - self.mv_distance, self.original_y)
# #                 else: # P2는 오른쪽, 뒤로 가면 x값이 늘어남
# #                     self.rect.center = (self.original_x + self.mv_distance, self.original_y)
# #             else:
# #                 self.mv_anim_active = False
# #                 self.image = self.normal_image # 애니메이션 종료 시 원본 이미지로 복귀
# #                 self.rect.center = (self.original_x, self.original_y)
# #         else: # 어떤 애니메이션도 활성화되어 있지 않을 때
# #             self.image = self.normal_image # 기본 이미지로 설정 (안전장치)
# #             self.rect.center = (self.original_x, self.original_y) # 항상 원래 위치

# #         # 현재 이미지의 rect를 업데이트하여 blit
# #         self.rect = current_image.get_rect(center=self.rect.center) # 이미지 변경 시 rect 크기 업데이트
# #         surface.blit(current_image, self.rect)

# #     def attack_animation(self):
# #         if not self.atk_anim_active:
# #             self.atk_anim_active = True
# #             self.atk_anim_start_time = pygame.time.get_ticks()
# #             self.image = self.attack_image # 즉시 공격 이미지로 변경
        
# #     def hit_animation(self):
# #         if not self.hit_anim_active:
# #             self.hit_anim_active = True
# #             self.hit_anim_start_time = pygame.time.get_ticks()
# #             self.image = self.hit_image # 즉시 피격 이미지로 변경

# #     def movement_animation(self):
# #         if not self.mv_anim_active:
# #             self.mv_anim_active = True
# #             self.mv_anim_start_time = pygame.time.get_ticks()
# #             self.image = self.movement_image # MOVEMENT 이미지로 변경

# # # 플레이어 객체 생성
# # P1 = Player(150, 300, "player1")
# # P2 = Player(450, 300, "player2")


# # # ZMQ 설정
# # context = zmq.Context()
# # sub_socket = context.socket(zmq.SUB)
# # # main.py의 GUI PUB 소켓과 연결 (GUI_SUB_PORT)
# # sub_socket.connect("tcp://localhost:6002")
# # sub_socket.setsockopt_string(zmq.SUBSCRIBE, "GAME_STATE_GUI,")
# # sub_socket.setsockopt_string(zmq.SUBSCRIBE, "ACTION_GUI,")
# # sub_socket.setsockopt_string(zmq.SUBSCRIBE, "HIT_GUI,")
# # sub_socket.setsockopt_string(zmq.SUBSCRIBE, "GAME_RESULT,")


# # # 게임 상태 변수
# # game_over_flag = False
# # current_game_state = 0 # 0: 대기 및 초기화, 1: 게임 중
# # winner_text = ""

# # # ZMQ 메시지 수신 및 처리 함수 (논블로킹)
# # def receive_zmq_messages():
# #     global P1, P2, current_game_state, winner_text, game_over_flag
# #     try:
# #         msg = sub_socket.recv_string(zmq.DONTWAIT)
# #         print(f"[GUI] ZMQ 메시지 수신: {msg}")
# #         parts = msg.split(',')
        
# #         if len(parts) >= 1:
# #             msg_type = parts[0]

# #             if msg_type == "GAME_STATE_GUI" and len(parts) == 3:
# #                 new_state = int(parts[1])
# #                 hp_parts = parts[2].split(':')
# #                 if len(hp_parts) == 2:
# #                     p1_hp = int(hp_parts[0])
# #                     p2_hp = int(hp_parts[1])
# #                     P1.hp = p1_hp
# #                     P2.hp = p2_hp

# #                 # GUI의 게임 상태 플래그 업데이트
# #                 if current_game_state != new_state:
# #                     current_game_state = new_state
# #                     print(f"[GUI] 게임 상태 업데이트: {current_game_state}")
# #                     if current_game_state == 0:
# #                         game_over_flag = False
# #                         winner_text = ""

# #             elif msg_type == "ACTION_GUI" and len(parts) == 3:
# #                 player_role = parts[1]
# #                 action_type = parts[2]

# #                 if action_type == "ATTACK":
# #                     if player_role == "player1":
# #                         P1.attack_animation()
# #                     elif player_role == "player2":
# #                         P2.attack_animation()
# #                 elif action_type == "MOVEMENT": # MOVEMENT 처리 활성화
# #                     if player_role == "player1":
# #                         P1.movement_animation()
# #                     elif player_role == "player2":
# #                         P2.movement_animation()
                
# #             elif msg_type == "HIT_GUI" and len(parts) == 2:
# #                 hit_player_role = parts[1]
# #                 if hit_player_role == "player1":
# #                     P1.hit_animation()
# #                 elif hit_player_role == "player2":
# #                     P2.hit_animation()

# #             elif msg_type == "GAME_RESULT" and len(parts) == 2:
# #                 game_over_flag = True
# #                 winner_text = parts[1]
# #                 print(f"[GUI] 게임 종료 결과 수신: {winner_text}")

# #     except zmq.Again:
# #         pass # 읽을 메시지가 없으면 발생, 정상 처리
# #     except Exception as e:
# #         print(f"[GUI Error] ZMQ 메시지 처리 오류: {e}")

# # # 게임 루프
# # running = True
# # while running:
# #     for event in pygame.event.get():
# #         if event.type == pygame.QUIT:
# #             running = False

# #     # ZMQ 메시지 수신
# #     receive_zmq_messages()

# #     GameDisplay.blit(loaded_images['background'], loaded_images['background'].get_rect()) # 배경 그리기

# #     # 플레이어 캐릭터 그리기
# #     P1.draw(GameDisplay)
# #     P2.draw(GameDisplay)

# #     # HP 표시
# #     GameDisplay.blit(P1.display_hp(), (10, 10))
# #     GameDisplay.blit(P2.display_hp(), (WIDTH - P2.display_hp().get_width() - 10, 10))

# #     # 게임 상태에 따른 UI 업데이트
# #     if current_game_state == 0: # 게임 대기 및 초기화 중
# #         waiting_text = font.render("Waiting for Players...", True, WHITE)
# #         text_rect = waiting_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
# #         GameDisplay.blit(waiting_text, text_rect)
        
# #     # 게임 결과 화면 표시 (게임 종료 후 '대기' 상태로 전환될 때도 잠시 표시)
# #     if game_over_flag:
# #         result_font = pygame.font.SysFont('Malgun Gothic', 50)
# #         result_text_render = result_font.render(winner_text, True, BLACK)
# #         result_text_rect = result_text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
# #         GameDisplay.blit(result_text_render, result_text_rect)
            
# #     pygame.display.update()
# #     FramePerSec.tick(FPS)

# # # 게임 종료 시 ZMQ 소켓 정리
# # sub_socket.close()
# # context.term() # 컨텍스트 파괴 (모든 소켓 닫은 후)
# # print("[GUI] ZMQ sockets and context terminated.")

# # pygame.quit()
# # sys.exit()
# # # gui.py
# # import pygame
# # import sys
# # import zmq
# # import os

# # # --- ZMQ 컨텍스트 및 소켓 설정 추가 ---
# # context = zmq.Context()
# # sub_socket = context.socket(zmq.SUB)
# # sub_socket.connect("tcp://localhost:6002") # main.py의 GUI PUB 소켓에 연결
# # sub_socket.setsockopt_string(zmq.SUBSCRIBE, "") # 모든 메시지 구독

# # print("[GUI] ZMQ 구독 소켓 연결 완료 (tcp://localhost:6002)")
# # # --- ZMQ 컨텍스트 및 소켓 설정 추가 끝 ---

# # # 초기화
# # pygame.init()

# # # 화면 설정
# # WIDTH, HEIGHT = 600, 400
# # GameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
# # pygame.display.set_caption("위대한 2조 동무들의 합동작업")

# # # 색상 정의
# # WHITE = (255, 255, 255)
# # BLACK = (0, 0, 0)
# # RED = (255, 0, 0)
# # GREEN = (0, 255, 0)
# # BLUE = (0, 0, 255)
# # HP_COLOR = (255, 0, 0) # HP바 색상

# # # 폰트 설정
# # try:
# #     font = pygame.font.SysFont('Malgun Gothic', 30) # 한글 폰트 (Windows 기준)
# #     hp_font = pygame.font.SysFont('Arial', 24)
# #     # instructions_font는 test_gui에서만 사용되므로 여기서는 제거
# # except:
# #     print("Warning: Malgun Gothic or Arial font not found, using default.")
# #     font = pygame.font.SysFont(None, 30)
# #     hp_font = pygame.font.SysFont(None, 24)

# # # 이미지 로드 (현재 스크립트 파일의 디렉토리를 기준으로 images 폴더 지정)
# # script_dir = os.path.dirname(__file__)
# # image_dir = os.path.join(script_dir, 'images')

# # # 이미지 파일 이름 리스트 (movement 이미지 포함)
# # image_files = {
# #     'background': 'background.png',
# #     'player1_normal': 'player1_normal.png',
# #     'player1_attack': 'player1_attack.png',
# #     'player1_hit': 'player1_hit.png',
# #     'player1_movement': 'player1_movement.png', 
# #     'player2_normal': 'player2_normal.png',
# #     'player2_attack': 'player2_attack.png', 
# #     'player2_hit': 'player2_hit.png',
# #     'player2_movement': 'player2_movement.png', 
# # }

# # # 로드된 이미지 저장 딕셔너리
# # loaded_images = {}

# # # 이미지 로드 및 크기 조정 (200% 스케일 적용)
# # # try-except 블록 제거: 사용자님의 피드백에 따라 파일이 항상 존재한다고 가정
# # for key, filename in image_files.items():
# #     path = os.path.join(image_dir, filename)
# #     img = pygame.image.load(path)
# #     loaded_images[key] = img

# # loaded_images['background'] = pygame.transform.scale(loaded_images['background'], (WIDTH, HEIGHT))

# # # 플레이어 이미지 크기 정의 (200% 스케일)
# # player_normal_size = (100 * 2, 100 * 2) 
# # player_attack_size = (120 * 2, 100 * 2) 
# # player_movement_size = (110 * 2, 100 * 2) 

# # # Player1 이미지 크기 조정
# # loaded_images['player1_normal'] = pygame.transform.scale(loaded_images['player1_normal'], player_normal_size)
# # loaded_images['player1_attack'] = pygame.transform.scale(loaded_images['player1_attack'], player_attack_size)
# # loaded_images['player1_hit'] = pygame.transform.scale(loaded_images['player1_hit'], player_normal_size)
# # loaded_images['player1_movement'] = pygame.transform.scale(loaded_images['player1_movement'], player_movement_size)

# # # Player2 이미지 크기 조정 (flip 제거)
# # loaded_images['player2_normal'] = pygame.transform.scale(loaded_images['player2_normal'], player_normal_size)
# # loaded_images['player2_attack'] = pygame.transform.scale(loaded_images['player2_attack'], player_attack_size)
# # loaded_images['player2_hit'] = pygame.transform.scale(loaded_images['player2_hit'], player_normal_size)
# # loaded_images['player2_movement'] = pygame.transform.scale(loaded_images['player2_movement'], player_movement_size)


# # # FPS 설정
# # FPS = 30
# # FramePerSec = pygame.time.Clock()

# # # 플레이어 클래스
# # class Player(pygame.sprite.Sprite):
# #     def __init__(self, x, y, role):
# #         super().__init__()
# #         self.role = role # "player1" or "player2"
        
# #         self.normal_image = loaded_images[f'{role}_normal']
# #         self.attack_image = loaded_images[f'{role}_attack']
# #         self.hit_image = loaded_images[f'{role}_hit']
# #         self.movement_image = loaded_images[f'{role}_movement'] # MOVEMENT 이미지 속성 추가
        
# #         self.image = self.normal_image
# #         self.rect = self.image.get_rect()
# #         self.rect.center = (x, y)
# #         self.hp = 100 # 초기 HP
        
# #         self.original_x = x # 원래 x 위치 저장
# #         self.original_y = y # 원래 y 위치 저장

# #         self.atk_anim_active = False
# #         self.atk_anim_start_time = 0
# #         self.atk_anim_duration = 200 # ms
        
# #         self.hit_anim_active = False
# #         self.hit_anim_start_time = 0
# #         self.hit_anim_duration = 300 # ms

# #         self.mv_anim_active = False
# #         self.mv_anim_start_time = 0
# #         self.mv_anim_duration = 200 # ms
# #         self.mv_distance = 20 # 뒤로 물러나는 거리 (픽셀)

# #     def display_hp(self):
# #         hp_text = hp_font.render(f"HP: {self.hp}", True, HP_COLOR)
# #         return hp_text

# #     def draw(self, surface):
# #         current_image = self.image # 현재 애니메이션에 따라 변경될 이미지

# #         if self.atk_anim_active:
# #             current_image = self.attack_image
# #             if pygame.time.get_ticks() - self.atk_anim_start_time > self.atk_anim_duration:
# #                 self.atk_anim_active = False
# #                 self.image = self.normal_image # 애니메이션 종료 후 원본 이미지로 복귀
# #                 self.rect = self.image.get_rect(center=(self.original_x, self.original_y)) # rect 업데이트
# #         elif self.hit_anim_active:
# #             current_image = self.hit_image
# #             if pygame.time.get_ticks() - self.hit_anim_start_time > self.hit_anim_duration:
# #                 self.hit_anim_active = False
# #                 self.image = self.normal_image # 애니메이션 종료 후 원본 이미지로 복귀
# #                 self.rect = self.image.get_rect(center=(self.original_x, self.original_y)) # rect 업데이트
# #         elif self.mv_anim_active: # MOVEMENT 애니메이션 처리
# #             current_image = self.movement_image # MOVEMENT 이미지 사용
# #             current_time = pygame.time.get_ticks()
# #             if current_time - self.mv_anim_start_time < self.mv_anim_duration:
# #                 # 애니메이션 시간 동안 뒤로 이동
# #                 if self.role == "player1": # P1은 왼쪽, 뒤로 가면 x값이 줄어듦
# #                     self.rect.center = (self.original_x - self.mv_distance, self.original_y)
# #                 else: # P2는 오른쪽, 뒤로 가면 x값이 늘어남
# #                     self.rect.center = (self.original_x + self.mv_distance, self.original_y)
# #             else:
# #                 self.mv_anim_active = False
# #                 self.image = self.normal_image # 애니메이션 종료 시 원본 이미지로 복귀
# #                 self.rect.center = (self.original_x, self.original_y) # 항상 원래 위치
# #         else: # 어떤 애니메이션도 활성화되어 있지 않을 때
# #             self.image = self.normal_image # 기본 이미지로 설정 (안전장치)
# #             self.rect.center = (self.original_x, self.original_y) # 항상 원래 위치

# #         # 현재 이미지의 rect를 업데이트하여 blit
# #         # current_image의 rect를 사용하여 그릴 때, 기존 rect의 center를 유지하도록 합니다.
# #         display_rect = current_image.get_rect(center=self.rect.center)
# #         surface.blit(current_image, display_rect)

# #     def attack_animation(self):
# #         if not self.atk_anim_active:
# #             self.atk_anim_active = True
# #             self.atk_anim_start_time = pygame.time.get_ticks()
# #             self.image = self.attack_image # 즉시 공격 이미지로 변경
        
# #     def hit_animation(self):
# #         if not self.hit_anim_active:
# #             self.hit_anim_active = True
# #             self.hit_anim_start_time = pygame.time.get_ticks()
# #             self.image = self.hit_image # 즉시 피격 이미지로 변경

# #     def movement_animation(self):
# #         if not self.mv_anim_active:
# #             self.mv_anim_active = True
# #             self.mv_anim_start_time = pygame.time.get_ticks()
# #             self.image = self.movement_image # MOVEMENT 이미지로 변경

# # # 플레이어 객체 생성 좌표 (사용자 의도대로 유지)
# # P1 = Player(220, 300, "player1")
# # P2 = Player(380, 300, "player2")

# # # 게임 상태 변수 (gui.py와 동일한 명칭 사용)
# # game_over_flag = False
# # current_game_state = 0 # 0: 대기 및 초기화, 1: 게임 중
# # winner_text = ""

# # # ZMQ 메시지 수신 및 처리 함수 (논블로킹)
# # def receive_zmq_messages():
# #     global P1, P2, current_game_state, winner_text, game_over_flag
# #     try:
# #         msg = sub_socket.recv_string(zmq.DONTWAIT)
# #         # print(f"[GUI] ZMQ 메시지 수신: {msg}") # 디버깅용
# #         parts = msg.split(',')
        
# #         if len(parts) >= 1:
# #             msg_type = parts[0]

# #             if msg_type == "GAME_STATE_GUI" and len(parts) == 3:
# #                 new_state = int(parts[1])
# #                 hp_parts = parts[2].split(':')
# #                 if len(hp_parts) == 2:
# #                     p1_hp = int(hp_parts[0])
# #                     p2_hp = int(hp_parts[1])
# #                     P1.hp = p1_hp
# #                     P2.hp = p2_hp

# #                 # GUI의 게임 상태 플래그 업데이트
# #                 if current_game_state != new_state:
# #                     current_game_state = new_state
# #                     print(f"[GUI] 게임 상태 업데이트: {current_game_state}")
# #                     if current_game_state == 0:
# #                         game_over_flag = False
# #                         winner_text = ""

# #             elif msg_type == "ACTION_GUI" and len(parts) == 3:
# #                 player_role = parts[1]
# #                 action_type = parts[2]

# #                 if action_type == "ATTACK":
# #                     if player_role == "player1":
# #                         P1.attack_animation()
# #                     elif player_role == "player2":
# #                         P2.attack_animation()
# #                 elif action_type == "MOVEMENT": 
# #                     if player_role == "player1":
# #                         P1.movement_animation()
# #                     elif player_role == "player2":
# #                         P2.movement_animation()
                
# #             elif msg_type == "HIT_GUI" and len(parts) == 2:
# #                 hit_player_role = parts[1]
# #                 if hit_player_role == "player1":
# #                     P1.hit_animation()
# #                 elif hit_player_role == "player2":
# #                     P2.hit_animation()

# #             elif msg_type == "GAME_RESULT" and len(parts) == 2:
# #                 game_over_flag = True
# #                 winner_text = parts[1]
# #                 print(f"[GUI] 게임 종료 결과 수신: {winner_text}")

# #     except zmq.Again:
# #         pass # 읽을 메시지가 없으면 발생, 정상 처리
# #     except Exception as e:
# #         print(f"[GUI Error] ZMQ 메시지 처리 오류: {e}")

# # # 게임 루프
# # running = True
# # while running:
# #     for event in pygame.event.get():
# #         if event.type == pygame.QUIT:
# #             running = False

# #     # ZMQ 메시지 수신
# #     receive_zmq_messages()

# #     GameDisplay.blit(loaded_images['background'], loaded_images['background'].get_rect()) # 배경 그리기

# #     # 플레이어 캐릭터 그리기
# #     P1.draw(GameDisplay)
# #     P2.draw(GameDisplay)

# #     # HP 표시
# #     GameDisplay.blit(P1.display_hp(), (10, 10))
# #     GameDisplay.blit(P2.display_hp(), (WIDTH - P2.display_hp().get_width() - 10, 10))

# #     # 게임 상태에 따른 UI 업데이트
# #     if current_game_state == 0: # 게임 대기 및 초기화 중
# #         waiting_text = font.render("Waiting for Players...", True, WHITE)
# #         text_rect = waiting_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
# #         GameDisplay.blit(waiting_text, text_rect)
        
# #     # 게임 결과 화면 표시 (게임 종료 후 '대기' 상태로 전환될 때도 잠시 표시)
# #     if game_over_flag:
# #         result_font = pygame.font.SysFont('Malgun Gothic', 50)
# #         result_text_render = result_font.render(winner_text, True, BLACK)
# #         result_text_rect = result_text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
# #         GameDisplay.blit(result_text_render, result_text_rect)
            
# #     pygame.display.update()
# #     FramePerSec.tick(FPS)

# # # 게임 종료 시 ZMQ 소켓 정리
# # sub_socket.close()
# # context.term() # 컨텍스트 파괴 (모든 소켓 닫은 후)
# # print("[GUI] ZMQ sockets and context terminated.")

# # pygame.quit()
# # sys.exit()

# #####################################################################################319~613


# import pygame
# import sys
# import os
# # import zmq # ZMQ 관련 라이브러리 임포트 제거

# # --- ZMQ 컨텍스트 및 소켓 설정 제거 ---
# # context = zmq.Context()
# # sub_socket = context.socket(zmq.SUB)
# # sub_socket.connect("tcp://localhost:6002")
# # sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
# # print("[GUI] ZMQ 구독 소켓 연결 완료 (tcp://localhost:6002)")
# # --- ZMQ 컨텍스트 및 소켓 설정 제거 끝 ---

# # 초기화
# pygame.init()

# # 화면 설정
# WIDTH, HEIGHT = 600, 400
# GameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("위대한 2조 동무들의 합동작업")

# # 색상 정의
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# HP_COLOR = (255, 0, 0) # HP바 색상

# # 폰트 설정
# try:
#     font = pygame.font.SysFont('Malgun Gothic', 30) # 한글 폰트 (Windows 기준)
#     hp_font = pygame.font.SysFont('Arial', 24)
# except:
#     print("Warning: Malgun Gothic or Arial font not found, using default.")
#     font = pygame.font.SysFont(None, 30)
#     hp_font = pygame.font.SysFont(None, 24)

# # 이미지 로드 (현재 스크립트 파일의 디렉토리를 기준으로 images 폴더 지정)
# script_dir = os.path.dirname(__file__)
# image_dir = os.path.join(script_dir, 'images')

# image_files = {
#     'background': 'background.png',
#     'player1_normal': 'player1_normal.png',
#     'player1_attack': 'player1_attack.png',
#     'player1_hit': 'player1_hit.png',
#     'player1_movement': 'player1_movement.png', 
#     'player2_normal': 'player2_normal.png',
#     'player2_attack': 'player2_attack.png', 
#     'player2_hit': 'player2_hit.png',
#     'player2_movement': 'player2_movement.png', 
# }

# loaded_images = {}

# for key, filename in image_files.items():
#     path = os.path.join(image_dir, filename)
#     img = pygame.image.load(path)
#     loaded_images[key] = img

# loaded_images['background'] = pygame.transform.scale(loaded_images['background'], (WIDTH, HEIGHT))

# player_normal_size = (100 * 2, 100 * 2) 
# player_attack_size = (120 * 2, 100 * 2) 
# player_movement_size = (110 * 2, 100 * 2) 

# loaded_images['player1_normal'] = pygame.transform.scale(loaded_images['player1_normal'], player_normal_size)
# loaded_images['player1_attack'] = pygame.transform.scale(loaded_images['player1_attack'], player_attack_size)
# loaded_images['player1_hit'] = pygame.transform.scale(loaded_images['player1_hit'], player_normal_size)
# loaded_images['player1_movement'] = pygame.transform.scale(loaded_images['player1_movement'], player_movement_size)

# loaded_images['player2_normal'] = pygame.transform.scale(loaded_images['player2_normal'], player_normal_size)
# loaded_images['player2_attack'] = pygame.transform.scale(loaded_images['player2_attack'], player_attack_size)
# loaded_images['player2_hit'] = pygame.transform.scale(loaded_images['player2_hit'], player_normal_size)
# loaded_images['player2_movement'] = pygame.transform.scale(loaded_images['player2_movement'], player_movement_size)


# # FPS 설정
# FPS = 30
# FramePerSec = pygame.time.Clock()

# # 플레이어 클래스
# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y, role):
#         super().__init__()
#         self.role = role # "player1" or "player2"
        
#         self.normal_image = loaded_images[f'{role}_normal']
#         self.attack_image = loaded_images[f'{role}_attack']
#         self.hit_image = loaded_images[f'{role}_hit']
#         self.movement_image = loaded_images[f'{role}_movement'] # MOVEMENT 이미지 속성 추가
        
#         self.image = self.normal_image
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)
#         self.hp = 100 # 초기 HP
        
#         self.original_x = x # 원래 x 위치 저장
#         self.original_y = y # 원래 y 위치 저장

#         self.atk_anim_active = False
#         self.atk_anim_start_time = 0
#         self.atk_anim_duration = 200 # ms
        
#         self.hit_anim_active = False
#         self.hit_anim_start_time = 0
#         self.hit_anim_duration = 300 # ms

#         self.mv_anim_active = False
#         self.mv_anim_start_time = 0
#         self.mv_anim_duration = 200 # ms
#         self.mv_distance = 20 # 뒤로 물러나는 거리 (픽셀)

#     def display_hp(self):
#         hp_text = hp_font.render(f"HP: {self.hp}", True, HP_COLOR)
#         return hp_text

#     def draw(self, surface):
#         current_image = self.image # 현재 애니메이션에 따라 변경될 이미지

#         if self.atk_anim_active:
#             current_image = self.attack_image
#             if pygame.time.get_ticks() - self.atk_anim_start_time > self.atk_anim_duration:
#                 self.atk_anim_active = False
#                 self.image = self.normal_image # 애니메이션 종료 후 원본 이미지로 복귀
#                 self.rect = self.image.get_rect(center=(self.original_x, self.original_y)) # rect 업데이트
#         elif self.hit_anim_active:
#             current_image = self.hit_image
#             if pygame.time.get_ticks() - self.hit_anim_start_time > self.hit_anim_duration:
#                 self.hit_anim_active = False
#                 self.image = self.normal_image # 애니메이션 종료 후 원본 이미지로 복귀
#                 self.rect = self.image.get_rect(center=(self.original_x, self.original_y)) # rect 업데이트
#         elif self.mv_anim_active: # MOVEMENT 애니메이션 처리
#             current_image = self.movement_image # MOVEMENT 이미지 사용
#             current_time = pygame.time.get_ticks()
#             if current_time - self.mv_anim_start_time < self.mv_anim_duration:
#                 # 애니메이션 시간 동안 뒤로 이동
#                 if self.role == "player1": # P1은 왼쪽, 뒤로 가면 x값이 줄어듦
#                     self.rect.center = (self.original_x - self.mv_distance, self.original_y)
#                 else: # P2는 오른쪽, 뒤로 가면 x값이 늘어남
#                     self.rect.center = (self.original_x + self.mv_distance, self.original_y)
#             else:
#                 self.mv_anim_active = False
#                 self.image = self.normal_image # 애니메이션 종료 시 원본 이미지로 복귀
#                 self.rect.center = (self.original_x, self.original_y) # 항상 원래 위치
#         else: # 어떤 애니메이션도 활성화되어 있지 않을 때
#             self.image = self.normal_image # 기본 이미지로 설정 (안전장치)
#             self.rect.center = (self.original_x, self.original_y) # 항상 원래 위치

#         # 현재 이미지의 rect를 업데이트하여 blit
#         # current_image의 rect를 사용하여 그릴 때, 기존 rect의 center를 유지하도록 합니다.
#         display_rect = current_image.get_rect(center=self.rect.center)
#         surface.blit(current_image, display_rect)

#     def attack_animation(self):
#         if not self.atk_anim_active:
#             self.atk_anim_active = True
#             self.atk_anim_start_time = pygame.time.get_ticks()
#             self.image = self.attack_image # 즉시 공격 이미지로 변경
        
#     def hit_animation(self):
#         if not self.hit_anim_active:
#             self.hit_anim_active = True
#             self.hit_anim_start_time = pygame.time.get_ticks()
#             self.image = self.hit_image # 즉시 피격 이미지로 변경

#     def movement_animation(self):
#         if not self.mv_anim_active:
#             self.mv_anim_active = True
#             self.mv_anim_start_time = pygame.time.get_ticks()
#             self.image = self.movement_image # MOVEMENT 이미지로 변경

# # 플레이어 객체 생성 좌표 (사용자 의도대로 유지)
# P1 = Player(220, 300, "player1")
# P2 = Player(380, 300, "player2")

# # 게임 상태 변수 (gui.py와 동일한 명칭 사용)
# game_over_flag = False
# current_game_state = 0 # 0: 대기 및 초기화, 1: 게임 중
# winner_text = ""
# countdown_value = 0 # 카운트다운 값 추가

# # --- 외부에서 호출할 GUI 업데이트 함수들 ---
# def update_hp(p1_hp, p2_hp):
#     """
#     플레이어 HP를 업데이트합니다.
#     """
#     P1.hp = p1_hp
#     P2.hp = p2_hp

# def trigger_action_animation(player_role, action_type):
#     """
#     플레이어 액션 애니메이션을 트리거합니다.
#     """
#     if action_type == "ATTACK":
#         if player_role == "player1":
#             P1.attack_animation()
#         elif player_role == "player2":
#             P2.attack_animation()
#     elif action_type == "MOVEMENT":
#         if player_role == "player1":
#             P1.movement_animation()
#         elif player_role == "player2":
#             P2.movement_animation()

# def trigger_hit_animation(hit_player_role):
#     """
#     플레이어 피격 애니메이션을 트리거합니다.
#     """
#     if hit_player_role == "player1":
#         P1.hit_animation()
#     elif hit_player_role == "player2":
#         P2.hit_animation()

# def set_game_state(state):
#     """
#     게임 상태를 설정합니다. (0: 대기, 1: 게임 중)
#     """
#     global current_game_state, game_over_flag, winner_text
#     current_game_state = state
#     if current_game_state == 0:
#         game_over_flag = False
#         winner_text = ""

# def set_game_result(winner):
#     """
#     게임 결과(승자)를 설정합니다.
#     """
#     global game_over_flag, winner_text
#     game_over_flag = True
#     winner_text = winner

# def set_countdown(value):
#     """
#     게임 시작 카운트다운 값을 설정합니다.
#     """
#     global countdown_value
#     countdown_value = value
# # --- 외부에서 호출할 GUI 업데이트 함수들 끝 ---


# # ZMQ 메시지 수신 및 처리 함수 (이제 필요 없으므로 제거)
# # def receive_zmq_messages():
# #     global P1, P2, current_game_state, winner_text, game_over_flag
# #     try:
# #         msg = sub_socket.recv_string(zmq.DONTWAIT)
# #         # print(f"[GUI] ZMQ 메시지 수신: {msg}") # 디버깅용
# #         parts = msg.split(',')
# #         
# #         if len(parts) >= 1:
# #             msg_type = parts[0]
# #
# #             if msg_type == "GAME_STATE_GUI" and len(parts) == 3:
# #                 new_state = int(parts[1])
# #                 hp_parts = parts[2].split(':')
# #                 if len(hp_parts) == 2:
# #                     p1_hp = int(hp_parts[0])
# #                     p2_hp = int(hp_parts[1])
# #                     P1.hp = p1_hp
# #                     P2.hp = p2_hp
# #
# #                 if current_game_state != new_state:
# #                     current_game_state = new_state
# #                     print(f"[GUI] 게임 상태 업데이트: {current_game_state}")
# #                     if current_game_state == 0:
# #                         game_over_flag = False
# #                         winner_text = ""
# #
# #             elif msg_type == "ACTION_GUI" and len(parts) == 3:
# #                 player_role = parts[1]
# #                 action_type = parts[2]
# #
# #                 if action_type == "ATTACK":
# #                     if player_role == "player1":
# #                         P1.attack_animation()
# #                     elif player_role == "player2":
# #                         P2.attack_animation()
# #                 elif action_type == "MOVEMENT": 
# #                     if player_role == "player1":
# #                         P1.movement_animation()
# #                     elif player_role == "player2":
# #                         P2.movement_animation()
# #                 
# #             elif msg_type == "HIT_GUI" and len(parts) == 2:
# #                 hit_player_role = parts[1]
# #                 if hit_player_role == "player1":
# #                     P1.hit_animation()
# #                 elif hit_player_role == "player2":
# #                     P2.hit_animation()
# #
# #             elif msg_type == "GAME_RESULT" and len(parts) == 2:
# #                 game_over_flag = True
# #                 winner_text = parts[1]
# #                 print(f"[GUI] 게임 종료 결과 수신: {winner_text}")
# #
# #     except zmq.Again:
# #         pass # 읽을 메시지가 없으면 발생, 정상 처리
# #     except Exception as e:
# #         print(f"[GUI Error] ZMQ 메시지 처리 오류: {e}")

# # 게임 루프
# # 이 루프는 이제 main.py에서 호출되어야 하므로, gui.py에서는 단순히 함수로 제공
# def run_gui_frame():
#     """
#     GUI의 한 프레임을 업데이트하고 그리는 함수.
#     main.py의 메인 루프에서 호출되어야 합니다.
#     """
#     global game_over_flag, current_game_state, winner_text, countdown_value
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             # 외부에서 gui_running 플래그를 변경하여 종료하도록 할 것
#             # 또는 pygame.quit()을 여기서 직접 호출할 수도 있음
#             # 일단 sys.exit()는 직접 호출하지 않음
#             return False # 루프 종료 신호

#     # 배경 그리기
#     GameDisplay.blit(loaded_images['background'], loaded_images['background'].get_rect())

#     # 플레이어 캐릭터 그리기
#     P1.draw(GameDisplay)
#     P2.draw(GameDisplay)

#     # HP 표시
#     GameDisplay.blit(P1.display_hp(), (10, 10))
#     GameDisplay.blit(P2.display_hp(), (WIDTH - P2.display_hp().get_width() - 10, 10))

#     # 게임 상태에 따른 UI 업데이트
#     if current_game_state == 0: # 게임 대기 및 초기화 중
#         waiting_text = font.render("Waiting for Players...", True, WHITE)
#         text_rect = waiting_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
#         GameDisplay.blit(waiting_text, text_rect)
        
#         # 카운트다운 표시 (게임 시작 전에만)
#         if countdown_value > 0:
#             countdown_text = font.render(str(countdown_value), True, RED)
#             countdown_text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
#             GameDisplay.blit(countdown_text, countdown_text_rect)


#     # 게임 결과 화면 표시
#     if game_over_flag:
#         result_font = pygame.font.SysFont('Malgun Gothic', 50)
#         result_text_render = result_font.render(winner_text, True, BLACK)
#         result_text_rect = result_text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#         GameDisplay.blit(result_text_render, result_text_rect)
            
#     pygame.display.update()
#     FramePerSec.tick(FPS)
    
#     return True # 루프 계속 진행 신호

# # 게임 종료 시 ZMQ 소켓 정리 (이제 필요 없으므로 제거)
# # sub_socket.close()
# # context.term()
# # print("[GUI] ZMQ sockets and context terminated.")

# # pygame.quit() # gui.py는 이제 자체적으로 종료하지 않음
# # sys.exit() # gui.py는 이제 자체적으로 종료하지 않음
import pygame
import sys
import os

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 400
GameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("위대한 2조 동무들의 합동작업")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HP_COLOR = (255, 0, 0) # HP바 색상

# 폰트 설정
try:
    font = pygame.font.SysFont('Malgun Gothic', 30) # 한글 폰트 (Windows 기준)
    hp_font = pygame.font.SysFont('Arial', 24)
except:
    print("Warning: Malgun Gothic or Arial font not found, using default.")
    font = pygame.font.SysFont(None, 30)
    hp_font = pygame.font.SysFont(None, 24)

# 이미지 로드 (현재 스크립트 파일의 디렉토리를 기준으로 images 폴더 지정)
script_dir = os.path.dirname(__file__)
image_dir = os.path.join(script_dir, 'images')

image_files = {
    'background': 'background.png',
    'player1_normal': 'player1_normal.png',
    'player1_attack': 'player1_attack.png',
    'player1_hit': 'player1_hit.png',
    'player1_movement': 'player1_movement.png', 
    'player2_normal': 'player2_normal.png',
    'player2_attack': 'player2_attack.png', 
    'player2_hit': 'player2_hit.png',
    'player2_movement': 'player2_movement.png', 
}

loaded_images = {}

for key, filename in image_files.items():
    path = os.path.join(image_dir, filename)
    img = pygame.image.load(path)
    loaded_images[key] = img

loaded_images['background'] = pygame.transform.scale(loaded_images['background'], (WIDTH, HEIGHT))

player_normal_size = (100 * 2, 100 * 2) 
player_attack_size = (120 * 2, 100 * 2) 
player_movement_size = (110 * 2, 100 * 2) 

loaded_images['player1_normal'] = pygame.transform.scale(loaded_images['player1_normal'], player_normal_size)
loaded_images['player1_attack'] = pygame.transform.scale(loaded_images['player1_attack'], player_attack_size)
loaded_images['player1_hit'] = pygame.transform.scale(loaded_images['player1_hit'], player_normal_size)
loaded_images['player1_movement'] = pygame.transform.scale(loaded_images['player1_movement'], player_movement_size)

loaded_images['player2_normal'] = pygame.transform.scale(loaded_images['player2_normal'], player_normal_size)
loaded_images['player2_attack'] = pygame.transform.scale(loaded_images['player2_attack'], player_attack_size)
loaded_images['player2_hit'] = pygame.transform.scale(loaded_images['player2_hit'], player_normal_size)
loaded_images['player2_movement'] = pygame.transform.scale(loaded_images['player2_movement'], player_movement_size)


# FPS 설정
FPS = 30
FramePerSec = pygame.time.Clock()

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, role):
        super().__init__()
        self.role = role # "player1" or "player2"
        
        self.normal_image = loaded_images[f'{role}_normal']
        self.attack_image = loaded_images[f'{role}_attack']
        self.hit_image = loaded_images[f'{role}_hit']
        self.movement_image = loaded_images[f'{role}_movement'] # MOVEMENT 이미지 속성 추가
        
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hp = 100 # 초기 HP
        
        self.original_x = x # 원래 x 위치 저장
        self.original_y = y # 원래 y 위치 저장

        self.atk_anim_active = False
        self.atk_anim_start_time = 0
        self.atk_anim_duration = 200 # ms
        
        self.hit_anim_active = False
        self.hit_anim_start_time = 0
        self.hit_anim_duration = 300 # ms

        self.mv_anim_active = False
        self.mv_anim_start_time = 0
        self.mv_anim_duration = 200 # ms
        self.mv_distance = 20 # 뒤로 물러나는 거리 (픽셀)

    def display_hp(self):
        hp_text = hp_font.render(f"HP: {self.hp}", True, HP_COLOR)
        return hp_text

    def draw(self, surface):
        current_image = self.image # 현재 애니메이션에 따라 변경될 이미지

        if self.atk_anim_active:
            current_image = self.attack_image
            if pygame.time.get_ticks() - self.atk_anim_start_time > self.atk_anim_duration:
                self.atk_anim_active = False
                self.image = self.normal_image # 애니메이션 종료 후 원본 이미지로 복귀
                self.rect = self.image.get_rect(center=(self.original_x, self.original_y)) # rect 업데이트
        elif self.hit_anim_active:
            current_image = self.hit_image
            if pygame.time.get_ticks() - self.hit_anim_start_time > self.hit_anim_duration:
                self.hit_anim_active = False
                self.image = self.normal_image # 애니메이션 종료 후 원본 이미지로 복귀
                self.rect = self.image.get_rect(center=(self.original_x, self.original_y)) # rect 업데이트
        elif self.mv_anim_active: # MOVEMENT 애니메이션 처리
            current_image = self.movement_image # MOVEMENT 이미지 사용
            current_time = pygame.time.get_ticks()
            if current_time - self.mv_anim_start_time < self.mv_anim_duration:
                # 애니메이션 시간 동안 뒤로 이동
                if self.role == "player1": # P1은 왼쪽, 뒤로 가면 x값이 줄어듦
                    self.rect.center = (self.original_x - self.mv_distance, self.original_y)
                else: # P2는 오른쪽, 뒤로 가면 x값이 늘어남
                    self.rect.center = (self.original_x + self.mv_distance, self.original_y)
            else:
                self.mv_anim_active = False
                self.image = self.normal_image # 애니메이션 종료 시 원본 이미지로 복귀
                self.rect.center = (self.original_x, self.original_y) # 항상 원래 위치
        else: # 어떤 애니메이션도 활성화되어 있지 않을 때
            self.image = self.normal_image # 기본 이미지로 설정 (안전장치)
            self.rect.center = (self.original_x, self.original_y) # 항상 원래 위치

        # 현재 이미지의 rect를 업데이트하여 blit
        # current_image의 rect를 사용하여 그릴 때, 기존 rect의 center를 유지하도록 합니다.
        display_rect = current_image.get_rect(center=self.rect.center)
        surface.blit(current_image, display_rect)

    def attack_animation(self):
        if not self.atk_anim_active:
            self.atk_anim_active = True
            self.atk_anim_start_time = pygame.time.get_ticks()
            self.image = self.attack_image # 즉시 공격 이미지로 변경
        
    def hit_animation(self):
        if not self.hit_anim_active:
            self.hit_anim_active = True
            self.hit_anim_start_time = pygame.time.get_ticks()
            self.image = self.hit_image # 즉시 피격 이미지로 변경

    def movement_animation(self):
        if not self.mv_anim_active:
            self.mv_anim_active = True
            self.mv_anim_start_time = pygame.time.get_ticks()
            self.image = self.movement_image # MOVEMENT 이미지로 변경

# 플레이어 객체 생성 좌표 (사용자 의도대로 유지)
P1 = Player(220, 300, "player1")
P2 = Player(380, 300, "player2")

# 게임 상태 변수
game_over_flag = False
current_game_state = 0 # 0: 대기 및 초기화, 1: 게임 중, 2: 카운트다운 중, 3: 게임 종료 결과 표시
winner_text = ""
countdown_value = 0 # 카운트다운 값 추가
game_end_display_start_time = 0 # 게임 종료 화면 표시 시작 시간

# --- 외부에서 호출할 GUI 업데이트 함수들 ---
def update_hp(p1_hp, p2_hp):
    """
    플레이어 HP를 업데이트합니다.
    """
    P1.hp = p1_hp
    P2.hp = p2_hp

def trigger_action_animation(player_role, action_type):
    """
    플레이어 액션 애니메이션을 트리거합니다.
    """
    if action_type == "ATTACK":
        if player_role == "player1":
            P1.attack_animation()
        elif player_role == "player2":
            P2.attack_animation()
    elif action_type == "MOVEMENT":
        if player_role == "player1":
            P1.movement_animation()
        elif player_role == "player2":
            P2.movement_animation()

def trigger_hit_animation(hit_player_role):
    """
    플레이어 피격 애니메이션을 트리거합니다.
    """
    if hit_player_role == "player1":
        P1.hit_animation()
    elif hit_player_role == "player2":
        P2.hit_animation()

def set_game_state(state):
    """
    게임 상태를 설정합니다. (0: 대기, 1: 게임 중, 2: 카운트다운 중, 3: 게임 종료 결과 표시)
    """
    global current_game_state, game_over_flag, winner_text, countdown_value
    current_game_state = state
    if current_game_state == 0: # 대기 상태로 전환 시 초기화
        game_over_flag = False
        winner_text = ""
        countdown_value = 0
        P1.hp = 100 # HP 초기화
        P2.hp = 100 # HP 초기화
    elif current_game_state == 1: # 게임 중 상태
        game_over_flag = False
        winner_text = ""
        countdown_value = 0

def set_countdown(value):
    """
    게임 시작 카운트다운 값을 설정합니다.
    """
    global countdown_value
    countdown_value = value

def show_game_result(winner):
    """
    게임 결과(승자)를 설정하고 게임 종료 화면 표시를 시작합니다.
    """
    global game_over_flag, winner_text, current_game_state, game_end_display_start_time
    game_over_flag = True
    winner_text = winner
    current_game_state = 3 # 게임 종료 결과 표시 상태
    game_end_display_start_time = pygame.time.get_ticks() # 현재 시간 기록

# 게임 루프
def run_gui_frame():
    """
    GUI의 한 프레임을 업데이트하고 그리는 함수.
    main.py의 메인 루프에서 호출되어야 합니다.
    """
    global game_over_flag, current_game_state, winner_text, countdown_value, game_end_display_start_time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False # 루프 종료 신호

    # 배경 그리기
    GameDisplay.blit(loaded_images['background'], loaded_images['background'].get_rect())

    # 플레이어 캐릭터 그리기
    P1.draw(GameDisplay)
    P2.draw(GameDisplay)

    # HP 표시 (게임 종료 결과 표시 중에도 HP는 보여야 함)
    GameDisplay.blit(P1.display_hp(), (10, 10))
    GameDisplay.blit(P2.display_hp(), (WIDTH - P2.display_hp().get_width() - 10, 10))

    # 게임 상태에 따른 UI 업데이트
    if current_game_state == 0: # 게임 대기 및 초기화 중
        waiting_text = font.render("Waiting for Players...", True, WHITE)
        text_rect = waiting_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        GameDisplay.blit(waiting_text, text_rect)
        
    elif current_game_state == 2: # 카운트다운 중
        countdown_text = font.render(str(countdown_value), True, RED)
        countdown_text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        GameDisplay.blit(countdown_text, countdown_text_rect)

    elif current_game_state == 3: # 게임 종료 결과 표시
        result_font = pygame.font.SysFont('Malgun Gothic', 50)
        result_text_render = result_font.render(winner_text, True, BLACK)
        result_text_rect = result_text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        GameDisplay.blit(result_text_render, result_text_rect)
        
        # 10초 후 자동 초기화를 위해 시간을 확인 (main.py에서 제어하므로 gui에서는 표시만)
        # 이 부분은 main.py에서 show_game_result 호출 후 일정 시간 뒤 set_game_state(0)을 호출하도록 처리

    pygame.display.update()
    FramePerSec.tick(FPS)
    
    return True # 루프 계속 진행 신호
