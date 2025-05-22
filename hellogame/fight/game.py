import pygame
from pygame.locals import *
import random, time

Vec = pygame.math.Vector2

pygame.init()

# 초당 프레임 설정
FPS = 60
FramePerSec = pygame.time.Clock()

# 색상 세팅(RGB코드)
RED = (255, 0, 0)
ORANGE = (255, 153, 51)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
SEAGREEN = (60, 179, 113)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VIOLET = (204, 153, 255)
PINK = (255, 153, 153)
BEIGE = (255 , 224 , 196)

# 게임 진행에 필요한 변수들 설정
SPEED = 5  # 게임 진행 속도
SCORE = 0  # 플레이어 점수

# 폰트 설정
font = pygame.font.SysFont('Tahoma', 60)  # 기본 폰트 및 사이즈 설정(폰트1)
small_font = pygame.font.SysFont('Malgun Gothic', 20)  # 작은 사이즈 폰트(폰트2)
game_over = font.render("GG", True, BLACK)  # 게임 종료시 문구

# 게임 배경화면
background = pygame.image.load('../looftop.jpg')  # 배경화면 사진 로드

# 게임 화면 생성 및 설정
GameDisplay = pygame.display.set_mode((640, 440))
GameDisplay.fill(WHITE)
pygame.display.set_caption("Mini Game")



class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.size = 40
        self.body = 80
        self.head = 60
        

        self.y = 240
        self.distance = 0
        self.image = pygame.Surface((self.size * 2, self.size * 2))
        self.color = (48 , 48 , 48) 

        self.waitGame = True
        self.atk = False
        self.isAttack = True
        self.hit = True

        self.all_sprite = pygame.sprite.Group()
        self.rect1 = pygame.rect.Rect([self.head + self.distance, 40 + self.y , 40 , 20])
        self.rect2 = pygame.rect.Rect([self.head  + self.distance, 40 + 20 + self.y , 40 , 20])
        self.rect3 = pygame.rect.Rect([40  + self.distance, 80 + self.y , 80 , 80])
        self.rect4 = pygame.rect.Rect([40  + self.distance, 80 + 80 + self.y , 80 , 60])

        self.hp = 100  # 추가
        self.font = pygame.font.SysFont('Malgun Gothic', 24)

        self.getReady = False
        self.circleDist = self.distance + 140


        self.hit_animation_count = 0  # 몇 단계 진행됐는지
        self.is_being_hit = False
        self.hit_phase = 0
        self.hit_timer = 0

    def draw(self, background):
        if self.waitGame :
            move = 2
            self.distance += move
        if self.distance >= 160:
            self.waitGame = False
            self.getReady = True
        pygame.draw.rect(background, BLACK, [60 + self.distance, 40 + self.y , 40 , 20])
        pygame.draw.rect(background, BEIGE, [60  + self.distance, 40 + 20 + self.y , 40 , 20])
        pygame.draw.rect(background, RED, [40  + self.distance, 80 + self.y , 80 , 80])
        pygame.draw.rect(background, YELLOW , [40  + self.distance, 80 + 80 + self.y , 80 , 60])
        time.sleep(0.005)

    def attack(self , background):
        attackFinish = False
        if self.atk :
            if self.isAttack :
                move = 2
                self.circleDist += move
            if self.circleDist >= 260:
                self.isAttack = False
                self.atk = False
                attackFinish = True
            pygame.draw.circle(background , RED , (60 + self.circleDist + 60, 40 + self.y + 20) , 15)
        return attackFinish
    
    def HIT(self , background):
        self.head -= 2
        pygame.draw.rect(background, BLACK, [self.head + self.distance, 40 + self.y , 40 , 20])
        pygame.draw.rect(background, BEIGE, [self.head  + self.distance, 40 + 20 + self.y , 40 , 20])
        # pygame.time.delay(50)

    def HITBACK(self , background):
        self.head += 2
        pygame.draw.rect(background, BLACK, [self.head + self.distance, 40 + self.y , 40 , 20])
        pygame.draw.rect(background, BEIGE, [self.head  + self.distance, 40 + 20 + self.y , 40 , 20])

    def display_hp(self):
        return self.font.render(f"Player1 HP: {self.hp}", True, WHITE)

    def kill(self):
        self.rect_sprite.kill()
        Sprite.kill(self)

        

