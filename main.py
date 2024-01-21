import sys
import pyganim
import os
import pygame
import sqlite3
from button import ImageButton
import time
import pygame.mixer
from enemy import Enemy
from boss import Boss


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
data = ['background.jpg', 'background1.jpg', 'background2.jpg', 'background3.png']
level_data = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt']
pygame.init()
WIDTH, HEIGHT = 1280, 720
MAX_FPS = 80
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Платформер')
icon = pygame.image.load('mainicon.png')
pygame.display.set_icon(icon)
main_background = load_image(data[image])
data_now = data[image]

MOVE_SPEED = 5
WIDTH1 = 42
HEIGHT1 = 52
WIDTH2 = 42
HEIGHT2 = 52
COLOR = "#888888"
JUMP_POWER = 12
GRAVITY = 0.4
ANIMATION_DELAY = 0.1

ANIMATION_RIGHT = ['Run/run1.png', 'Run/run2.png', 'Run/run3.png', 'Run/run4.png', 'Run/run5.png', 'Run/run6.png',
                   'Run/run7.png', 'Run/run8.png']
ANIMATION_LEFT = ['Run1/run1.png', 'Run1/run2.png', 'Run1/run3.png', 'Run1/run4.png', 'Run1/run5.png', 'Run1/run6.png',
                  'Run1/run7.png', 'Run1/run8.png']
ANIMATION_JUMP_LEFT = [('Poses/Jumpl.png', 0.1)]
ANIMATION_JUMP_RIGHT = [('Poses/Jumpr.png', 0.1)]
ANIMATION_JUMP = [('Poses/r1.png', 0.1)]
ANIMATION_STAY = [('Poses/r1.png', 0.1)]
KEY_PICKUP_ANIM = ['KeyPickup/lifting1.png', 'KeyPickup/lifting2.png', 'KeyPickup/lifting3.png',
                   'KeyPickup/lifting4.png', 'KeyPickup/lifting5.png']
ATTACK_LEFT = [f'AttacksL/attacks{i}.png' for i in range(1, 19)]
ATTACK_RIGHT = [f'AttacksR/attacks{i}.png' for i in range(1, 19)]
ATTACK_LEFT_WAVE = [f'AttacksL_wave/attacks{i}_wave.png' for i in range(1, 19)]
ATTACK_RIGHT_WAVE = [f'AttacksR_wave/attacks{i}_wave.png' for i in range(1, 19)]
ATTACK_PAUSES = [0, 5, 8, 11, 17]
ANIMATION_DEAD = ['die/death1.png', 'die/death2.png', 'die/death3.png', 'die/death4.png', 'die/death4.png']

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)
PLATFORMS_TEXTURES = {chr(92): 'platform_floor_cornerRW.png', '/': 'platform_floor_cornerRN.png',
                      '!': 'platform_floor_cornerLN.png', '?': 'platform_floor_cornerLW.png',
                      '_': 'platform_floor.png', '=': 'platform_ceiling.png', '-': 'platform.png',
                      '[': 'platform_vertically.png', ']': 'platform_horizontally.png',
                      '{': 'platform_floor3N.png', '}': 'platform_floor3H.png',
                      ')': 'platform_floor3R.png', '(': 'platform_floor3L.png',
                      'i': 'platform_wall_L.png', 'I': 'platform_wall_R.png',
                      '#': 'land.jpg', '@': 'land_grass.jpg',
                      '&': 'land_island.png', '$': 'land_islandR.png',
                      ':': 'land_islandL.png', ';': 'land_islandN.png',
                      "'": 'land_islandH.png', '"': 'land_islandHh.png',
                      ',': 'land_islandRr.png', '`': 'land_islandLl.png',
                      '~': 'land_islandM.png', 'R': 'lava_landR.png',
                      'r': 'lava_landRh.png', 'L': 'lava_landL.png',
                      'l': 'lava_landLh.png', 'W': 'lava_land.png',
                      'H': 'lava_landn.png', 'x': 'level4_block.png'
                      }


LAVA_WIDTH = 32
LAVA_HEIGHT = 32
LAVA_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)
wasd = True

WIN_WIDTH = 1280
WIN_HEIGHT = 720
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

