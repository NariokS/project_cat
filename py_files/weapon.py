import pygame
from settings import *
from random import choice
from support import import_folder

class Weapon(pygame.sprite.Sprite):
    '''Класс для создания объекта оружия.
    Объект создаётся в зависимости от направления игрока и от выбранного оружия'''

    def __init__(self, player, groups, z=LAYERS['main']):
        super().__init__(groups)

        # графика
        if player.status in ['up', 'down', 'left', 'right', 'idle']:
            self.status = f"{player.selected_weapon}_{player.status}"
        else:
            self.status = f"{player.selected_weapon}_idle"

        full_path = f"../graphics/weapons/{self.status}"
        self.animations = import_folder(full_path)
        self.frame_index = 0
        self.player = player

        self.image = self.animations[self.frame_index]
        self.find_out_direction()

        # местонахождение
        self.z = z


    def find_out_direction(self,):
        '''Изображение атаки появляется в зависимости от направления движения игрока.'''
        if self.player.status:
            self.direction = self.player.status if self.player.direction.magnitude() else 'idle'
            if self.player.selected_weapon == 'fungs':
                different_x = self.player.pos.x - SCREEN_WIDTH_HALF
                different_y = self.player.pos.y - SCREEN_HEIGHT_HALF
                self.pos = pygame.mouse.get_pos()
                self.rect = self.image.get_rect(center=self.pos)
            else:
                if self.direction == 'right':
                    self.rect = self.image.get_rect(midleft=self.player.rect.midright)
                elif self.direction == 'left':
                    self.rect = self.image.get_rect(midright=self.player.rect.midleft)
                elif self.direction == 'up':
                    self.rect = self.image.get_rect(midbottom=self.player.rect.midtop)
                elif self.direction == 'down':
                    self.rect = self.image.get_rect(midtop=self.player.rect.midbottom)
                else:
                    self.rect = self.image.get_rect(center=self.player.rect.center)
                self.pos = self.player.pos
            self.rect.centerx = self.pos[0] + different_x if self.player.selected_weapon == 'fungs' else self.pos.x
            self.rect.centery = self.pos[1] + different_y if self.player.selected_weapon == 'fungs' else self.pos.y

    def move(self, dt):
        if self.player.selected_weapon != 'fungs':
            self.pos = self.player.pos
            self.rect.centerx = round(self.pos.x)

            self.pos = self.player.pos
            self.rect.centery = round(self.pos.y)

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.animations):
            self.kill()
            return
        self.image = self.animations[int(self.frame_index)]

    def update(self, dt):
        self.move(dt)
        self.animate(dt)

