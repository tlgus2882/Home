import pygame
import sys
import random
import tkinter as tk
from tkinter import simpledialog

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
pygame.init()
clock = pygame.time.Clock()
FPS = 60
screen_image_y = 585
player_money = 100
# 맵 이미지 로드 및 스케일
screen_image = pygame.image.load("screenimage.png")
screen_image = pygame.transform.scale(screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 36)

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

def quiz_game():
    questions = {
        "많은 사람들이 일어나지 않은 거짓된 사실에 대한 기억을 공유하는 현상은 무엇인가요?": "만델라 효과",
        "국내 종합주가 지수로 대한민국의 주식 가격을 종합적으로 표시한 수치는 무엇인가요?": "코스피",
        "대한민국의 IMF 경제위기는 몇년도에 발생했을까요?": "1997",
        "오스트레일리아의 수도는 어디일까요?": "캔버라",
        "그리스 로마 신화에 나오는 지혜와 전술의 여신은 누구일까요?": "아테나",
        "자유의 여신상을 선물로 준 나라는 어디일까요?": "프랑스",
        "음악의 아버지는 바흐라면 의학의 아버지는 누구일까요?": "히포크라테스",
        "모든 혈액형에게 피를 수혈해줄 수 있는 혈액형은 무엇인가요?": "o형",
        "스승을 뛰어넘는 제자를 비유하는 사자성어는 무엇인가?": "청출어람",
        "한 시즌 동안 최고의 활약을 펼친 선수에게 수여하는 상으로, 축구 선수로서 받을 수 있는 가장 명예로운 상으로 여겨지는 이상은?": "발롱도르",
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

def main():
    global player_money
    # 플레이어 설정
    player = Animated(position=(100, screen_image_y))
    all_sprites = pygame.sprite.Group(player)

    # 오브젝트 이미지 및 위치 설정
    home_image = pygame.image.load("home.png")
    home_image = pygame.transform.scale(home_image, (100, 100))
    home_rect = home_image.get_rect(topleft=(500, screen_image_y))

    quiz_image = pygame.image.load("quiz.png")
    quiz_image = pygame.transform.scale(quiz_image, (100, 100))
    quiz_rect = quiz_image.get_rect(topleft=(700, screen_image_y))

    timer_duration = 120  # 타이머 2분
    start_ticks = pygame.time.get_ticks()
    end_text = font.render("Time Over", True, (70, 80, 90))
    collision_occurred = False
    choice_made = False

    running = True
    while running:
        mt = clock.tick(FPS) / 1000

        # 이벤트 처리
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
                    if player.rect.colliderect(quiz_rect):
                        score = quiz_game()
                        player_money += score * 10
                        choice_made = True
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
            SCREEN.blit(end_text, (SCREEN_WIDTH / 2 - end_text.get_width() // 2, SCREEN_HEIGHT / 2 - end_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        # 맵 표시
        SCREEN.blit(screen_image, (0, 0))
        SCREEN.blit(quiz_image, quiz_rect.topleft)

        # 충돌 감지 (home, quiz와 플레이어)
        if player.rect.colliderect(quiz_rect):
            collision_occurred = True
            if not choice_made:
                choice_text = font.render("Press Y to start the quiz.", True, (60, 70, 80))
                SCREEN.blit(choice_text, (SCREEN_WIDTH / 2 - choice_text.get_width() // 2, SCREEN_HEIGHT / 2))
        else:
            collision_occurred = False
            choice_made = False  # 선택을 초기화하여 반복적으로 충돌 처리 가능

        # 돈 출력
        money_text = font.render(f"Money: ${player_money}", True, (255, 255, 0))
        SCREEN.blit(money_text, (10, 10))

        # 타이머와 스프라이트 업데이트
        SCREEN.blit(timer_text, (SCREEN_WIDTH - 200, 20))
        all_sprites.draw(SCREEN)
        pygame.display.update()

if __name__ == '__main__':
    main()