BACKGROUND_IMAGE_DICT = dict()
conn = sqlite3.connect('play_db.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT name FROM level_background")
result = cursor.fetchall()
k = 1
for i in result:
    BACKGROUND_IMAGE_DICT[str(k)] = i[0]
    k += 1
conn.close()


DOOR_WIDTH = 59
DOOR_HEIGHT = 63

KEY_WIDTH = 34
KEY_HEIGHT = 49
LEVEL_MUSIC_DICT = dict()
conn = sqlite3.connect('play_db.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT music_name FROM music WHERE level_id > 0")
result = cursor.fetchall()
k = 1
for i in result:
    print(i)
    LEVEL_MUSIC_DICT[str(k)] = i[0]
    k += 1
conn.close()


def main_menu():
    pygame.mixer.init()
    music = pygame.mixer.Sound('music\mainmenu.mp3')
    music.set_volume(0.1)
    music.play()
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
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (450 <= y and y <= 450 + 74):
                    fade()
                    running = False
                    pygame.quit()
                    sys.exit()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (250 <= y and y <= 250 + 74):
                    fade()
                    continuation()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (350 <= y and y <= 350 + 74):
                    fade()
                    setting_menu()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (150 <= y and y <= 150 + 74):
                    fade()
                    new_game()
            for btn in [start_button, settings_button, exit_button, continuation_button]:
                btn.handle_event(event)
        for btn in [start_button, settings_button, exit_button, continuation_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        pygame.display.flip()


def setting_menu():
    global main_background, data_now, wasd
    video_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, "Видео", "green_button.png",
                               'green_button_hover.png')
    management_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, "Смена управления", "green_button.png",
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
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (150 <= y and y <= 250 + 74):
                    wasd = not wasd
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
                    pygame.mixer.stop()
                    fade()
                    main_menu()
            for btn in [management_button, video_button, back_button]:
                btn.handle_event(event)
        for btn in [management_button, video_button, back_button]:
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
                    pygame.mixer.stop()
                    fade()
                    level_now = 0
                    level()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (250 <= y and y <= 250 + 74):
                    fade()
                    pygame.mixer.stop()
                    level_now = 1
                    level()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (350 <= y and y <= 350 + 74):
                    fade()
                    pygame.mixer.stop()
                    level_now = 2
                    level()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (450 <= y and y <= 450 + 74):
                    fade()
                    pygame.mixer.stop()
                    level_now = 3
                    level()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (550 <= y and y <= 550 + 74):
                    fade()
                    pygame.mixer.stop()
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
    level1_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, "Продолжение", "green_button.png",
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
                    pygame.mixer.stop()
                    fade()
                    level()
                if (WIDTH / 2 - (252 / 2) <= x and x <= WIDTH / 2 - (252 / 2) + 252) and (350 <= y and y <= 350 + 74):
                    pygame.mixer.stop()
                    fade()
                    main_menu()
            for btn in [level1_button, back_button]:
                btn.handle_event(event)
        for btn in [level1_button, back_button]:
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
        self.HP = 150
        self.DPS = 10
        self.rotation = 1
        self.alive = True
        self.onGround = False
        self.image = pygame.Surface((WIDTH1, HEIGHT1))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, WIDTH1, HEIGHT1)
        self.image.set_colorkey(pygame.Color(COLOR))
        self.pickuping_key = False
        self.attacking = False
        self.attack_time = 0
        self.time_from_dmg = 0

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

        boltAnim = list()
        for anim in KEY_PICKUP_ANIM:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.keyPickupAnim = pyganim.PygAnimation(boltAnim)
        self.keyPickupAnim.play()

        boltAnim = [(anim, ANIMATION_DELAY) for anim in ATTACK_LEFT]
        self.attackLeftAnim = pyganim.PygAnimation(boltAnim)
        self.attackLeftAnim.play()

        boltAnim = [(anim, ANIMATION_DELAY) for anim in ATTACK_RIGHT]
        self.attackRightAnim = pyganim.PygAnimation(boltAnim)
        self.attackRightAnim.play()

        boltAnim = list()
        for anim in ANIMATION_DEAD:
            boltAnim.append((anim, ANIMATION_DELAY * 4))
        self.dyingAnim = pyganim.PygAnimation(boltAnim)
        self.dyingAnim.play()
        self.dyingAnim.nextFrame()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms, dmg_deal, enemies: pygame.sprite.Group, attack_wave):
        if self.HP <= 0:
            self.rect.width = WIDTH1 + 30
            self.image.fill(pygame.Color(COLOR))
            self.dyingAnim.blit(self.image, (0, 0))
            if self.dyingAnim.currentFrameNum == 4:
                time.sleep(1)
                self.alive = False
        elif self.pickuping_key:
            self.image.fill(pygame.Color(COLOR))
            self.keyPickupAnim.blit(self.image, (0, 0))
            if self.keyPickupAnim.currentFrameNum == 3:
                self.pickuping_key = False
        elif self.attacking:
            self.image.fill(pygame.Color(COLOR))
            if self.rotation:
                self.attackRightAnim.blit(self.image, (0, 0))
                if self.attackRightAnim.currentFrameNum in ATTACK_PAUSES:
                    if pygame.mouse.get_pressed(3)[0]:
                        for sprite in enemies:
                            if sprite.hit_collide(attack_wave.rect):
                                sprite.HP -= self.DPS
                    else:
                        self.attackRightAnim.currentFrameNum = 0
                        self.attacking = False
            else:
                self.attackLeftAnim.blit(self.image, (0, 0))
                if self.attackLeftAnim.currentFrameNum in ATTACK_PAUSES:
                    if pygame.mouse.get_pressed(3)[0]:
                        for sprite in enemies:
                            if sprite.hit_collide(self.rect):
                                sprite.death = True
                    else:
                        self.attackLeftAnim.currentFrameNum = 0
                        self.attacking = False
        else:
            if up:
                if self.onGround:
                    self.yvel = -JUMP_POWER
                self.image.fill(pygame.Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))
            if left:
                self.xvel = -MOVE_SPEED
                self.rotation = 0
                self.image.fill(pygame.Color(COLOR))
                if up:
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
                else:
                    self.boltAnimLeft.blit(self.image, (0, 0))
            if right:
                self.xvel = MOVE_SPEED
                self.image.fill(pygame.Color(COLOR))
                self.rotation = 1
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
            self.collide(0, self.yvel, platforms, dmg_deal)
            self.rect.x += self.xvel
            self.collide(self.xvel, 0, platforms, dmg_deal)

    def collide(self, xvel, yvel, platforms, dmg_deal):
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
        for d in dmg_deal:
            if (pygame.time.get_ticks() - self.time_from_dmg) / 1000 >= 1:
                if isinstance(d, Enemy):
                    if self.rect.colliderect(d.rect):
                        if d.attack_l.currentFrameNum == 10 or d.attack_r.currentFrameNum == 10:
                            self.HP -= d.DPS
                            self.time_from_dmg = pygame.time.get_ticks()
                elif pygame.sprite.collide_rect(self, d):
                    self.HP -= d.DPS
                    self.time_from_dmg = pygame.time.get_ticks()
            if self.HP < 0:
                self.HP = 0

    def show_hp(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f'{self.HP} / 150', True, pygame.color.Color('red'))
        screen.blit(text, (5, 5))

