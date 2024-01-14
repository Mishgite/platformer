import pyganim
import pygame


ENEMY_WIDTH = 87
ENEMY_HEIGHT = 45
VISION = 200
HIT_DISTANCE = 1
COLOR = '#708090'
MOVE_SPEED = 3
ANIMATION_DELAY = 0.1

IDLE_ANIM_L = [f'EnemyAnimL/idle/idle{i + 1}.png' for i in range(4)]
IDLE_ANIM_R = [f'EnemyAnimR/idle/idle{i + 1}.png' for i in range(4)]
WALK_ANIM_L = [f'EnemyAnimL/walk/walk{i + 1}.png' for i in range(8)]
WALK_ANIM_R = [f'EnemyAnimR/walk/walk{i + 1}.png' for i in range(8)]
TAKE_HIT_L = [f'EnemyAnimL/Take Hit/hit{i + 1}.png' for i in range(4)]
TAKE_HIT_R = [f'EnemyAnimR/Take Hit/hit{i + 1}.png' for i in range(4)]
DEATH_ANIM_L = [f'EnemyAnimL/Death/death{i + 1}.png' for i in range(4)]
DEATH_ANIM_R = [f'EnemyAnimR/Death/death{i + 1}.png' for i in range(4)]
ATTACK_ANIM_L = [f'EnemyAnimL/Attack/attack{i + 1}.png' for i in range(8)] + IDLE_ANIM_L
ATTACK_ANIM_R = [f'EnemyAnimR/Attack/attack{i + 1}.png' for i in range(8)] + IDLE_ANIM_R


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xv = 0
        self.rotation = -1

        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(pygame.Color(COLOR))
        self.image.set_colorkey(COLOR)
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.track_rect = pygame.Rect(x - VISION, y, VISION * 2, ENEMY_HEIGHT)
        self.hit_move_rect_l = pygame.Rect(self.rect.left, y, HIT_DISTANCE, ENEMY_HEIGHT)
        self.hit_move_rect_r = pygame.Rect(self.rect.right, y, HIT_DISTANCE, ENEMY_HEIGHT)
        self.idle = True
        self.walk = False
        self.attacking = False
        self.death = False
        self.dead = False
        self.DPS = 60

        anim = [(anim, ANIMATION_DELAY) for anim in IDLE_ANIM_R]
        self.idle_anim_r = pyganim.PygAnimation(anim)
        self.idle_anim_r.play()

        anim = [(anim, ANIMATION_DELAY) for anim in IDLE_ANIM_L]
        self.idle_anim_l = pyganim.PygAnimation(anim)
        self.idle_anim_l.play()
        self.idle_anim_l.blit(self.image, (0, 0))

        anim = [(anim, ANIMATION_DELAY) for anim in WALK_ANIM_R]
        self.walk_anim_r = pyganim.PygAnimation(anim)
        self.walk_anim_r.play()

        anim = [(anim, ANIMATION_DELAY) for anim in WALK_ANIM_L]
        self.walk_anim_l = pyganim.PygAnimation(anim)
        self.walk_anim_l.play()

        anim = [(anim, ANIMATION_DELAY) for anim in TAKE_HIT_R]
        self.take_hit_r = pyganim.PygAnimation(anim)
        self.take_hit_r.play()

        anim = [(anim, ANIMATION_DELAY) for anim in TAKE_HIT_L]
        self.take_hit_l = pyganim.PygAnimation(anim)
        self.take_hit_l.play()

        anim = [(anim, ANIMATION_DELAY) for anim in DEATH_ANIM_R]
        self.death_r = pyganim.PygAnimation(anim)
        self.death_r.play()

        anim = [(anim, ANIMATION_DELAY * 4) for anim in DEATH_ANIM_L]
        self.death_l = pyganim.PygAnimation(anim)
        self.death_l.play()

        anim = [(anim, ANIMATION_DELAY) for anim in ATTACK_ANIM_R]
        self.attack_r = pyganim.PygAnimation(anim)
        self.attack_r.play()

        anim = [(anim, ANIMATION_DELAY) for anim in ATTACK_ANIM_L]
        self.attack_l = pyganim.PygAnimation(anim)
        self.attack_l.play()

    def move(self, xv):
        self.track_rect.x += xv
        self.hit_move_rect_l.x += xv
        self.hit_move_rect_l.x += xv
        self.rect.x += xv

    def update(self, player, platforms):
        if not self.dead:
            self.image.fill(COLOR)
            if self.track_rect.colliderect(player.rect) and self.idle:
                self.idle = False
                self.walk = True
            elif self.walk:
                platforms = tuple(map(lambda x: x.rect, platforms))
                if self.track_rect.colliderect(player.rect):
                    if player.rect.x < self.rect.x:
                        if any(x.collidepoint(self.rect.left, self.rect.bottom) for x in platforms):
                            self.rotation = -1
                            self.walk_anim_l.blit(self.image, (ENEMY_WIDTH - 36, 0))
                            self.xv = -MOVE_SPEED
                        else:
                            self.idle_anim_l.blit(self.image, (ENEMY_WIDTH - 36, 0))
                            self.xv = 0
                    else:
                        if any(x.collidepoint(self.rect.right, self.rect.bottom) for x in platforms):
                            self.rotation = 1
                            self.walk_anim_r.blit(self.image, (0, 0))
                            self.xv = MOVE_SPEED
                        else:
                            self.idle_anim_r.blit(self.image, (ENEMY_WIDTH, 0))
                            self.xv = 0
                    if player.rect.colliderect(self.rect) and player.HP > 0:
                        self.attacking = True
                        self.walk = False

                    self.move(self.xv)
                else:
                    self.walk = False
            elif self.attacking:
                if self.rotation == 1:
                    self.attack_r.blit(self.image, (0, 0))
                    if self.attack_r.currentFrameNum == 11:
                        self.attacking = False
                        self.walk = True
                else:
                    if 6 <= self.attack_l.currentFrameNum <= 7:
                        self.attack_l.blit(self.image, (0, 0))
                    else:
                        self.attack_l.blit(self.image, (ENEMY_WIDTH - 36, 0))

                    if self.attack_l.currentFrameNum == 11:
                        self.attacking = False
                        self.walk = True
            else:
                self.idle = True
                if self.rotation == 1:
                    self.idle_anim_r.blit(self.image, (0, 0))
                else:
                    self.idle_anim_l.blit(self.image, (ENEMY_WIDTH - 36, 0))
