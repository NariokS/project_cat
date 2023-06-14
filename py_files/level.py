import pygame
from time import time
from settings import *
from player import Player
from sprites import Generic, AnimateTile, Decoration, Tree, Collision, Interaction
from pytmx.util_pygame import load_pygame
from support import *
from sky import Rain, Sky
from overlay import Overlay
from transition import Transition
from pathfinder import Pathfinder
from enemy import Enemy
from weapon import Weapon

def duration_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        func(*args, **kwargs)
        duration = time() - start_time
        print(duration)
    return wrapper

class Level:
    def __init__(self):

        # игровая поверхность
        self.display_surface = pygame.display.get_surface()
        self.earth_size = pygame.image.load('../tiled/ProjectMap.png').convert_alpha().get_size()
        self.earth_width, self.earth_height = self.earth_size[0], self.earth_size[1]

        # группа спрайтов
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        # спрайты атак
        self.current_attack = None

        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.player)

        # небо
        self.rain = Rain(self.all_sprites, self.player)
        self.sky = Sky()

        self.pathfinder = Pathfinder(self.matrix, self.player)

    def setup(self):

        tmx_data = load_pygame('../tiled/ProjectMap.tmx')
        non_matrix = {}

        # составляем карту столкновений
        for layer in tmx_data.visible_layers:
            if layer.name not in ['HouseAnimateObjects', 'HouseObjects', 'HouseObjectsUnder', 'Player', 'Enemy']:
                for x, y, surf in tmx_data.get_layer_by_name(layer.name).tiles():
                    if type(non_matrix.get(x)) == dict:
                        if non_matrix[x].get(y) in [0, 1]:
                            if non_matrix[x][y] == 1 and layer.name == 'Collision':
                                non_matrix[x][y] = 0
                        else:
                            non_matrix[x][y] = 0 if layer.name == 'Collision' else 1
                    else:
                        non_matrix[x] = {}

        self.matrix = []
        for k in sorted(non_matrix.keys()):
            self.matrix.append(non_matrix[k])

        for index,d in enumerate(self.matrix):
            l = [1] if 0 not in d else []
            l.extend([i[1] for i in sorted(d.items())])
            self.matrix[index] = l

        #дом
        # пол и напольные покрытия
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        # анимации в доме
        television_frames = import_folder('../graphics/television')
        stove_frames = import_folder('../graphics/stove')
        for obj in tmx_data.get_layer_by_name('HouseAnimateObjects'):
            if obj.name == 'TV':
                AnimateTile((obj.x, obj.y), television_frames, self.all_sprites)
            if obj.name == 'stove':
                AnimateTile((obj.x, obj.y), stove_frames, self.all_sprites)

        # стены и то, что на стенах
        for layer in ['HouseWalls', 'HouseWallsFurniture']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['main'])

        # объекты, которые может что-то перекрывать и объекты перекрывающие их
        for layer in ['HouseObjects', 'HouseObjectsUnder']:
            for obj in tmx_data.get_layer_by_name(layer):
                Generic((obj.x, obj.y), obj.image, self.all_sprites, LAYERS['main'])


        # объекты столкновений
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Collision((x*TILE_SIZE, y*TILE_SIZE), surf, self.collision_sprites, LAYERS['main'])

        # вода
        water_frames = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            AnimateTile((x*TILE_SIZE, y*TILE_SIZE), water_frames, self.all_sprites, z=LAYERS['water'])

        # объекты взаимодействия
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name in ['Bed', 'Toilet']:
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

        # враги
        for obj in tmx_data.get_layer_by_name('Enemy'):
            Enemy(obj.name, (obj.x, obj.y), self.all_sprites)

        # игрок
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    self.create_attack,
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    interaction=self.interaction_sprites)

        Generic(
            pos=(0,0),
            surf=pygame.image.load('../tiled/ProjectMap.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground']
        )

    def create_attack(self):
        Weapon(self.player, self.all_sprites)

    #@duration_decorator
    def run(self, dt):

        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        # дождь
        if self.player.raining:
            self.rain.update()

        # время суток
        self.sky.display(dt, self.player.night)

        # интерфейс игрока
        self.overlay.display(self.player, dt)

        # затемнение если игрок взаимодействует с чем-то
        if self.player.interact:
            self.transition.play()

        if self.player.click_path:
            self.pathfinder.create_path()
            self.player.click_path = False
        self.pathfinder.update()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH_HALF
        self.offset.y = player.rect.centery - SCREEN_HEIGHT_HALF

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.top):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)