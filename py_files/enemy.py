import pygame
from settings import *
from entity import Entity
from support import import_folder


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups):
        
        # основные настройки
        super().__init__(groups)
        self.monster_name = monster_name
        self.status = f"{self.monster_name}_idle"

        # настройки отображения
        self.import_assets()
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['main']

    def import_assets(self):
        self.animations = {'mouse_idle': [],
                           'mouse_left': [], 'mouse_right': [], 'mouse_down': [], 'mouse_up': []}

        for animation in self.animations.keys():
            full_path = f'../graphics/enemy/{self.monster_name}/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