class Player2(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 플레이어 사진 불러오기
        # self.image = pygame.image.load('../chick.png')
        self.size = 40
        self.body = 80
        self.head = 60

        self.y = 240
        self.distance = 480
        self.image = pygame.Surface((self.size * 2, self.size * 2))
        self.color = (48 , 48 , 48) 

        self.waitGame = True
        self.atk = False
        self.isAttack = True
        self.hit = True

        self.all_sprite = pygame.sprite.Group()
        self.rect1 = pygame.rect.Rect([self.head + self.distance, 40 + self.y , 40 , 20])
        self.rect2 = pygame.rect.Rect([self.head  + self.distance, 40 + 20 + self.y , 40 , 20])
        self.rect3 = pygame.rect.Rect([40  + self.distance, 80 + self.y , 80 , 80])
        self.rect4 = pygame.rect.Rect([40  + self.distance, 80 + 80 + self.y , 80 , 60])

        self.hp = 100  # 추가
        self.font = pygame.font.SysFont('Malgun Gothic', 24)

        self.getReady = False
        self.circleDist = self.distance - 140

        self.hit_animation_count = 0  # 몇 단계 진행됐는지
        self.is_being_hit = False
        self.hit_phase = 0
        self.hit_timer = 0

    def draw(self, background):
        if self.waitGame :
            move = 2
            self.distance -= move
        if self.distance <= 320:
            self.waitGame = False
            self.getReady = True
        pygame.draw.rect(background, BLACK, [self.head + self.distance, 40 + self.y , 40 , 20])
        pygame.draw.rect(background, BEIGE, [self.head  + self.distance, 40 + 20 + self.y , 40 , 20])
        pygame.draw.rect(background, BLUE, [40  + self.distance, 80 + self.y , 80 , 80])
        pygame.draw.rect(background, YELLOW , [40  + self.distance, 80 + 80 + self.y , 80 , 60])
        time.sleep(0.005)

    def attack(self , background):
        attackFinish = False
        if self.atk :
            if self.isAttack :
                move = 2
                self.circleDist -= move
            if self.circleDist <= 460:
                self.isAttack = False
                self.atk = False
                attackFinish = True
            pygame.draw.circle(background , BLUE , (60 + self.circleDist + 60, 40 + self.y + 20) , 15)
        return attackFinish

    def HIT(self , background):
        self.head += 2
        pygame.draw.rect(background, BLACK, [self.head + self.distance, 40 + self.y , 40 , 20])
        pygame.draw.rect(background, BEIGE, [self.head  + self.distance, 40 + 20 + self.y , 40 , 20])
        # pygame.time.delay(50)

    def HITBACK(self , background):
        self.head -= 2
        pygame.draw.rect(background, BLACK, [self.head + self.distance, 40 + self.y , 40 , 20])
        pygame.draw.rect(background, BEIGE, [self.head  + self.distance, 40 + 20 + self.y , 40 , 20])
        # pygame.time.delay(50)
    def display_hp(self):
        return self.font.render(f"Player2 HP: {self.hp}", True, WHITE)

    def kill(self):
        self.rect_sprite.kill()
        Sprite.kill(self)

            
P1 = Player1()
P2 = Player2()

isPlayer1 = True
isPlayer2 = True

All_groups = pygame.sprite.Group()

if(isPlayer1) :
    All_groups.add(P1)

if(isPlayer2) :
    All_groups.add(P2)


P1.atk = True





# 적 개체 1초(1000ms)마다 새로 생기는 이벤트 생성
increaseSpeed = pygame.USEREVENT + 1
pygame.time.set_timer(increaseSpeed, 1000)

rect = background.get_rect()

# while True: 이후 전체 반복 루프 내부
while True:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == increaseSpeed:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    GameDisplay.blit(background, rect)
    P1.draw(GameDisplay)
    P2.draw(GameDisplay)

    GameDisplay.blit(P1.display_hp(), (10, 10))
    GameDisplay.blit(P2.display_hp(), (500, 10))

    # --- 공격 처리 (P1 → P2) ---
    if P1.getReady and P2.getReady and P1.atk and not P2.is_being_hit:
        isFinish = P1.attack(GameDisplay)
        if isFinish:
            P1.atk = False
            P1.isAttack = True
            P1.circleDist = P1.distance
            P2.hp -= 10
            P2.is_being_hit = True
            P2.hit_phase = 0
            P2.hit_timer = 0

    # --- 공격 처리 (P2 → P1) ---
    if P1.getReady and P2.getReady and P2.atk and not P1.is_being_hit:
        isFinish = P2.attack(GameDisplay)
        if isFinish:
            P2.atk = False
            P2.isAttack = True
            P2.circleDist = P2.distance
            P1.hp -= 10
            P1.is_being_hit = True
            P1.hit_phase = 0
            P1.hit_timer = 0

    # --- P2 피격 애니메이션 ---
    if P2.is_being_hit:
        P2.hit_timer += 1
        if P2.hit_phase < 5:
            if P2.hit_timer % 5 == 0:
                P2.HIT(GameDisplay)
                P2.hit_phase += 1
        elif P2.hit_phase < 10:
            if P2.hit_timer % 5 == 0:
                P2.HITBACK(GameDisplay)
                P2.hit_phase += 1
        else:
            P2.is_being_hit = False
            P2.hit_phase = 0
            P2.hit_timer = 0

    # --- P1 피격 애니메이션 ---
    if P1.is_being_hit:
        P1.hit_timer += 1
        if P1.hit_phase < 5:
            if P1.hit_timer % 5 == 0:
                P1.HIT(GameDisplay)
                P1.hit_phase += 1
        elif P1.hit_phase < 10:
            if P1.hit_timer % 5 == 0:
                P1.HITBACK(GameDisplay)
                P1.hit_phase += 1
        else:
            P1.is_being_hit = False
            P1.hit_phase = 0
            P1.hit_timer = 0

    pygame.display.update()
    FramePerSec.tick(FPS)

    pygame.display.update()

    
