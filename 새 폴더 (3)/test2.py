import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
pygame.init()
clock = pygame.time.Clock()
FPS = 60
screen_image_y = 585
player_money = 100

# 맵 이미지 로드 및 스케일
screen_image = pygame.image.load("screenimage.png")
screen_image = pygame.transform.scale(screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

screen_image2 = pygame.image.load("screenimage2.png")
screen_image2 = pygame.transform.scale(screen_image2, (SCREEN_WIDTH, SCREEN_HEIGHT))

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 36)
is_minigame = False  # 미니게임 실행 상태

class Animated(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Animated, self).__init__()
        size = (100, 80)
        self.front_images = [
            pygame.image.load("front1.png"),
            pygame.image.load("front2.png"),
            pygame.image.load("front3.png")
        ]
        self.right_images = [
            pygame.image.load("right1.png"),
            pygame.image.load("right2.png"),
            pygame.image.load("right3.png")
        ]
        self.left_images = [pygame.transform.flip(img, True, False) for img in self.right_images]
        
        self.rect = pygame.Rect(position, size)
        self.images = [pygame.transform.scale(img, size) for img in self.front_images]
        self.direction = 'front'
        self.state = 0
        self.index = 0
        self.image = self.images[self.index]
        
        self.animation_time = 0.1
        self.current_time = 0
        self.speed_x = 0

    def update(self, mt):
        if self.direction == 'front':
            self.images = self.front_images
        elif self.direction == 'right':
            self.images = self.right_images
            self.speed_x = 2
        elif self.direction == 'left':
            self.images = self.left_images
            self.speed_x = -2
        
        self.current_time += mt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = pygame.transform.scale(self.images[self.index], (100, 80))
        self.rect.x += self.speed_x
        if self.rect.left < 0:  
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:  
            self.rect.right = SCREEN_WIDTH

def main_game():
    global player_money, is_minigame
    player = Animated(position=(100, screen_image_y))
    all_sprites = pygame.sprite.Group(player)

    # 오브젝트 이미지 및 위치 설정
    home_image = pygame.image.load("home.png")
    home_image = pygame.transform.scale(home_image, (100, 100))
    home_rect = home_image.get_rect(topleft=(500, screen_image_y))

    exit_image = pygame.image.load("exit.png")
    exit_image = pygame.transform.scale(exit_image, (100, 100))
    exit_rect = exit_image.get_rect(topleft=(500, screen_image_y))

    object_image = pygame.image.load("object.png")
    object_image = pygame.transform.scale(object_image, (100, 100))
    object_rect = object_image.get_rect(topleft=(700, screen_image_y))

    current_map = 1
    timer_duration = 120  # 타이머 2분
    start_ticks = pygame.time.get_ticks()
    collision_occurred = False
    choice_made = False

    running = True
    while running:
        mt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.direction = "right"
                    player.state = 1
                elif event.key == pygame.K_LEFT:
                    player.direction = "left"
                    player.state = 1
                elif collision_occurred and not choice_made:
                    if event.key == pygame.K_y:
                        if current_map == 1:
                            if player.rect.colliderect(object_rect):
                                is_minigame = True  # 미니게임으로 전환
                                return
                            else:
                                current_map = 2  # 맵 전환
                        elif current_map == 2:
                            current_map = 1  # 원래 맵으로 복귀
                        choice_made = True  # 선택이 완료됨을 표시
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.direction = "front"
                    player.state = 0
                    player.speed_x = 0

        all_sprites.update(mt)

        # 시간 계산
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, timer_duration - int(elapsed_seconds))
        if remaining_time > 0:
            timer_text = font.render(f"Time Left: {remaining_time // 60}:{remaining_time % 60:02}", True, (70, 80, 90))
        else:
            end_text = font.render("Time Over", True, (70, 80, 90))
            SCREEN.blit(end_text, (SCREEN_WIDTH / 2 - end_text.get_width() // 2, SCREEN_HEIGHT / 2 - end_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        # 맵 표시
        if current_map == 1:
            SCREEN.blit(screen_image, (0, 0))
            SCREEN.blit(home_image, home_rect.topleft)
            SCREEN.blit(object_image, object_rect.topleft)
        else:
            SCREEN.blit(screen_image2, (0, 0))
            SCREEN.blit(exit_image, exit_rect.topleft)

        # 충돌 감지 (home, exit, 또는 object와 플레이어)
        if current_map == 1 and player.rect.colliderect(home_rect):
            collision_occurred = True
            if not choice_made:
                choice_text = font.render("Press Y to enter the house.", True, (60, 70, 80))
                SCREEN.blit(choice_text, (SCREEN_WIDTH / 2 - choice_text.get_width() // 2, SCREEN_HEIGHT / 2))
        elif current_map == 1 and player.rect.colliderect(object_rect):
            collision_occurred = True
            if not choice_made:
                choice_text = font.render("Press Y for MiniGame.", True, (60, 70, 80))
                SCREEN.blit(choice_text, (SCREEN_WIDTH / 2 - choice_text.get_width() // 2, SCREEN_HEIGHT / 2))
        elif current_map == 2 and player.rect.colliderect(exit_rect):
            collision_occurred = True
            if not choice_made:
                choice_text = font.render("Press Y to exit the house.", True, (60, 70, 80))
                SCREEN.blit(choice_text, (SCREEN_WIDTH / 2 - choice_text.get_width() // 2, SCREEN_HEIGHT / 2))
        else:
            collision_occurred = False
            choice_made = False

        # 돈 출력
        money_text = font.render(f"Money: ${player_money}", True, (255, 255, 0))
        SCREEN.blit(money_text, (10, 10))
        # 타이머와 스프라이트 업데이트
        SCREEN.blit(timer_text, (SCREEN_WIDTH - 200, 20))
        all_sprites.draw(SCREEN)
        pygame.display.update()

# 미니게임 함수
def mini_game():
    global is_minigame
    mini_game_time = 5  # 미니게임 시간 (5초)
    start_ticks = pygame.time.get_ticks()

    while is_minigame:
        SCREEN.fill((100, 50, 150))  # 미니게임 배경 색
        remaining_time = mini_game_time - (pygame.time.get_ticks() - start_ticks) / 1000
        mini_text = font.render(f"MiniGame: {remaining_time:.1f} seconds left", True, (255, 255, 255))
        SCREEN.blit(mini_text, (SCREEN_WIDTH / 2 - mini_text.get_width() / 2, SCREEN_HEIGHT / 2))

        if remaining_time <= 0:
            is_minigame = False  # 미니게임 종료 후 메인 게임으로 복귀

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

# 메인 실행 루프
while True:
    if is_minigame:
        mini_game()  # 미니게임 실행
    else:
        main_game()  # 메인 게임 실행