# КОНЕЦ ПЕРСОНАЖА


class AttackWave(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.rotation = player.rotation
        self.image = pygame.Surface((60, 52))
        self.image.fill(pygame.Color(COLOR))
        self.image.set_colorkey(pygame.Color(COLOR))

        anim = [(anim, ANIMATION_DELAY) for anim in ATTACK_RIGHT_WAVE]
        self.attackR_anim = pyganim.PygAnimation(anim)
        self.attackR_anim.play()

        anim = [(anim, ANIMATION_DELAY) for anim in ATTACK_LEFT_WAVE]
        self.attackL_anim = pyganim.PygAnimation(anim)
        self.attackL_anim.play()

        if self.rotation:
            self.rect = pygame.Rect(player.rect.right - 10, player.rect.top, 67, 52)
            self.attackR_anim.blit(self.image, (0, 0))
        else:
            self.rect = pygame.Rect(player.rect.left - 50, player.rect.top, 67, 52)
            self.attackL_anim.blit(self.image, (0, 0))

    def update(self):
        self.rotation = self.player.rotation
        self.image.fill(pygame.Color(COLOR))
        if self.player.attacking:
            if self.rotation:
                self.rect.x = self.player.rect.right - 10
                if self.player.attackRightAnim.currentFrameNum == 0:
                    self.attackR_anim.currentFrameNum = 0
                self.attackR_anim.blit(self.image, (0, 0))
            else:
                self.rect.x = self.player.rect.left - 50
                if self.player.attackLeftAnim.currentFrameNum == 0:
                    self.attackL_anim.currentFrameNum = 0
                self.attackL_anim.blit(self.image, (0, 0))
        else:
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y


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
        self.DPS = 30


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
        if not self.pickuped:
            self.pickuped = True
            self.image = pygame.Surface((0, 0))
            self.door.key_pickuped = True
            # show_message('Ключ подобран', 10, 10)


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


black = (0, 0, 0)
white = (255, 255, 255)


def show_message(message, x, y, duration=1000):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, white)
    screen.blit(text, (x, y))
    pygame.display.flip()

    # Ждем несколько секунд, затем очищаем сообщение
    time.sleep(duration / 1000)
    screen.fill(black)
    pygame.display.flip()


