import pygame
from settings import *
from support import *
from timer import Timer
from random import choice
from entity import Entity

class Player(Entity):
    def __init__(self, create_attack, pos, group, collision_sprites, interaction):
        super().__init__(group)

        self.import_assets()
        self.status = 'idle'
        self.status_idle = True

        # взаимодействия
        self.interaction_status = None  # Взаимодействует ли игрок в данный момент
        self.interact = False  # Чтобы отслеживать время затемнения/освещения
        self.interact_sprite = None  # Чтобы знать объект, с которым взаимодействуем
        self.former_place_x = None  # Чтобы вернуться на место до взаимодействия
        self.former_place_y = None
        self.action = False

        self.raining = False
        self.night = False

        # основные настройки
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['main']

        # атрибуты движения
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # путь
        self.path = []
        self.collision_rects = []
        self.click_path = False

        # для столкновений
        self.hitbox = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.collision_sprites = collision_sprites
        self.interaction = interaction

        # таймеры
        self.timers = {'weapon_use': Timer(300, self.use_weapon),
                       'weapon_switch': Timer(300),
                       'interaction_delay': Timer(500)
                       }

        # оружия
        self.weapons = ['claws', 'tail', 'fungs']
        self.weapon_index = 0
        self.selected_weapon = self.weapons[self.weapon_index]
        self.attack_status = False
        self.create_attack = create_attack

        # индикаторы
        self.max_health = 1000
        self.health = 1000

    def use_weapon(self):
        pass

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'idle': [],
                           'sleeping': [], 'pissing': [],
                           'licking_left': [], 'licking_right': [], 'stretch': []}

        for animation in self.animations.keys():
            full_path = '../graphics/player/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
            self.status_idle = True
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        '''Отслеживание нажатий на кнопки.'''
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_path = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    if self.raining:
                        self.raining = False
                    else:
                        self.raining = True
                if event.key == pygame.K_n:
                    if self.night:
                        self.night = False
                    else:
                        self.night = True

        # Нажатия на все кнопки проверяются только если нет анимации атаки
        if not self.timers['weapon_use'].active:
            # кнопка взаимодействия 'F'
            if keys[pygame.K_f]:
                if not self.timers['interaction_delay'].active and \
                        not any([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]):
                    self.timers['interaction_delay'].activate()
                    collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                    if collided_interaction_sprite:
                        self.direction.x = self.direction.y = 0
                        self.interact = True
                        self.interact_sprite = collided_interaction_sprite[0]
                        if not self.interaction_status:
                            self.former_place_x, self.former_place_y = self.rect.centerx, self.rect.centery
                            if collided_interaction_sprite[0].name == 'Bed':
                                self.interaction_status = 'cat_sleeping'
                            elif collided_interaction_sprite[0].name == 'Toilet':
                                self.interaction_status = 'cat_pissing'
                        else:
                            self.interaction_status = None

            # Нажатия на кнопки движения, атаки, смены оружия
            # проверяются только если мы ни с чем не взаимодействуем
            if not self.interaction_status and not self.interact:

                    # временно __________________________________
                if any([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]):
                    if self.health > 0:
                        self.health -= 0.1
                    #____________________________________________

                if keys[pygame.K_w]:
                    self.direction.y = -1
                    self.status = 'up'
                elif keys[pygame.K_s]:
                    self.direction.y = 1
                    self.status = 'down'
                else:
                    self.direction.y = 0

                if keys[pygame.K_d]:
                    self.direction.x = 1
                    self.status = 'right'
                elif keys[pygame.K_a]:
                    self.direction.x = -1
                    self.status = 'left'
                else:
                    self.direction.x = 0

                # использование оружия
                if keys[pygame.K_SPACE]:
                        #if not self.attack_status:
                        self.timers['weapon_use'].activate()
                        self.create_attack()
                        # else:
                        #     self.attack_status = False

                # смена оружия
                if keys[pygame.K_q] and not self.timers['weapon_switch'].active:
                    self.timers['weapon_switch'].activate()
                    self.weapon_index += 1
                    if self.weapon_index >= len(self.weapons):
                        self.weapon_index = 0
                    self.selected_weapon = self.weapons[self.weapon_index]

    def get_status(self):

        if self.direction.magnitude() == 0:
            if not self.interaction_status and not self.interact:
                if self.status_idle:
                    self.status = choice(['idle', 'licking_left', 'licking_right', 'stretch'])
                    self.status_idle = False

            # временно__________________________________________
            elif self.interaction_status == 'sleeping':
                if self.health < self.max_health:
                    self.health += 0.1
            #___________________________________________________

        if self.timers['weapon_use'].active:
            self.attack_status = f"{self.selected_weapon}_{self.status}" if self.direction.x and self.direction.y != 0 else \
                f"{self.selected_weapon}_idle"


    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):

        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)
