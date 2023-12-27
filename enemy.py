from main import load_image, ANIMATION_DELAY
import pyganim
import pygame


ENEMY_WIDTH = 26
ENEMY_HEIGHT = 15
COLOR = '#708090'

IDLE_ANIM = [f'EnemyAnim/idle/idle{i + 1}.png' for i in range(7)]
TRACK_ANIM = [f'EnemyAnim/track/track{i + 1}.png' for i in range(4)]
WALK_ANIM = [f'EnemyAnim/walk/walk{i + 1}.png' for i in range(8)]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, r):
        pygame.sprite.Sprite.__init__(self)
        self.xv = 0
        self.yv = 0
        self.rotation = r
        self.start_x = x
        self.start_y = y

        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(pygame.Color(COLOR))
        self.image.set_colorkey(COLOR)
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

        anim = [(anim, ANIMATION_DELAY) for anim in IDLE_ANIM]
        self.idle_anim = pyganim.PygAnimation(anim)
        self.idle_anim.play()

        anim = [(anim, ANIMATION_DELAY) for anim in TRACK_ANIM]
        self.track_anim = pyganim.PygAnimation(anim)
        self.track_anim.play()

        anim = [(anim, ANIMATION_DELAY) for anim in WALK_ANIM]
        self.walk_anim = pyganim.PygAnimation(anim)
        self.walk_anim.play()
