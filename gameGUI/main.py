from fight import Game

import pygame, sys
from pygame.locals import *
import random, time

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

# 게임 진행에 필요한 변수들 설정
SPEED = 5  # 게임 진행 속도
SCORE = 0  # 플레이어 점수

# 폰트 설정
font = pygame.font.SysFont('Tahoma', 60)  # 기본 폰트 및 사이즈 설정(폰트1)
small_font = pygame.font.SysFont('Malgun Gothic', 20)  # 작은 사이즈 폰트(폰트2)
game_over = font.render("GG", True, BLACK)  # 게임 종료시 문구

# 게임 배경화면
background = pygame.image.load('looftop.jpg')  # 배경화면 사진 로드

# 게임 화면 생성 및 설정
GameDisplay = pygame.display.set_mode((640, 440))
GameDisplay.fill(PINK)
pygame.display.set_caption("Mini Game")

## 게임 내에서 동작할 클래스 설정 ##

## 플레이어에게 적용할 클래스
class Player(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 플레이어 사진 불러오기
        self.image = pygame.image.load('chick.png')
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        print("플레이어: ",self.rect)
        # 이미지 시작 위치 설정
        self.rect.center = (540, 390)

    # 플레이어 키보드움직임 설정 함수
    def move(self):
        prssdKeys = pygame.key.get_pressed()
        # 왼쪽 방향키를 누르면 5만큼 왼쪽 이동
        if self.rect.left > 0:
            if prssdKeys[K_LEFT]:
                self.rect.move_ip(-5, 0)
                position_p = self.rect.center
                return position_p
        # 오른쪽을 누르면 5만큼 오른쪽으로 이동
        if self.rect.right < 640:
            if prssdKeys[K_RIGHT]:
                self.rect.move_ip(5, 0)
                position_p = self.rect.center
                return position_p
## 적에게 적용할 클래스
class Enemy(pygame.sprite.Sprite):

    # 적의 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 적 사진 불러오기
        self.image = pygame.image.load('boom2.png')
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        print("적: ", self.rect)
        # 이미지 시작 위치 설정
        self.rect.center = (random.randint(40, 600), 0)

    # 적의 움직임 설정 함수+ 플레이어 점수 측정
    def move(self):
        global SCORE

        # 적을 10픽셀크기만큼 위에서 아래로 떨어지도록 설정
        self.rect.move_ip(0, SPEED)  # x,y좌표 설정
        # 이미지 가 화면 끝에 있으면(플레이어가 물체를 피하면) 다시 이미지 위치 세팅 + 1점 추가
        if (self.rect.bottom > 440):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 610), 0)
        return self.rect.center
    ###### 게임 설정 ########
# 플레이어 및 적 개체 생성
P1 = Player()

E1 = Enemy()

# Sprites Groups 생성하기
# 게임 물체들을 그룹화 하여 그룹별로 접근하여 설정 시 용이하게 만들기
# 적(enemy) 객체 그룹화하기
Enemies = pygame.sprite.Group()
Enemies.add(E1)
# 전체 그룹을 묶기
All_groups = pygame.sprite.Group()
All_groups.add(P1)
All_groups.add(E1)

# 적 개체 1초(1000ms)마다 새로 생기는 이벤트 생성
increaseSpeed = pygame.USEREVENT + 1
pygame.time.set_timer(increaseSpeed, 1000)

## 게임 루프 설정 ##
# 게임 종료되기 전까지 실행되는 루프(이벤트) 설정
while True:

    for event in pygame.event.get():
        # type increaseSpeed이면 속도 증가하여 어렵게 만듬(적 물체 이벤트)
        if event.type == increaseSpeed:
            SPEED += 0.5
        # 이벤트가 종료되면 게임도 종료시킴
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 배경화면 사진 게임창에 불러오기(사진, 위치)
    GameDisplay.blit(background, (0, 0))
    # 하단부에 위치할 스코어 점수(적을 피할때마다 +1점 증가)
    scores = small_font.render("Score: " + str(SCORE), True, BLACK)
    GameDisplay.blit(scores, (10, 400))

    #group1 = '<Player Sprite(in 1 groups)>'
    #group2 = '<Enemy Sprite(in 2 groups)>'

    # 게임 내 물체 움직임 생성
    for i in All_groups:
        GameDisplay.blit(i.image, i.rect)
        i.move()
        if str(i) == '<Player Sprite(in 1 groups)>':
            player_pos = i
        else:
            enemy_pos = i

# 플레이어 충돌 판정(게임종료)시
    if pygame.sprite.spritecollideany(P1, Enemies):
        for i in All_groups:
            i.kill()
        # 물체 이미지 변경(충돌후 변경되는 이미지)
        # 플레이어
        GameDisplay.blit(background, (0, 0))
        image0 = pygame.image.load('chickbommed.png')
        image0.get_rect()
        GameDisplay.blit(image0, player_pos)

        # 폭탄
        image1 = pygame.image.load('boomm.png')
        image1.get_rect()
        GameDisplay.blit(image1, enemy_pos)
        pygame.display.update()

        # 게임오버화면 설정
        pygame.mixer.Sound('gameover.mp3').play()
        GameDisplay.fill(SEAGREEN)
        final_scores = font.render("Your Score: " + str(SCORE), True, BLACK)
        GameDisplay.blit(final_scores, (150, 100))
        GameDisplay.blit(game_over, (280, 200))
        time.sleep(1)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    # 초당 프레임 설정
    FramePerSec.tick(FPS)
    