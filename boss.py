import random
import pygame
import pyganim
import os
import sys

ATTACK = [f'Boss/Attack/attack{i}.png' for i in range(1, 10)]
ATTRACT_HAND = [f'Boss/attraction_hand/attra_hand{i}.png' for i in range(1, 8)]
DYING = [f'Boss/die/die{i}.png' for i in range(1, 13)]
HURT = [f'Boss/Hurt/hurt{i}.png' for i in range(1, 10)]
WAKE = [f'Boss/sleep/sleep{i}.png' for i in range(1, 9)]
RUN = [f'Boss/run_fly/run{i}.png' for i in range(1, 9)]
LASER_ATTACK = [f'Boss/laser_attack/laser_att{i}.png' for i in range(1, 7)]
LASER = [f'Boss/laser/laser{i}.png' for i in range(1, 11)]
SLEEP = ['Boss/sleep/sleep1.png']

COLOR = '#708090'
ANIMATION_DELAY = 0.15
BOSS_WIDTH = 72
BOSS_HEIGHT = 72
HAND_WIDTH = 47
HAND_HEIGHT = 18
VISION = 150


def load_image(fullname, colorkey=None):
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xv = 0
        self.DPS = 15
        self.HP = 200
        self.speed = 3
        self.time_from_attack = 0
        self.dead = False
        self.hand_throw = False
        self.hand_attr = False
        self.laser_att = False
        self.moving = False
        self.waking = False
        self.sleeping = True

        self.image = pygame.Surface((BOSS_WIDTH, BOSS_HEIGHT))
        self.image.fill(pygame.Color(COLOR))
        self.image.set_colorkey(pygame.Color(COLOR))
        self.rect = pygame.Rect((x, y, BOSS_WIDTH, BOSS_HEIGHT))
        self.vision = pygame.Rect((x - VISION, y - VISION, VISION * 2, VISION * 2))

        anim = [(frame, ANIMATION_DELAY) for frame in ATTACK]
        self.attack = pyganim.PygAnimation(anim)
        self.attack.play()

        anim = [(frame, ANIMATION_DELAY) for frame in ATTRACT_HAND]
        self.attract_hand = pyganim.PygAnimation(anim)
        self.attract_hand.play()

        anim = [(frame, ANIMATION_DELAY) for frame in DYING]
        self.dying = pyganim.PygAnimation(anim)
        self.dying.play()

        anim = [(frame, ANIMATION_DELAY) for frame in HURT]
        self.hurt = pyganim.PygAnimation(anim)
        self.hurt.play()

        anim = [(frame, ANIMATION_DELAY) for frame in WAKE]
        self.wake = pyganim.PygAnimation(anim)
        self.wake.play()
        self.wake.blit(self.image, (0, 0))

        anim = [(frame, ANIMATION_DELAY) for frame in RUN]
        self.run = pyganim.PygAnimation(anim)
        self.run.play()

        anim = [(frame, ANIMATION_DELAY) for frame in LASER_ATTACK]
        self.laser_attack = pyganim.PygAnimation(anim)
        self.laser_attack.play()

        anim = [(frame, ANIMATION_DELAY) for frame in SLEEP]
        self.sleep = pyganim.PygAnimation(anim)
        self.sleep.play()

    def update(self, screen, player, platforms, enm, ent, dd):
        if not self.dead:
            self.image.fill(pygame.Color(COLOR))
            if self.sleeping:
                self.sleep.blit(self.image, (0, 0))
                if self.vision.colliderect(player.rect):
                    self.waking = True
                    self.sleeping = False
                    self.time_from_attack = pygame.time.get_ticks()
            elif self.waking:
                self.wake.blit(self.image, (0, 0))
                if self.wake.currentFrameNum == 7:
                    self.waking = False
                    self.moving = True
            elif self.moving:
                if pygame.time.get_ticks() - self.time_from_attack >= 3000:
                    self.moving = False
                    self.hand_throw = True
                else:
                    if self.able_to_move(player, platforms):
                        if self.rect.x < player.rect.x:
                            self.xv = self.speed
                        else:
                            self.xv = -self.speed
                        self.rect.x += self.xv
                    else:
                        self.xv = 0
                    self.run.blit(self.image, (0, 0))
            elif self.hand_throw:
                self.attack.blit(self.image, (0, 0))
                if self.attack.currentFrameNum == 8:
                    self.hand_throw = False
                    self.hand_attr = True
                    hand = Hand(self.rect.right, self.rect.top + 10, player.rect.x, player.rect.y)
                    ent.add(hand)
                    dd.append(hand)
                    enm.add(hand)
            elif self.hand_attr:
                self.attract_hand.blit(self.image, (0, 0))
                if self.attract_hand.currentFrameNum == 6:
                    self.hand_attr = False
                    self.moving = True
                    self.time_from_attack = pygame.time.get_ticks()

    def able_to_move(self, player, platforms):
        if player.rect.x < self.rect.x:
            return not any([p.rect.collidepoint(self.rect.left, self.rect.top) for p in platforms])
        else:
            return not any([p.rect.collidepoint(self.rect.right, self.rect.top) for p in platforms])

    def hit_collide(self, rect):
        return self.rect.colliderect(rect)


class Hand(pygame.sprite.Sprite):
    def __init__(self, x, y, dest_x, dest_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((HAND_WIDTH, HAND_HEIGHT))
        self.image = load_image("boss/hand.png")

        self.rect = pygame.Rect(x, y, HAND_WIDTH, HAND_HEIGHT)

        self.dest_x = dest_x
        self.dest_y = dest_y
        self.DPS = 10
        self.moving = True
        self.speed = 7
        if x < dest_x:
            self.xv = self.speed
        else:
            self.xv = -self.speed
            self.image = pygame.transform.flip(self.image, True, False)
        self.yv = 0

    def update(self, *args):
        platforms = args[2]
        if self.moving:
            if self.dest_x - 7 < self.rect.x < self.dest_x + 7 and self.xv != 0:
                self.yv = self.speed
                angle = -90 if self.xv > 0 else 90
                self.xv = 0
                self.image = pygame.transform.rotate(self.image, angle)
            if self.rect.collidelist([p.rect for p in platforms]) != -1:
                self.moving = False
                self.DPS = 0
            print(self.xv, self.yv)
            self.rect.x += self.xv
            self.rect.y += self.yv

    def hit_collide(self, *args):
        return False
