import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
pygame.init()
clock = pygame.time.Clock()
FPS = 60

# 배경 이미지 설정
screen_image = pygame.image.load("screenimage.png")
screen_image = pygame.transform.scale(screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 폰트 설정
font = pygame.font.Font(None, 36)  # 기본 폰트, 크기 36

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
        self.velocity_x = 0

    def update(self, mt):
        if self.direction == 'front':
            self.images = self.front_images
        elif self.direction == 'right':
            self.images = self.right_images
            self.velocity_x = 2
        elif self.direction == 'left':
            self.images = self.left_images
            self.velocity_x = -2

        self.current_time += mt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = pygame.transform.scale(self.images[self.index], (100, 80))
        self.rect.x += self.velocity_x
        if self.rect.left < 0:  
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:  
            self.rect.right = SCREEN_WIDTH

def main():
    player = Animated(position=(100, 585))
    all_sprites = pygame.sprite.Group(player)

    # 타이머 설정 (10분 = 600초)
    timer_duration = 600  # 10분을 초로 변환
    start_ticks = pygame.time.get_ticks()  # 시작 시간 기록

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
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.direction = "front"
                    player.state = 0
                    player.velocity_x = 0

        all_sprites.update(mt)

        # 남은 시간 계산
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, timer_duration - int(elapsed_seconds))

        # 타이머 텍스트 생성
        if remaining_time > 0:
            timer_text = font.render(f"Time Left: {remaining_time // 60}:{remaining_time % 60:02}", True, (70, 80, 90))
        else:
            timer_text = font.render("시간 종료", True, (70, 80, 90))
            SCREEN.blit(timer_text, (SCREEN_WIDTH - 200, 20))
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        # 배경 화면에 표시
        SCREEN.blit(screen_image, (0, 0))

        # 타이머 텍스트를 오른쪽 상단에 표시
        SCREEN.blit(timer_text, (SCREEN_WIDTH - 200, 20))
        all_sprites.draw(SCREEN)
        pygame.display.update()

if __name__ == '__main__':
    main()