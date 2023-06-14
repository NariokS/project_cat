import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

class AnimateTile(Generic):
    def __init__(self, pos, frames, groups, z=LAYERS['main']):

        # для анимации
        self.frames = frames
        self.frame_index = 0

        # для спрайтов
        super().__init__(pos=pos,
                         surf=self.frames[self.frame_index],
                         groups=groups,
                         z=z)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class Decoration(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

class Tree(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)

class Collision(Generic):
    '''Объекты столкновений.'''
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)

class Interaction(Generic):
    '''Объекты взаимодействий.'''
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name
