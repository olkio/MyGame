import pygame
import sys
import random
import time

pygame.init()
pygame.font.init()
pygame.mixer.init()

display_width = 600
display_height = 400
FPS = 60
size = 20

display = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
pygame.display.set_caption('Покорми котика ヾ(=`ω´=)ノ”')
clock = pygame.time.Clock()

cat_image = pygame.image.load('asserts/cat60.png').convert_alpha()
cat = cat_image
cat_rect = cat_image.get_rect(center=(250, 250))

sausages_image = pygame.image.load('asserts/sausages35.png').convert_alpha()
sausages_rect = sausages_image.get_rect()

bg_music = pygame.mixer.Sound('asserts/bg_sound.mp3')
interaction_sound = pygame.mixer.Sound('asserts/chavk.ogg')

start_time = time.time()
timer_duration = 10

font = pygame.font.Font(None, 36)  # Размер шрифта 36


class Cat:
    jump = 5

    def __init__(self, x, y, width, height, image) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def move(self, keys):
        global display_height, display_width

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and cat_rect.y > -20:
            cat_rect.y -= self.jump
        if keys[pygame.K_RIGHT] and cat_rect.right < display_width:
            cat_rect.x += self.jump
        if keys[pygame.K_DOWN] and cat_rect.bottom < display_height:
            cat_rect.y += self.jump
        if keys[pygame.K_LEFT] and cat_rect.x > 0:
            cat_rect.x -= self.jump

    def draw(self, display):
        display.blit(cat, cat_rect)


def make_new_sausages():
    sausages_x = random.randint(0, display_width - size)
    sausages_y = random.randint(0, display_height - size)
    sausages = pygame.Rect(sausages_x, sausages_y, size, size)
    return sausages


def feeding_the_cat():
    global cat_image, sausages_image
    cat = Cat(10, 300, 100, 60, cat_image)
    sausages = make_new_sausages()
    sausages_eaten = 0
    bg_music.play(-1)
    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        remaining_time = max(timer_duration - elapsed_time, 0)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        cat.move(pygame.key.get_pressed())
        display.fill((0, 128, 0))

        display.blit(sausages_image, (sausages.x, sausages.y))
        cat.draw(display)

        if cat_rect.colliderect(sausages):
            interaction_sound.play()
            pygame.time.delay(200)
            sausages = make_new_sausages()
            sausages_eaten += 1

        score_text = font.render("Score: " + str(sausages_eaten), True, (255, 255, 255))
        display.blit(score_text, (10, 10))

        timer_text = font.render("Time: {:.1f}".format(remaining_time), True, (255, 255, 255))
        display.blit(timer_text, (display_width - 100, 10))

        if remaining_time <= 0:
            bg_music.stop()
            
            if sausages_eaten >= 5:
                message = "Котик сыт!"
                break
            else:
                message = "Котик голодный!"

            font_big = pygame.font.Font(None, 48)
            message_text = font_big.render(message, True, (255, 255, 255))
            message_rect = message_text.get_rect(center=(display_width // 2, display_height // 2))

            display.blit(message_text, message_rect)
            pygame.display.update()
            pygame.time.delay(3000)  # Отобразить сообщение в течение 3 секунд

            sausages_eaten = 0
            start_time = time.time()
            bg_music.play(-1)



        clock.tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    while True:
        if not feeding_the_cat():
            pygame.quit()
            quit()
