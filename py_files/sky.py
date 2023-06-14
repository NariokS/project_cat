import pygame
from settings import *
from support import import_folder
from sprites import Generic
from random import randint, choice

class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.current_color = [255, 255, 255]
        self.end_color = (50, 100, 180)

    def display(self, dt, night=False):
        if night:
            for index, value in enumerate(self.end_color):
                if self.current_color[index] > value:
                    self.current_color[index] -= 100 * dt
        else:
            for index, value in enumerate(self.start_color):
                if self.current_color[index] < value:
                    self.current_color[index] += 100 * dt

        self.full_surf.fill(self.current_color)
        self.display_surface.blit(self.full_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

class Drop(Generic):
    def __init__(self, surf, pos, moving, groups, z):

        # основные настройки
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # движение
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)

            # капля будет двигаться на 2 влево и 4 вниз,
            # что в сумме даст движение по диагонали
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        '''Только для капель устанавливается видимость движения путём изменения
        её позиции по диагонали.
        Через определенное время и капля, и её место её отскока удаляются.
        '''
        # движение
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = round(self.pos.x), round(self.pos.y)

        # таймер
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class Rain:
    def __init__(self, all_sprites, player):

        self.player = player
        self.half_screen_width = SCREEN_WIDTH / 2
        self.half_screen_height = SCREEN_HEIGHT / 2
        self.all_sprites = all_sprites

        self.rain_drops = import_folder('graphics/rain/drops/')
        self.rain_floor = import_folder('graphics/rain/floor/')

    def update_player_pos(self):
        '''Получение ширины и высоты экрана, на котором надо изображать дождь,
        Т.е. дождь появляется только в зоне, которую игрок непосредственно видит,
        а не на всей карте.
        '''
        self.floor_w_l, self.floor_w_r = int(self.player.pos[0] - self.half_screen_width), \
                                         int(self.player.pos[0] + self.half_screen_width)
        self.floor_h_l, self.floor_h_r = int(self.player.pos[1] - self.half_screen_height - 64), \
                                         int(self.player.pos[1] + self.half_screen_height)

    def create_floor(self):
        '''Создание в видимой зоне отскока капли.'''
        Drop(surf=choice(self.rain_floor),
             pos=(randint(self.floor_w_l, self.floor_w_r), randint(self.floor_h_l, self.floor_h_r)),
             moving=False,
             groups=self.all_sprites,
             z=LAYERS['rain floor'])

    def create_drops(self):
        '''Создание в видимой зоне капли.'''
        Drop(surf=choice(self.rain_drops),
             pos=(randint(self.floor_w_l, self.floor_w_r), randint(self.floor_h_l, self.floor_h_r)),
             moving=True,
             groups=self.all_sprites,
             z=LAYERS['rain drops'])

    def update(self):
        '''Обновления позиции игрока.
        Создание места отскока капли.
        Создание капли.
        '''
        self.update_player_pos()
        self.create_floor()
        self.create_drops()