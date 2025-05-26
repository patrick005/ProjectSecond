# # test_gui.py - 게임 시나리오 테스트용 GUI
# import pygame
# import sys
# import os
# import random # 테스트를 위한 무작위 HP 감소 추가 (옵션)

# # 초기화
# pygame.init()

# # 화면 설정
# WIDTH, HEIGHT = 600, 400
# GameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("게임 시나리오 테스트 GUI")

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
#     instruction_font = pygame.font.SysFont('Arial', 18)
# except:
#     print("Warning: Malgun Gothic or Arial font not found, using default.")
#     font = pygame.font.SysFont(None, 30)
#     hp_font = pygame.font.SysFont(None, 24)
#     instruction_font = pygame.font.SysFont(None, 18)

# # 이미지 로드 (현재 스크립트 파일의 디렉토리를 기준으로 images 폴더 지정)
# script_dir = os.path.dirname(__file__)
# image_dir = os.path.join(script_dir, 'images')

# # 이미지 파일 이름 리스트 (movement 이미지 추가)
# image_files = {
#     'background': 'background.png',
#     'player1_normal': 'player1_normal.png',
#     'player1_attack': 'player1_attack.png',
#     'player1_hit': 'player1_hit.png',
#     'player1_movement': 'player1_movement.png', # MOVEMENT 이미지 추가
#     'player2_normal': 'player2_normal.png',
#     'player2_attack': 'player2_attack.png', # player2_attack.png가 있다고 가정, 없으면 player1_attack 사용
#     'player2_hit': 'player2_hit.png',
#     'player2_movement': 'player2_movement.png', # MOVEMENT 이미지 추가
# }

# # 로드된 이미지 저장 딕셔너리
# loaded_images = {}

# try:
#     for key, filename in image_files.items():
#         path = os.path.join(image_dir, filename)
#         img = pygame.image.load(path)
#         loaded_images[key] = img

#     # 이미지 크기 조정 (200% 스케일 적용)
#     loaded_images['background'] = pygame.transform.scale(loaded_images['background'], (WIDTH, HEIGHT))
    
#     # 플레이어 이미지 크기 정의 (기존 100% 기준에서 200%로 변경)
#     player_normal_size = (100 * 2, 100 * 2) # 200%
#     player_attack_size = (120 * 2, 100 * 2) # 200%
#     player_movement_size = (110 * 2, 100 * 2) # 200%

#     # Player1 이미지 크기 조정
#     loaded_images['player1_normal'] = pygame.transform.scale(loaded_images['player1_normal'], player_normal_size)
#     loaded_images['player1_attack'] = pygame.transform.scale(loaded_images['player1_attack'], player_attack_size)
#     loaded_images['player1_hit'] = pygame.transform.scale(loaded_images['player1_hit'], player_normal_size)
#     loaded_images['player1_movement'] = pygame.transform.scale(loaded_images['player1_movement'], player_movement_size)

# except pygame.error as e:
#     print(f"이미지 로드 오류: {e}")
#     print(f"이미지 파일이 '{image_dir}' 폴더에 있고, 이름이 올바른지 확인해주세요.")
#     # 오류 발생 시 기본 색상으로 대체
#     loaded_images['background'] = pygame.Surface((WIDTH, HEIGHT)); loaded_images['background'].fill(BLUE)
#     loaded_images['player1_normal'] = pygame.Surface(player_normal_size); loaded_images['player1_normal'].fill(RED)
#     loaded_images['player1_attack'] = pygame.Surface(player_attack_size); loaded_images['player1_attack'].fill(RED)
#     loaded_images['player1_hit'] = pygame.Surface(player_normal_size); loaded_images['player1_hit'].fill(RED)
#     loaded_images['player1_movement'] = pygame.Surface(player_movement_size); loaded_images['player1_movement'].fill(RED)
#     loaded_images['player2_normal'] = pygame.Surface(player_normal_size); loaded_images['player2_normal'].fill(GREEN)
#     loaded_images['player2_attack'] = pygame.Surface(player_attack_size); loaded_images['player2_attack'].fill(GREEN)
#     loaded_images['player2_hit'] = pygame.Surface(player_normal_size); loaded_images['player2_hit'].fill(GREEN)
#     loaded_images['player2_movement'] = pygame.Surface(player_movement_size); loaded_images['player2_movement'].fill(GREEN)


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
#         self.mv_distance = 200 # 뒤로 물러나는 거리 (픽셀)

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
#                 self.rect.center = (self.original_x, self.original_y)
#         elif self.hit_anim_active:
#             current_image = self.hit_image
#             if pygame.time.get_ticks() - self.hit_anim_start_time > self.hit_anim_duration:
#                 self.hit_anim_active = False
#                 self.image = self.normal_image # 애니메이션 종료 후 원본 이미지로 복귀
#                 self.rect.center = (self.original_x, self.original_y)
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
#                 self.rect.center = (self.original_x, self.original_y)
#         else: # 어떤 애니메이션도 활성화되어 있지 않을 때
#             self.image = self.normal_image # 기본 이미지로 설정 (안전장치)
#             self.rect.center = (self.original_x, self.original_y) # 항상 원래 위치

