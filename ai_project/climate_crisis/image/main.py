import pygame
import sys
import random

# 초기화
pygame.init()

# 창 설정
width, height = 1980, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Garbage Collector Game")

# 색깔 정의
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)

# 로봇 캐릭터 설정
robot_size = 180
robot_image = pygame.image.load("ai_project/climate_crisis/image/robot.jpg")  # 주인공 이미지 로드
robot_image = pygame.transform.scale(robot_image, (robot_size, robot_size))  # 이미지 크기 조정
robot_x = width // 2 - robot_size // 2
robot_y = height - robot_size
robot_speed = 10  # 로봇 캐릭터 속도를 높임

# 초기 로봇 위치 저장
initial_robot_x = robot_x
initial_robot_y = robot_y

# 점프 설정
jump_height = 15
jumping = False
jump_count = jump_height

# 쓰레기 설정
garbage_size = 150
garbage_speed = 12  # 쓰레기 속도를 높임
garbage_list = []
garbage_image = pygame.image.load("ai_project/climate_crisis/image/thlagi.jpg")  # 쓰레기 이미지 로드
garbage_image = pygame.transform.scale(garbage_image, (garbage_size, garbage_size))  # 이미지 크기 조정

# 장애물 설정
obstacle_size = 200
obstacle_x = width
obstacle_y = height - obstacle_size
obstacle_speed = 8  # 장애물 속도를 높임
obstacle_image = pygame.image.load("ai_project/climate_crisis/image/pado.jpg")  # 장애물 이미지 로드
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_size, obstacle_size))  # 이미지 크기 조정

# 배경 설정
background_image = pygame.image.load("ai_project/climate_crisis/image/background.jpg")  # 배경 이미지 로드
background_image = pygame.transform.scale(background_image, (width, height))  # 이미지 크기 조정

# 상점 아이템 설정
shop_items = [
    {"name": "장애물 속도 감소", "cost": 50, "effect": 0.8},  # 1번 아이템: 장애물 속도 감소
    {"name": "로봇 속도 증가", "cost": 50, "effect": 1.2},  # 2번 아이템: 로봇 속도 증가
    {"name": "쓰레기 생성량 증가", "cost": 50, "effect": 1.5},  # 3번 아이템: 쓰레기 생성량 증가
]

# 상점 상태 및 선택된 아이템 초기화
shop_open = False
selected_item = None

# 점수 설정
score = 0
target_score = 300

# 폰트 설정
font_path = "ai_project/climate_crisis/image/ChungjuKimSaeng.ttf"
font = pygame.font.Font(font_path, 36)

# 게임 상태 설정
game_active = False
game_over = False

# 시간 설정
clock = pygame.time.Clock()
spawn_timer = pygame.time.get_ticks()
speed_increase_interval = 2000  # 2초마다 속도를 증가시킬지 설정

# 배경 스토리 설정
background_story = [
    "전 세계는 쓰레기로 뒤덮여 있었습니다.",
    "지구는 황폐해져가고 있었습니다.",
    "그러던 어느 날, 로봇 한 대가 이 문제에 도전하기로 했습니다.",
    "로봇은 우주로 떠나 쓰레기를 수거하기 시작했습니다.",
    "지구의 미래는 로봇의 손에 달려있습니다.",
]