def what_level():
    level_number = (level_data[level_now])[5]
    background_for_current_level = load_image(BACKGROUND_IMAGE_DICT.get(level_number))
    return background_for_current_level


def what_level_music():
    return (level_data[level_now])[5]


def level():
    global level_now
    bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    # будем использовать как фон
    bg.blit(what_level(), (0, 0))  # Заливаем поверхность сплошным цветом

    hero = Player(50, 700)  # создаем героя по (x,y) координатам
    wave = AttackWave(hero)
    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    enemies = pygame.sprite.Group()
    platforms = []  # то, во что мы будем врезаться или опираться
    damage_dealing = list()

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
                damage_dealing.append(lv)
            if col == '|':
                door = Door(x, y)
            if col == '*':
                key_coords = x, y
            if col == 'E':
                enemy = Enemy(x, y)
                damage_dealing.append(enemy)
                entities.add(enemy)
                enemies.add(enemy)
            if col == 'B':
                boss = Boss(x, y)
                damage_dealing.append(boss)
                entities.add(boss)
                enemies.add(boss)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    key = Key(*key_coords, door)
    entities.add(key)
    entities.add(door)
    entities.add(hero)
    entities.add(wave)

    total_level_width = len(lvl[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(lvl) * PLATFORM_HEIGHT  # высоту

    pygame.mixer.init()
    music_level = pygame.mixer.Sound(LEVEL_MUSIC_DICT.get(what_level_music()))
    music_level.set_volume(0.1)
    music_level.play()

    camera = Camera(camera_configure, total_level_width, total_level_height)
    raning = True
    while raning:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.mixer.stop()
                fade()
                raning = False
            if not wasd:
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
            else:
                if e.type == pygame.KEYDOWN and (e.key == pygame.K_w or e.key == pygame.K_SPACE):
                    up = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
                    left = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
                    right = True
                if e.type == pygame.KEYUP and (e.key == pygame.K_w or e.key == pygame.K_SPACE):
                    up = False
                if e.type == pygame.KEYUP and e.key == pygame.K_d:
                    right = False
                if e.type == pygame.KEYUP and e.key == pygame.K_a:
                    left = False
            if pygame.sprite.collide_rect(hero, door) and e.type == pygame.KEYDOWN and e.key == pygame.K_e:
                if door.collide():
                    pygame.mixer.stop()
                    fade()
                    raning = False
                    level_now += 1
                    level()
            if pygame.sprite.collide_rect(hero, key) and not key.pickuped:
                key.pickup()
                hero.pickuping_key = True
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 or \
                    e.type == pygame.KEYDOWN and e.key == pygame.K_LCTRL:
                hero.attacking = True

        pygame.display.flip()
        screen.blit(bg, (0, 0))
        camera.update(hero)  # камера движется за игроком
        hero.update(left, right, up, platforms, damage_dealing, enemies, wave)  # передвижение
        wave.update()
        enemies.update(screen, hero, platforms, enemies, entities, damage_dealing)

        # screen.blit(door.image, camera.apply(door))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        hero.show_hp(screen)
        if not hero.alive:
            pygame.mixer.stop()
            raning = False
            fade()
            level()
        pygame.display.update()


if __name__ == '__main__':
    main_menu()