#         # 현재 이미지의 rect를 업데이트하여 blit
#         self.rect = current_image.get_rect(center=self.rect.center) # 이미지 변경 시 rect 크기 업데이트
#         surface.blit(current_image, self.rect)

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

# # 플레이어 객체 생성 좌표
# P1 = Player(250, 300, "player1")
# P2 = Player(350, 300, "player2")

# # 게임 상태 변수 (gui.py와 동일한 명칭 사용)
# game_over_flag = False
# current_game_state = 0 # 0: 대기 및 초기화, 1: 게임 중
# winner_text = ""

# # 게임 상태 업데이트 함수 (ZMQ 대신 직접 호출)
# def update_game_state_and_hp(state_flag, p1_hp, p2_hp):
#     global current_game_state, game_over_flag, winner_text
#     P1.hp = max(0, p1_hp)
#     P2.hp = max(0, p2_hp)
#     current_game_state = state_flag
#     print(f"[Test GUI] 게임 상태 업데이트: {current_game_state}, P1 HP: {P1.hp}, P2 HP: {P2.hp}")
#     if current_game_state == 0: # 대기 상태로 전환 시 게임 오버 플래그 및 결과 텍스트 초기화
#         game_over_flag = False
#         winner_text = ""

# # 액션 트리거 함수 (ZMQ 대신 직접 호출)
# def trigger_action(player_role, action_type):
#     if player_role == "player1":
#         player_obj = P1
#     elif player_role == "player2":
#         player_obj = P2
#     else:
#         return

#     if action_type == "ATTACK":
#         player_obj.attack_animation()
#         print(f"[Test GUI] {player_role} ATTACK 애니메이션 트리거")
#     elif action_type == "MOVEMENT":
#         player_obj.movement_animation()
#         print(f"[Test GUI] {player_role} MOVEMENT 애니메이션 트리거")

# # 피격 트리거 함수 (ZMQ 대신 직접 호출)
# def trigger_hit(hit_player_role):
#     if hit_player_role == "player1":
#         P1.hit_animation()
#         print(f"[Test GUI] {hit_player_role} HIT 애니메이션 트리거")
#     elif hit_player_role == "player2":
#         P2.hit_animation()
#         print(f"[Test GUI] {hit_player_role} HIT 애니메이션 트리거")

# # 게임 결과 트리거 함수 (ZMQ 대신 직접 호출)
# def trigger_game_result(result):
#     global game_over_flag, winner_text
#     game_over_flag = True
#     winner_text = result
#     update_game_state_and_hp(0, P1.hp, P2.hp) # 결과 표시 후 대기 상태로 전환
#     print(f"[Test GUI] 게임 결과: {result}")

# # 게임 초기화
# def reset_game():
#     global P1, P2, game_over_flag, current_game_state, winner_text
#     P1.hp = 100
#     P2.hp = 100
#     game_over_flag = False
#     current_game_state = 0
#     winner_text = ""
#     print("[Test GUI] 게임 상태 초기화 완료. 대기 중.")

# # 게임 시작
# def start_game():
#     global P1, P2
#     P1.hp = 100
#     P2.hp = 100
#     update_game_state_and_hp(1, P1.hp, P2.hp)
#     print("[Test GUI] 게임 시작. 플레이어 HP 초기화.")

# # 명령어 안내 텍스트
# instructions = [
#     "Press 1: P1 ATTACK      Press 2: P2 ATTACK",
#     "Press 3: P1 MOVEMENT    Press 4: P2 MOVEMENT",
#     "Press H: P1 HIT         Press J: P2 HIT",
#     "Press S: Game Start     Press R: Game Reset",
#     "Press W: P1 Wins        Press L: P2 Wins",
#     "Press D: Draw           Press Q or ESC: Quit"
# ]

# # 게임 루프
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
        
