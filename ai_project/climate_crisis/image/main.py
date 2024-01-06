import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Survival Jump")

# 색상 정의
white = (255, 255, 255)

# 주인공 설정
player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - player_size * 2
player_speed = 5

# 떠다니는 조각 설정
platform_width = 100
platform_height = 20
platform_speed = 5

# 맵 설정
current_map = [
    (100, screen_height - 100, platform_width, platform_height),
    # 현재 맵의 요소들을 정의합니다.
]

def draw_map(map_elements):
    for element in map_elements:
        pygame.draw.rect(screen, (0, 0, 255), element)

# 게임 루프
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += player_speed

    # 화면 업데이트
    screen.fill(white)

    # 플레이어 그리기
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_size, player_size))

    # 맵 그리기
    draw_map(current_map)

    # 다음 맵으로 이동
    if player_x > screen_width:
        # 현재 맵을 비우고 다음 맵으로 이동하는 로직을 추가
        current_map = []  # 비우기 (다음 맵으로 이동할 때 필요한 요소들을 추가)
        player_x = 0  # 왼쪽 끝에서 시작

    pygame.display.flip()

    # 프레임 설정
    clock.tick(30)
