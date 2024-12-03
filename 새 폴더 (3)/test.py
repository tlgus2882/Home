import pygame
import sys
import random
import tkinter as tk
from tkinter import simpledialog

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
FPS = 60

# 전역 변수
player_money = 100
knowledge = 0
screen_image_y = 585

# 이미지 및 음악 로드
screen_image = pygame.image.load("screenimage.png")
screen_image = pygame.transform.scale(screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
button_click_sound = pygame.mixer.Sound("button04a.mp3")
button_click_sound.set_volume(0.7)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 36)

class Animated(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
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

        # 화면 경계 확인
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# 퀴즈 게임 함수
def quiz_game():
    questions = {
        "많은 사람들이 일어나지 않은 거짓된 사실에 대한 기억을 공유하는 현상은 무엇인가요?": "만델라 효과",
        "국내 종합주가 지수로 대한민국의 주식 가격을 종합적으로 표시한 수치는 무엇인가요?": "코스피",
        "대한민국의 IMF 경제위기는 몇년도에 발생했을까요?": "1997",
        "오스트레일리아의 수도는 어디일까요?": "캔버라",
        "그리스 로마 신화에 나오는 지혜와 전술의 여신은 누구일까요?": "아테나",
    }

    quiz_list = list(questions.items())
    random.shuffle(quiz_list)
    score = 0
    root = tk.Tk()
    root.withdraw()

    for i, (question, answer) in enumerate(quiz_list[:5], 1):
        user_input = simpledialog.askstring(f"퀴즈 {i}/5", question.strip())
        if user_input == answer:
            score += 1

    root.destroy()
    return score

# 조준 게임 함수
def aim_game():
    school_image = pygame.image.load("school.png")
    school_image = pygame.transform.scale(school_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    mini_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    target_image = pygame.image.load("target.png")
    target_image = pygame.transform.scale(target_image, (60, 60))
    target_rect = target_image.get_rect()
    target_rect.topleft = (
        random.randint(0, SCREEN_WIDTH - target_rect.width),
        random.randint(0, SCREEN_HEIGHT - target_rect.height),
    )

    target_spawn_time = 2000
    last_spawn_time = pygame.time.get_ticks()
    score = 0
    game_time = 15
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        remaining_time = max(0, game_time - int(elapsed_time))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if target_rect.collidepoint(pygame.mouse.get_pos()):
                    button_click_sound.play()
                    score += 1
                    target_rect.topleft = (
                        random.randint(0, SCREEN_WIDTH - target_rect.width),
                        random.randint(0, SCREEN_HEIGHT - target_rect.height),
                    )

        if pygame.time.get_ticks() - last_spawn_time > target_spawn_time:
            target_rect.topleft = (
                random.randint(0, SCREEN_WIDTH - target_rect.width),
                random.randint(0, SCREEN_HEIGHT - target_rect.height),
            )
            last_spawn_time = pygame.time.get_ticks()

        mini_screen.blit(school_image, (0, 0))
        mini_screen.blit(target_image, target_rect.topleft)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 255, 0))
        timer_text = font.render(f"Time Left: {remaining_time}", True, (125, 125, 50))
        mini_screen.blit(score_text, (10, 10))
        mini_screen.blit(timer_text, (10, 50))

        pygame.display.update()

        if remaining_time <= 0:
            running = False

    return score

# 메인 함수
def main():
    global player_money
    global knowledge

    player = Animated(position=(100, screen_image_y))
    all_sprites = pygame.sprite.Group(player)

    reset_image = pygame.image.load("reset.png")
    reset_image = pygame.transform.scale(reset_image, (100, 100))
    reset_rect = reset_image.get_rect(topleft=(50, screen_image_y))

    quiz_image = pygame.image.load("quiz.png")
    quiz_image = pygame.transform.scale(quiz_image, (100, 100))
    quiz_rect = quiz_image.get_rect(topleft=(700, screen_image_y))

    shot_image = pygame.image.load("shot.png")
    shot_image = pygame.transform.scale(shot_image, (100, 100))
    shot_rect = shot_image.get_rect(topleft=(400, screen_image_y))

    timer_duration = 600
    start_ticks = pygame.time.get_ticks()

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
                elif event.key == pygame.K_LEFT:
                    player.direction = "left"
                elif player.rect.colliderect(quiz_rect) and event.key == pygame.K_y:
                    score = quiz_game()
                    player_money += score
                    knowledge += score
                elif player.rect.colliderect(reset_rect) and event.key == pygame.K_y:
                    start_ticks -= 60000
                elif player.rect.colliderect(shot_rect) and event.key == pygame.K_y and knowledge > 5:
                    score = aim_game()
                    player_money += score * 5
                    knowledge += score
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    player.direction = "front"
                    player.speed_x = 0

        all_sprites.update(mt)
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, timer_duration - int(elapsed_seconds))
        if remaining_time > 0:
            timer_text = font.render(f"Time Left: {remaining_time // 60}:{remaining_time % 60:02}", True, (70, 80, 90))
        else:
            end_text = font.render("Time Over", True, (255, 0, 0))
            SCREEN.blit(end_text, (SCREEN_WIDTH / 2 - end_text.get_width() // 2, SCREEN_HEIGHT / 2 - end_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        SCREEN.blit(screen_image, (0, 0))
        SCREEN.blit(quiz_image, quiz_rect.topleft)
        SCREEN.blit(reset_image, reset_rect.topleft)
        SCREEN.blit(shot_image, shot_rect.topleft)

        if player.rect.colliderect(quiz_rect):
            quiz_text = font.render("Press Y to start the quiz game.", True, (0, 255, 0))
            SCREEN.blit(quiz_text, (SCREEN_WIDTH // 2 - quiz_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        if player.rect.colliderect(reset_rect):
            reset_text = font.render("Press Y to rest and reduce 60 seconds.", True, (0, 255, 255))
            SCREEN.blit(reset_text, (SCREEN_WIDTH // 2 - reset_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        if player.rect.colliderect(shot_rect):
            shot_text = font.render("Press Y to start the mini-game (Knowledge > 5).", True, (255, 255, 0))
            SCREEN.blit(shot_text, (SCREEN_WIDTH // 2 - shot_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

        money_text = font.render(f"Money: ${player_money}", True, (255, 161, 92))
        SCREEN.blit(money_text, (10, 10))

        knowledge_text = font.render(f"Knowledge: {knowledge}", True, (137, 178, 233))
        SCREEN.blit(knowledge_text, (170, 10))

        all_sprites.draw(SCREEN)
        SCREEN.blit(timer_text, (SCREEN_WIDTH - 200, 20))
        pygame.display.update()

if __name__ == '__main__':
    main()        
