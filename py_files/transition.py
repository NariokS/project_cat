import pygame
from settings import *

class Transition:
    def __init__(self, player):

        # настройки
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # перекрывающая картинка
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -1

    def play(self):
        self.color += self.speed
        # по достижении полного затемнения, умножаем скорость на -1
        # для того, чтобы начать осветление, и перемещаем игрока
        # в центр объекта, с которым тот взаимодействует
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.displacement()
        if self.color > 255:
            self.speed *= -1
            self.color = 255
            self.player.interact = False
        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def displacement(self):
        '''Перемещение игрока в центр объекта, с которым тот взаимодействует,
        или возвращение на прежнее место.'''
        if self.player.interaction_status:
            self.player.rect.centerx = self.player.interact_sprite.rect.centerx
            self.player.rect.centery = self.player.interact_sprite.rect.centery
            self.player.pos.x = self.player.rect.centerx
            self.player.pos.y = self.player.rect.centery
            self.player.status = self.player.interaction_status
        else:
            self.player.rect.centerx = self.player.former_place_x
            self.player.rect.centery = self.player.former_place_y
            self.player.pos.x = self.player.rect.centerx
            self.player.pos.y = self.player.rect.centery
            self.player.status = 'cat_idle'
