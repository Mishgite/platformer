import pygame
import sys
import os
import sqlite3
from button import ImageButton


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


con = sqlite3.connect("play_db.sqlite")
cur = con.cursor()
result = cur.execute("""SELECT * FROM play""").fetchall()
image = result[0][1]
level = result[1][1]
data = ['background.jpg', 'background1.jpg', 'background2.jpg', 'background3.jpg']
pygame.init()
WIDTH, HEIGHT = 1000, 760
MAX_FPS = 80
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Платформер')
main_background = load_image(data[image])
data_now = data[image]


def main_menu():
    start_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, "Новая игра", "green_button.png", 'green_button_hover.png')
    continuation_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, "Продолжение",
                                      "green_button.png", 'green_button_hover.png')
    settings_button = ImageButton(WIDTH/2-(252/2), 350, 252, 74, "Настройки", "green_button.png", 'green_button_hover.png')
    exit_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "Выйти", "green_button.png", 'green_button_hover.png')
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render("MENU TEST", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH/2, 100))
        screen.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (WIDTH/2-(252/2) <= x and x <= WIDTH/2-(252/2) + 252) and (450 <= y and y <= 450 + 74):
                    fade()
                    running = False
                    pygame.quit()
                    sys.exit()
                if (WIDTH/2-(252/2) <= x and x <= WIDTH/2-(252/2) + 252) and (250 <= y and y <= 250 + 74):
                    fade()
                    continuation()
                if (WIDTH/2-(252/2) <= x and x <= WIDTH/2-(252/2) + 252) and (350 <= y and y <= 350 + 74):
                    fade()
                    setting_menu()
                if (WIDTH/2-(252/2) <= x and x <= WIDTH/2-(252/2) + 252) and (150 <= y and y <= 150 + 74):
                    fade()
                    new_game()
            for btn in [start_button, settings_button, exit_button, continuation_button]:
                btn.handle_event(event)
        for btn in [start_button, settings_button, exit_button, continuation_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        pygame.display.flip()


def setting_menu():
    global main_background, data_now
    video_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, "Видио", "green_button.png",
                                  'green_button_hover.png')
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "Выйти", "green_button.png",
                              'green_button_hover.png')
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, -200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (250 <= y and y <= 250 + 74):
                    if data_now == 'background.jpg':
                        cur.execute('''UPDATE play SET values = 1''').fetchall()
                        main_background = load_image(data[1])
                        data_now = data[1]
                    elif data_now == 'background1.jpg':
                        main_background = load_image(data[2])
                        data_now = data[2]
                    elif data_now == 'background2.jpg':
                        main_background = load_image(data[3])
                        data_now = data[3]
                    elif data_now == 'background3.jpg':
                        main_background = load_image(data[0])
                        data_now = data[0]
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (350 <= y and y <= 350 + 74):
                    fade()
                    main_menu()
            for btn in [video_button, back_button]:
                btn.handle_event(event)
        for btn in [video_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        pygame.display.flip()


def new_game():
    level1_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, "первый уровень", "green_button.png",
                                'green_button_hover.png')
    level2_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, "второй уровень",
                                "green_button.png", 'green_button_hover.png')
    level3_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "третий уровень", "green_button.png",
                                'green_button_hover.png')
    level4_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "четвёртыйй уровень", "green_button.png",
                                'green_button_hover.png')
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, "Выйти", "green_button.png",
                              'green_button_hover.png')
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, -200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (550 <= y and y <= 550 + 74):
                    fade()
                    main_menu()
            for btn in [level1_button, level2_button, level3_button, level4_button, back_button]:
                btn.handle_event(event)
        for btn in [level1_button, level2_button, level3_button, level4_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        pygame.display.flip()


def fade():
    running = True
    fade_alpha = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False
        pygame.display.flip()
        clock.tick(MAX_FPS)

def continuation():
    level1_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, "первый уровень", "green_button.png",
                               'green_button_hover.png')
    level2_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, "второй уровень",
                                      "green_button.png", 'green_button_hover.png')
    level3_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "третий уровень", "green_button.png",
                                  'green_button_hover.png')
    level4_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "четвёртыйй уровень", "green_button.png",
                              'green_button_hover.png')
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, "Выйти", "green_button.png",
                              'green_button_hover.png')
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, -200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (550 <= y and y <= 550 + 74):
                    fade()
                    main_menu()
            for btn in [level1_button, level2_button, level3_button, level4_button, back_button]:
                btn.handle_event(event)
        for btn in [level1_button, level2_button, level3_button, level4_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main_menu()