import pygame
import sys
import os
from button import ImageButton

all_sprites = pygame.sprite.Group()
bord = pygame.sprite.Group()
forester = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


pygame.init()
WIDTH, HEIGHT = 600, 550
MAX_FPS = 80
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Платформер')
main_background = load_image('background.jpg')
data_now = 'background.jpg'


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = pygame.Surface([20, 20])
        self.image.fill((0, 0, 255))
        self.rect = pygame.Rect(x, y, 20, 20)

    def update(self):
        global a
        if not pygame.sprite.spritecollideany(self, bord):
            self.rect = self.rect.move(0, 1)
        if pygame.sprite.spritecollideany(self, forester):
            self.rect = self.rect.move(0, -1)
            a = True
        elif not pygame.sprite.spritecollideany(self, forester):
            a = False

    def remo(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)

    def finding(self, m):
        self.rect = self.rect.move(m, 0)

    def finding1(self, m):
        self.rect = self.rect.move(0, m)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super().__init__(all_sprites)
        self.add(bord)
        self.image = pygame.Surface([50, 10])
        self.image.fill((129, 129, 129))
        self.rect = pygame.Rect(x1, y1, 50, 10)


class Forester(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super().__init__(all_sprites)
        self.add(forester)
        self.image = pygame.Surface([10, 50])
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(x1, y1, 10, 50)


def main_menu():
    start_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, "Новая игра", "green_button.png", 'green_button_hover.png')
    settings_button = ImageButton(WIDTH/2-(252/2), 250, 252, 74, "Настройки", "green_button.png", 'green_button_hover.png')
    exit_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "Выйти", "green_button.png", 'green_button_hover.png')
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, -200))
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
                if (WIDTH/2-(252/2) <= x and x <= WIDTH/2-(252/2) + 252) and (350 <= y and y <= 350 + 74):
                    running = False
                    pygame.quit()
                    sys.exit()
                if (WIDTH/2-(252/2) <= x and x <= WIDTH/2-(252/2) + 252) and (250 <= y and y <= 250 + 74):
                    fade()
                    setting_menu()
                if (WIDTH/2-(252/2) <= x and x <= WIDTH/2-(252/2) + 252) and (150 <= y and y <= 150 + 74):
                    fade()
                    new_game()
            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)
        for btn in [start_button, settings_button, exit_button]:
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
                        main_background = load_image('background1.jpg')
                        data_now = 'background1.jpg'
                    elif data_now == 'background1.jpg':
                        main_background = load_image('background2.jpg')
                        data_now = 'background2.jpg'
                    elif data_now == 'background2.jpg':
                        main_background = load_image('background3.jpg')
                        data_now = 'background3.jpg'
                    elif data_now == 'background3.jpg':
                        main_background = load_image('background.jpg')
                        data_now = 'background.jpg'
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
    global all_sprites, bord, forester
    all_sprites = pygame.sprite.Group()
    bord = pygame.sprite.Group()
    forester = pygame.sprite.Group()
    screen.fill((0, 0, 0))
    running = True
    clock = pygame.time.Clock()
    b = False
    f = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    f = True
            if event.type == pygame.K_ESCAPE:
                main_menu()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and f:
                if event.button == 1:
                    x, y = event.pos
                    Forester(x, y)
                    f = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    Border(x, y)
                elif event.button == 3:
                    x, y = event.pos
                    if not b:
                        a0 = Ball(x, y)
                        b = not b
                    else:
                        a0.remo(x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == 1073741906:
                    a0.finding1(-20)
                if a:
                    if event.key == 1073741906:
                        a0.finding1(-10)
                    if event.key == 1073741905:
                        a0.finding1(10)
                if event.key == 1073741903:
                    a0.finding(10)
                if event.key == 1073741904:
                    a0.finding(-10)
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)


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



if __name__ == '__main__':
    main_menu()