#         # 키보드 입력 처리
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
#                 running = False
#             elif event.key == pygame.K_1: # P1 공격
#                 trigger_action("player1", "ATTACK")
#             elif event.key == pygame.K_2: # P2 공격
#                 trigger_action("player2", "ATTACK")
#             elif event.key == pygame.K_3: # P1 이동
#                 trigger_action("player1", "MOVEMENT")
#             elif event.key == pygame.K_4: # P2 이동
#                 trigger_action("player2", "MOVEMENT")
#             elif event.key == pygame.K_h: # P1 피격
#                 if current_game_state == 1: # 게임 진행 중일 때만 피격 처리
#                     P1.hp -= 10
#                     trigger_hit("player1")
#                     update_game_state_and_hp(1, P1.hp, P2.hp)
#                     if P1.hp <= 0: # HP 0 이하 시 게임 종료 처리
#                         trigger_game_result("Player2 Wins!")
#             elif event.key == pygame.K_j: # P2 피격
#                 if current_game_state == 1: # 게임 진행 중일 때만 피격 처리
#                     P2.hp -= 10
#                     trigger_hit("player2")
#                     update_game_state_and_hp(1, P1.hp, P2.hp)
#                     if P2.hp <= 0: # HP 0 이하 시 게임 종료 처리
#                         trigger_game_result("Player1 Wins!")
#             elif event.key == pygame.K_s: # 게임 시작
#                 start_game()
#             elif event.key == pygame.K_r: # 게임 초기화
#                 reset_game()
#             elif event.key == pygame.K_w: # P1 승리 (테스트용)
#                 P2.hp = 0 # 강제로 P2 HP 0
#                 update_game_state_and_hp(1, P1.hp, P2.hp)
#                 trigger_game_result("Player1 Wins!")
#             elif event.key == pygame.K_l: # P2 승리 (테스트용)
#                 P1.hp = 0 # 강제로 P1 HP 0
#                 update_game_state_and_hp(1, P1.hp, P2.hp)
#                 trigger_game_result("Player2 Wins!")
#             elif event.key == pygame.K_d: # 무승부 (테스트용)
#                 P1.hp = 0
#                 P2.hp = 0
#                 update_game_state_and_hp(1, P1.hp, P2.hp)
#                 trigger_game_result("Draw!")
            
#     GameDisplay.blit(loaded_images['background'], loaded_images['background'].get_rect()) # 배경 그리기

#     # 플레이어 캐릭터 그리기
#     P1.draw(GameDisplay)
#     P2.draw(GameDisplay)

#     # HP 표시
#     GameDisplay.blit(P1.display_hp(), (10, 10))
#     GameDisplay.blit(P2.display_hp(), (WIDTH - P2.display_hp().get_width() - 10, 10))

#     # 게임 상태에 따른 UI 업데이트
#     if current_game_state == 0: # 게임 대기 및 초기화 중
#         waiting_text = font.render("Waiting for Commands...", True, WHITE)
#         text_rect = waiting_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
#         GameDisplay.blit(waiting_text, text_rect)
        
#     # 게임 결과 화면 표시
#     if game_over_flag:
#         result_font = pygame.font.SysFont('Malgun Gothic', 50)
#         result_text_render = result_font.render(winner_text, True, BLACK)
#         result_text_rect = result_text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#         GameDisplay.blit(result_text_render, result_text_rect)

#     # 명령어 안내 표시
#     y_offset = HEIGHT - 20 - len(instructions) * 20 # 화면 하단에 위치
#     for i, line in enumerate(instructions):
#         instruction_text = instruction_font.render(line, True, WHITE)
#         instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, y_offset + i * 20))
#         GameDisplay.blit(instruction_text, instruction_rect)
            
#     pygame.display.update()
#     FramePerSec.tick(FPS)

# pygame.quit()
# sys.exit()
# test_gui.py - 게임 시나리오 테스트용 GUI
import pygame
import sys
import os
import random # 테스트를 위한 무작위 HP 감소 추가 (옵션)

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 400
GameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("게임 시나리오 테스트 GUI")

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
    instruction_font = pygame.font.SysFont('Arial', 18)
except:
    print("Warning: Malgun Gothic or Arial font not found, using default.")
    font = pygame.font.SysFont(None, 30)
    hp_font = pygame.font.SysFont(None, 24)
    instruction_font = pygame.font.SysFont(None, 18)

