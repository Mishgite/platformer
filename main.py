import sys
import pyganim
import os
import pygame
import sqlite3
from button import ImageButton
import time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "Levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, ' '), level_map))


con = sqlite3.connect("play_db.sqlite")
cur = con.cursor()
result = cur.execute("""SELECT * FROM play""").fetchall()
image = result[0][1]
level_now = result[1][1]
data = ['background.jpg', 'background1.jpg', 'background2.jpg', 'background3.jpg']
level_data = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt']
pygame.init()
WIDTH, HEIGHT = 1000, 760
MAX_FPS = 80
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Платформер')
main_background = load_image(data[image])
data_now = data[image]

MOVE_SPEED = 7
WIDTH1 = 49
HEIGHT1 = 52
COLOR = "#888888"
JUMP_POWER = 12
GRAVITY = 0.5
ANIMATION_DELAY = 0.1

ANIMATION_RIGHT = ['Run/run1.png', 'Run/run2.png', 'Run/run3.png', 'Run/run4.png', 'Run/run5.png', 'Run/run6.png',
                   'Run/run7.png', 'Run/run8.png']
ANIMATION_LEFT = ['Run1/run1.png', 'Run1/run2.png', 'Run1/run3.png', 'Run1/run4.png', 'Run1/run5.png', 'Run1/run6.png',
                  'Run1/run7.png', 'Run1/run8.png']
ANIMATION_JUMP_LEFT = [('Poses/Jumpl.png', 0.1)]
ANIMATION_JUMP_RIGHT = [('Poses/Jumpr.png', 0.1)]
ANIMATION_JUMP = [('Poses/r1.png', 0.1)]
ANIMATION_STAY = [('Poses/r1.png', 0.1)]

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)
PLATFORMS_TEXTURES = {chr(92): 'platform_floor_cornerRW.png', '/': 'platform_floor_cornerRN.png',
                      '!': 'platform_floor_cornerLN.png', '?': 'platform_floor_cornerLW.png',
                      '_': 'platform_floor.png', '=': 'platform_ceiling.png', '-': 'platform.png'
                      }


LAVA_WIDTH = 32
LAVA_HEIGHT = 32
LAVA_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)

WIN_WIDTH = 1000
WIN_HEIGHT = 760
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_IMAGE = load_image('backgroundl.png')

DOOR_WIDTH = 59
DOOR_HEIGHT = 63

KEY_WIDTH = 34
KEY_HEIGHT = 49


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
        text_surface = font.render("MENU", True, (255, 255, 255))
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
    video_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, "Видео", "green_button.png",
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
                        # cur.execute("""UPDATE play SET values = 1 WHERE id = 1""")
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
    global level_now
    level1_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, "первый уровень", "green_button.png",
                                'green_button_hover.png')
    level2_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, "второй уровень",
                                "green_button.png", 'green_button_hover.png')
    level3_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "третий уровень", "green_button.png",
                                'green_button_hover.png')
    level4_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "четвёртый уровень", "green_button.png",
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
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (150 <= y and y <= 150 + 74):
                    fade()
                    level_now = 0
                    level()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (250 <= y and y <= 250 + 74):
                    fade()
                    level_now = 1
                    level()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (350 <= y and y <= 350 + 74):
                    fade()
                    level_now = 2
                    level()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (450 <= y and y <= 450 + 74):
                    fade()
                    level_now = 3
                    level()
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
    level4_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "четвёртый уровень", "green_button.png",
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
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (150 <= y and y <= 150 + 74):
                    fade()
                    level()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (550 <= y and y <= 550 + 74):
                    fade()
                    main_menu()
            for btn in [level1_button, level2_button, level3_button, level4_button, back_button]:
                btn.handle_event(event)
        for btn in [level1_button, level2_button, level3_button, level4_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.onGround = False
        self.image = pygame.Surface((WIDTH1, HEIGHT1))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, WIDTH1, HEIGHT1)
        self.image.set_colorkey(pygame.Color(COLOR))

        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По умолчанию стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms):
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
            self.image.fill(pygame.Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))
        if left:
            self.xvel = -MOVE_SPEED
            self.image.fill(pygame.Color(COLOR))
            if up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))
        if right:
            self.xvel = MOVE_SPEED
            self.image.fill(pygame.Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))
        if not (left or right):
            self.xvel = 0
            if not up:
                self.image.fill(pygame.Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
# КОНЕЦ ПЕРСОНАЖА


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.image = load_image(img)
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
# КОНЕЦ ПЛАТФОРМЫ


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.image = load_image("lava.png")
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((DOOR_WIDTH, DOOR_HEIGHT))
        self.image = load_image("door.png")
        self.rect = pygame.Rect(x, y, DOOR_WIDTH, DOOR_HEIGHT)
        self.opened = False
        self.key_pickuped = False

    def collide(self):
        if not self.opened:
            if self.key_pickuped:
                self.image = load_image("door_open.png")
                self.opened = not self.opened
                return False
        else:
            return True


class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, door: Door):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((KEY_WIDTH, KEY_HEIGHT))
        self.image = load_image("certificate_key.jpg")
        self.rect = pygame.Rect(x, y, KEY_WIDTH, KEY_HEIGHT)
        self.pickuped = False
        self.door = door

    def pickup(self):
        self.pickuped = True
        self.image = None
        self.door.key_pickuped = True


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


def level():
    global level_now

    bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    # будем использовать как фон
    bg.blit(BACKGROUND_IMAGE, (0, 0))  # Заливаем поверхность сплошным цветом

    hero = Player(50, 700)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    entities.add(hero)

    lvl = load_level(level_data[level_now])

    timer = pygame.time.Clock()
    x = y = 0
    for row in lvl:
        for col in row:
            if col in PLATFORMS_TEXTURES.keys():
                pf = Platform(x, y, PLATFORMS_TEXTURES[col])
                entities.add(pf)
                platforms.append(pf)
            if col == "%":
                lv = Lava(x, y)
                entities.add(lv)
                platforms.append(lv)
            if col == '|':
                door = Door(x, y)
            if col == '*':
                key_coords = x, y

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    key = Key(*key_coords, door)

    total_level_width = len(lvl[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(lvl) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)
    raning = True
    while raning:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                fade()
                raning = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                up = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                right = True
            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                left = False
            if pygame.sprite.collide_rect(hero, door) and e.type == pygame.KEYDOWN and e.key == pygame.K_e:
                if door.collide():
                    fade()
                    raning = False
                    level_now += 1
                    level()
            if pygame.sprite.collide_rect(hero, key):
                key.pickup()
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos
                if 10 <= x and x <= 10 + 66 and (150 <= y and y <= 50 + 66):
                    raning = False
                    fade()
                    main_menu()

        pygame.display.flip()
        screen.blit(bg, (0, 0))
        camera.update(hero)  # камера движется за игроком
        hero.update(left, right, up, platforms)  # передвижение
        screen.blit(door.image, camera.apply(door))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()


if __name__ == '__main__':
    main_menu()
