# -*- coding: utf-8 -*-
import pygame
import random

########################################################
# 파이게임 초기설정 (반드시 초기에 세 해야하는 것)
pygame.init()

#화면크기 설정
screen_width = 480 # 가로크기
screen_height = 640 # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 (GUI 제목창)
pygame.display.set_caption("퐁게임")

#FPS
clock = pygame.time.Clock()
########################################################
# 1. 사용자가 추가하는 내용물들 초기화 (배경, 스프라이트, 좌표, 속도, 폰트, 시간 등)

#1-1 우리편 생성
character = pygame.image.load("pygame/source/character.png")
#스프라이트의 크기와 좌표 세팅하기 (움직임을 상정한 설정)
character_size = character.get_rect().size #스프라이트를 사각형 형태로 가로세로 크기 구함
character_width = character_size[0] #위에서 얻은 튜플의 1번째 값. 자동생성
character_height = character_size[1] #위에서 얻은 튜플의 2번째 값. 자동생성.
character_xPos = (screen_width / 2) - (character_width / 2) #화면 가로 정중앙
character_yPos = screen_height - character_height #화면 세로 맨아래

#아군 스프라이트 이동
character_to_x = 0
character_to_y = 0

#1-2 적군 생성
enemy = pygame.image.load("pygame/source/enemy.png")
#적군 스프라이트 크기 및 위치 지정
enemy_size = enemy.get_rect().size #스프라이트를 사각형 형태로 가로세로 크기 구함
enemy_width = enemy_size[0] #위에서 얻은 튜플의 1번째 값. 자동생성
enemy_height = enemy_size[1] #위에서 얻은 튜플의 2번째 값. 자동생성.
enemy_xPos = (screen_width / 2 - enemy_width / 2) #화면 가로 정중앙
enemy_yPos = (screen_height / 2 - enemy_height / 2) #화면 세로 정중앙

#적군 스프라이트 이동
enemy_to_x = 0
enemy_to_y = 0

#1-3 공 생성
ball = pygame.image.load("pygame/source/ball.png")
#공 스프라이트 크기 및 위치 지정
ball_size = ball.get_rect().size #스프라이트를 사각형 형태로 가로세로 크기 구함
ball_width = ball_size[0] #위에서 얻은 튜플의 1번째 값. 자동생성
ball_height = ball_size[1] #위에서 얻은 튜플의 2번째 값. 자동생성.
ball_xPos = (screen_width / 2 - ball_width / 2) #화면 가로 정중앙
ball_yPos = 0 #화면 맨 위

#공 스프라이트 이동
ball_speed_x = 3
ball_speed_y = 3


#이벤트 반복 시작 - 스크래치의 무한반복과 같음
running = True #실행중인지 확인
while running:
    dt = clock.tick(60) #게임화면이 초당 리프레시되는 횟수

    #2 이벤트 처리(키보드 마우스 등 화면조작 관련)
    for event in pygame.event.get(): #키마 이벤트를 지속적으로 체크
        if event.type == pygame.QUIT: #창닫는 이벤트
            running = False
        # 키보드로 캐릭터 움직이기
        if event.type == pygame.KEYDOWN: #키보드 눌림 확인
            if event.key == pygame.K_LEFT: #왼쪽 화살표
                character_to_x -= 1
            elif event.key == pygame.K_RIGHT: #오른쪽 화살표 
                character_to_x += 1

        if event.type == pygame.KEYUP: # 키보드에서 손을 뗐을 때 중지
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: #가로움직임
                character_to_x = 0
        
        mouseX_pos = 0
        mouseY_pos = 0
        # 마우스로 적군 움직이기
        if event.type == pygame.MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()
            mouseX_pos = mousePos[0]
            mouseY_pos = mousePos[1]
            
    # 3. 게임 캐릭터 위치 정의
    #3-1. 캐릭터 위치 정의
    character_xPos += character_to_x * dt
    character_yPos += character_to_y * dt

    #3-2. 캐릭터 범위 한정
    if character_xPos < 0:
        character_xPos = 0
    elif character_xPos > screen_width - character_width:
        character_xPos = screen_width - character_width
    if character_yPos < 0:
        character_yPos = 0
    elif character_yPos > screen_height - character_height:
        character_yPos = screen_height - character_height

    #3-3. 적 위치 정의
    enemy_xPos = mouseX_pos - (enemy_width / 2)
    enemy_yPos = mouseY_pos - (enemy_height / 2)
    
    #3-4. 적 범위 한정
    if enemy_xPos < 0:
        enemy_xPos = 0
    elif enemy_xPos > screen_width - enemy_width:
        enemy_xPos = screen_width - enemy_width
    if enemy_yPos < 0:
        enemy_yPos = 0
    elif enemy_yPos > screen_height - enemy_height:
        enemy_yPos = screen_height - enemy_height

    # 3-5. 공 위치 정의
    ball_xPos += ball_speed_x
    ball_yPos += ball_speed_y

    # 3-6. 공 벽에 닿으면 튕기기
    if ball_xPos <= 0:    
        ball_speed_x *= -1
        ball_speed_x = random.randint(3, 8)

    elif ball_xPos >= screen_width - ball_width:
        ball_speed_x *= -1
        ball_speed_x = -random.randint(3, 8)
    
    if ball_yPos <= 0:
        ball_speed_y *= -1
        ball_speed_y = random.randint(3, 8)

    elif ball_yPos >= screen_height - ball_height:
        ball_speed_y *= -1
        ball_speed_y = -random.randint(3, 8)

    # 5. 화면에 그리기
    screen.fill((255, 255, 255))
    screen.blit(character, (character_xPos, character_yPos))
    screen.blit(enemy, (enemy_xPos, enemy_yPos))
    screen.blit(ball, (ball_xPos, ball_yPos))
    pygame.display.update() # 게임화면을 새로고침해줌.

#종료처리
pygame.quit()