# 이미지 로드 (현재 스크립트 파일의 디렉토리를 기준으로 images 폴더 지정)
script_dir = os.path.dirname(__file__)
image_dir = os.path.join(script_dir, 'images')

# 이미지 파일 이름 리스트 (movement 이미지 추가)
image_files = {
    'background': 'background.png',
    'player1_normal': 'player1_normal.png',
    'player1_attack': 'player1_attack.png',
    'player1_hit': 'player1_hit.png',
    'player1_movement': 'player1_movement.png', # MOVEMENT 이미지 추가
    'player2_normal': 'player2_normal.png',
    'player2_attack': 'player2_attack.png',
    'player2_hit': 'player2_hit.png',
    'player2_movement': 'player2_movement.png', # MOVEMENT 이미지 추가
}

# 로드된 이미지 저장 딕셔너리
loaded_images = {}

# 이미지 로드 및 크기 조정 (200% 스케일 적용)
# try-except 블록 제거: 사용자님의 피드백에 따라 파일이 항상 존재한다고 가정
for key, filename in image_files.items():
    path = os.path.join(image_dir, filename)
    img = pygame.image.load(path)
    loaded_images[key] = img

loaded_images['background'] = pygame.transform.scale(loaded_images['background'], (WIDTH, HEIGHT))

# 플레이어 이미지 크기 정의 (기존 100% 기준에서 200%로 변경)
player_normal_size = (100 * 2, 100 * 2) # 200%
player_attack_size = (120 * 2, 100 * 2) # 200%
player_movement_size = (110 * 2, 100 * 2) # 200%

# Player1 이미지 크기 조정
loaded_images['player1_normal'] = pygame.transform.scale(loaded_images['player1_normal'], player_normal_size)
loaded_images['player1_attack'] = pygame.transform.scale(loaded_images['player1_attack'], player_attack_size)
loaded_images['player1_hit'] = pygame.transform.scale(loaded_images['player1_hit'], player_normal_size)
loaded_images['player1_movement'] = pygame.transform.scale(loaded_images['player1_movement'], player_movement_size)

# Player2 이미지 크기 조정 (flip 제거)
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
        self.mv_distance = 20 # 뒤로 물러나는 거리 (픽셀) - 원래 의도대로 200% 스케일이어도 20 유지

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
                self.rect.center = (self.original_x, self.original_y) # rect 업데이트
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

# 게임 상태 변수 (gui.py와 동일한 명칭 사용)
game_over_flag = False
current_game_state = 0 # 0: 대기 및 초기화, 1: 게임 중
winner_text = ""

# 게임 상태 업데이트 함수 (ZMQ 대신 직접 호출)
def update_game_state_and_hp(state_flag, p1_hp, p2_hp):
    global current_game_state, game_over_flag, winner_text
    P1.hp = max(0, p1_hp)
    P2.hp = max(0, p2_hp)
    current_game_state = state_flag
    print(f"[Test GUI] 게임 상태 업데이트: {current_game_state}, P1 HP: {P1.hp}, P2 HP: {P2.hp}")
    if current_game_state == 0: # 대기 상태로 전환 시 게임 오버 플래그 및 결과 텍스트 초기화
        game_over_flag = False
        winner_text = ""

# 액션 트리거 함수 (ZMQ 대신 직접 호출)
def trigger_action(player_role, action_type):
    if player_role == "player1":
        player_obj = P1
    elif player_role == "player2":
        player_obj = P2
    else:
        return

    if action_type == "ATTACK":
        player_obj.attack_animation()
        print(f"[Test GUI] {player_role} ATTACK 애니메이션 트리거")
    elif action_type == "MOVEMENT":
        player_obj.movement_animation()
        print(f"[Test GUI] {player_role} MOVEMENT 애니메이션 트리거")

# 피격 트리거 함수 (ZMQ 대신 직접 호출)
def trigger_hit(hit_player_role):
    if hit_player_role == "player1":
        P1.hit_animation()
        print(f"[Test GUI] {hit_player_role} HIT 애니메이션 트리거")
    elif hit_player_role == "player2":
        P2.hit_animation()
        print(f"[Test GUI] {hit_player_role} HIT 애니메이션 트리거")

# 게임 결과 트리거 함수 (ZMQ 대신 직접 호출)
def trigger_game_result(result):
    global game_over_flag, winner_text
    game_over_flag = True
    winner_text = result
    update_game_state_and_hp(0, P1.hp, P2.hp) # 결과 표시 후 대기 상태로 전환
    print(f"[Test GUI] 게임 결과: {result}")