# 함수: 다이얼로그 표시
def show_dialog():
    dialog_rect = pygame.Rect(width // 4, height // 4, width // 2, height // 2)
    pygame.draw.rect(screen, white, dialog_rect)
    pygame.draw.rect(screen, blue, dialog_rect, 5)

    title_text = font.render("게임 오버", True, blue)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))

    question_text = font.render("게임을 재시작하시겠습니까?", True, blue)
    screen.blit(question_text, (width // 2 - question_text.get_width() // 2, height // 2 - 20))

    yes_text = font.render("예", True, blue)
    yes_rect = pygame.Rect(
        width // 2 - yes_text.get_width() // 2 - 50, height // 2 + 50, yes_text.get_width() + 20, 40
    )
    pygame.draw.rect(screen, blue, yes_rect, 5)
    screen.blit(yes_text, (width // 2 - yes_text.get_width() // 2 - 45, height // 2 + 55))

    no_text = font.render("아니요", True, blue)
    no_rect = pygame.Rect(
        width // 2 - no_text.get_width() // 2 + 30, height // 2 + 50, no_text.get_width() + 20, 40
    )
    pygame.draw.rect(screen, blue, no_rect, 5)
    screen.blit(no_text, (width // 2 - no_text.get_width() // 2 + 35, height // 2 + 55))

    pygame.display.flip()

    return yes_rect, no_rect

# 함수: 상점 표시
def show_shop():
    shop_rect = pygame.Rect(width // 4, height // 4, width // 2, height // 2)
    pygame.draw.rect(screen, white, shop_rect)
    pygame.draw.rect(screen, blue, shop_rect, 5)

    title_text = font.render("상점", True, blue)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))

    for i, item in enumerate(shop_items, start=1):
        item_text = font.render(f"{i}. {item['name']} - {item['cost']} 쓰레기", True, blue)
        screen.blit(item_text, (width // 4 + 30, height // 3 + 50 * i))

    pygame.display.flip()

# 함수: 아이템 구매
def buy_item(item_index):
    global score, obstacle_speed, robot_speed, garbage_speed
    item = shop_items[item_index]
    if score >= item["cost"]:
        score -= item["cost"]
        if item_index == 0:  # 1번 아이템: 장애물 속도 감소
            obstacle_speed *= item["effect"]
        elif item_index == 1:  # 2번 아이템: 로봇 속도 증가
            robot_speed *= item["effect"]
        elif item_index == 2:  # 3번 아이템: 쓰레기 생성량 증가
            garbage_speed *= item["effect"]

# 배경 스토리 표시 함수
def show_background_story():
    for i, line in enumerate(background_story):
        text_surface = font.render(line, True, blue)
        text_rect = text_surface.get_rect(center=(width // 2, height // 2 + i * 40))
        screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # 스토리를 표시한 후 3초 대기

# 게임 시작 화면 표시 함수
def show_start_screen():
    screen.blit(background_image, (0, 0))  # 배경 그리기
    show_background_story()  # 배경 스토리 표시
    screen.blit(robot_image, (robot_x, robot_y))  # 주인공 그리기
    pygame.display.flip()
    pygame.time.wait(1000)  # 시작 화면을 표시한 후 1초 대기

# 게임 루프
show_start_screen()  # 게임 시작 화면 표시
game_active = True  # 게임 시작

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_p:  # P 키를 눌렀을 때 상점을 열거나 닫음
                shop_open = not shop_open  # 현재 상태의 반대로 설정

    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and robot_x > 0:
            robot_x -= robot_speed
        if keys[pygame.K_RIGHT] and robot_x < width - robot_size:
            robot_x += robot_speed

        # 점프 로직
        if not jumping:
            if keys[pygame.K_SPACE]:
                jumping = True
        else:
            if jump_count >= -jump_height:
                neg = 1
                if jump_count < 0:
                    neg = -1
                robot_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                jumping = False
                jump_count = jump_height

        # 시간이 2초 경과 시 쓰레기 생성 및 속도 증가
        current_time = pygame.time.get_ticks()
        if current_time - spawn_timer > 1000:  # 1초마다 쓰레기 생성
            garbage_x = random.randint(0, width - garbage_size)
            garbage_y = 0  # 위에서 생성
            garbage_list.append((garbage_x, garbage_y))
            spawn_timer = current_time
            obstacle_speed += 0.1  # 2초마다 속도 증가

        # 쓰레기 이동
        for idx, garbage in enumerate(garbage_list):
            garbage_x, garbage_y = garbage
            garbage_y += garbage_speed
            garbage = (garbage_x, garbage_y)
            garbage_list[idx] = garbage
            if garbage_y > height:
                garbage_list.pop(idx)

        # 장애물 이동
        obstacle_x -= obstacle_speed
        if obstacle_x + obstacle_size < 0:
            obstacle_x = width
            obstacle_speed += 0.1  # 2초마다 속도 증가
            obstacle_y = height - obstacle_size - random.randint(0, 100)  # 장애물 높이 랜덤 설정

        # 충돌 검사 - 쓰레기
        for idx, garbage in enumerate(garbage_list):
            if (
                robot_x < garbage[0] + garbage_size
                and robot_x + robot_size > garbage[0]
                and robot_y < garbage[1] + garbage_size
                and robot_y + robot_size > garbage[1]
            ):
                garbage_list.pop(idx)
                score += 1

        # 충돌 검사 - 장애물
        if (
            robot_x < obstacle_x + obstacle_size
            and robot_x + robot_size > obstacle_x
            and robot_y < obstacle_y + obstacle_size
            and robot_y + robot_size > obstacle_y
        ):
            print("게임 오버!")
            game_active = False

        # 게임 승리 조건
        if score >= target_score:
            print("게임 승리!")
            game_active = False

        # 그리기
        screen.blit(background_image, (0, 0))  # 배경 그리기
        screen.blit(robot_image, (robot_x, robot_y))  # 주인공 그리기

        for garbage in garbage_list:
            screen.blit(garbage_image, garbage)  # 쓰레기 이미지 그리기

        screen.blit(obstacle_image, (obstacle_x, obstacle_y))  # 장애물 이미지 그리기

        # 점수 표시
        score_text = font.render(f"Score: {score}/{target_score}", True, blue)
        screen.blit(score_text, (10, 10))
    else:
        if not game_over:
            # 게임 오버 화면 표시
            game_over_text = font.render("게임 오버!", True, (255, 0, 0))
            screen.blit(game_over_text, (width // 2 - 150, height // 2 - 50))

            if shop_open:
                # 상점이 열려있을 때 상점 표시
                show_shop()

                # 아이템 선택
                keys = pygame.key.get_pressed()
                for i, item in enumerate(shop_items):
                    if keys[pygame.K_1] and selected_item is None:
                        selected_item = 0
                    elif keys[pygame.K_2] and selected_item is None:
                        selected_item = 1
                    elif keys[pygame.K_3] and selected_item is None:
                        selected_item = 2

                # 선택된 아이템이 있으면 구매
                if selected_item is not None:
                    buy_item(selected_item)
                    selected_item = None
                    shop_open = False

            else:
                # 다이얼로그 표시
                yes_rect, no_rect = show_dialog()

                # 클릭 이벤트 처리
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:  # 0은 왼쪽 버튼을 나타냄
                    if yes_rect.collidepoint(mouse_pos):
                        # 게임 재시작
                        game_active = True
                        game_over = False
                        score = 0
                        garbage_list = []
                        obstacle_speed = 8
                        obstacle_x = width
                        obstacle_y = height - obstacle_size - random.randint(0, 100)
                        robot_x = initial_robot_x
                        robot_y = initial_robot_y
                    elif no_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            game_over = True

    # 업데이트
    pygame.display.flip()
    clock.tick(30)