# 게임 초기화
def reset_game():
    global P1, P2, game_over_flag, current_game_state, winner_text
    P1.hp = 100
    P2.hp = 100
    game_over_flag = False
    current_game_state = 0
    winner_text = ""
    print("[Test GUI] 게임 상태 초기화 완료. 대기 중.")

# 게임 시작
def start_game():
    global P1, P2
    P1.hp = 100
    P2.hp = 100
    update_game_state_and_hp(1, P1.hp, P2.hp)
    print("[Test GUI] 게임 시작. 플레이어 HP 초기화.")

# 명령어 안내 텍스트
instructions = [
    "Press 1: P1 ATTACK      Press 2: P2 ATTACK",
    "Press 3: P1 MOVEMENT    Press 4: P2 MOVEMENT",
    "Press H: P1 HIT         Press J: P2 HIT",
    "Press S: Game Start     Press R: Game Reset",
    "Press W: P1 Wins        Press L: P2 Wins",
    "Press D: Draw           Press Q or ESC: Quit"
]

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 키보드 입력 처리
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_1: # P1 공격
                trigger_action("player1", "ATTACK")
            elif event.key == pygame.K_2: # P2 공격
                trigger_action("player2", "ATTACK")
            elif event.key == pygame.K_3: # P1 이동
                trigger_action("player1", "MOVEMENT")
            elif event.key == pygame.K_4: # P2 이동
                trigger_action("player2", "MOVEMENT")
            elif event.key == pygame.K_h: # P1 피격
                if current_game_state == 1: # 게임 진행 중일 때만 피격 처리
                    P1.hp -= 10
                    trigger_hit("player1")
                    update_game_state_and_hp(1, P1.hp, P2.hp)
                    if P1.hp <= 0: # HP 0 이하 시 게임 종료 처리
                        trigger_game_result("Player2 Wins!")
            elif event.key == pygame.K_j: # P2 피격
                if current_game_state == 1: # 게임 진행 중일 때만 피격 처리
                    P2.hp -= 10
                    trigger_hit("player2")
                    update_game_state_and_hp(1, P1.hp, P2.hp)
                    if P2.hp <= 0: # HP 0 이하 시 게임 종료 처리
                        trigger_game_result("Player1 Wins!")
            elif event.key == pygame.K_s: # 게임 시작
                start_game()
            elif event.key == pygame.K_r: # 게임 초기화
                reset_game()
            elif event.key == pygame.K_w: # P1 승리 (테스트용)
                P2.hp = 0 # 강제로 P2 HP 0
                update_game_state_and_hp(1, P1.hp, P2.hp)
                trigger_game_result("Player1 Wins!")
            elif event.key == pygame.K_l: # P2 승리 (테스트용)
                P1.hp = 0 # 강제로 P1 HP 0
                update_game_state_and_hp(1, P1.hp, P2.hp)
                trigger_game_result("Player2 Wins!")
            elif event.key == pygame.K_d: # 무승부 (테스트용)
                P1.hp = 0
                P2.hp = 0
                update_game_state_and_hp(1, P1.hp, P2.hp)
                trigger_game_result("Draw!")
            
    GameDisplay.blit(loaded_images['background'], loaded_images['background'].get_rect()) # 배경 그리기

    # 플레이어 캐릭터 그리기
    P1.draw(GameDisplay)
    P2.draw(GameDisplay)

    # HP 표시
    GameDisplay.blit(P1.display_hp(), (10, 10))
    GameDisplay.blit(P2.display_hp(), (WIDTH - P2.display_hp().get_width() - 10, 10))

    # 게임 상태에 따른 UI 업데이트
    if current_game_state == 0: # 게임 대기 및 초기화 중
        waiting_text = font.render("Waiting for Commands...", True, WHITE)
        text_rect = waiting_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        GameDisplay.blit(waiting_text, text_rect)
        
    # 게임 결과 화면 표시
    if game_over_flag:
        result_font = pygame.font.SysFont('Malgun Gothic', 50)
        result_text_render = result_font.render(winner_text, True, BLACK)
        result_text_rect = result_text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        GameDisplay.blit(result_text_render, result_text_rect)

    # 명령어 안내 표시
    y_offset = HEIGHT - 20 - len(instructions) * 20 # 화면 하단에 위치
    for i, line in enumerate(instructions):
        instruction_text = instruction_font.render(line, True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, y_offset + i * 20))
        GameDisplay.blit(instruction_text, instruction_rect)
            
    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()
sys.exit()
