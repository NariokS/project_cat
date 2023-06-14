from settings import *
from support import *

class Overlay:
    def __init__(self, player):

        # основные настройки
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # импорты
        self.import_assets()
        overlay_path = '../graphics/UI/Weapons/'
        self.weapon_surfaces = {weapon: pygame.image.load(f'{overlay_path}{weapon}.png').convert_alpha() for weapon in player.weapons}

        # здоровье
        self.health_frame_index = 0
        self.health_status = 'health_bar_3'
        self.health_bar_topleft = (71, 53)
        self.bar_max_width = 100
        self.bar_height = 5
        self.speed_biting = 1

    def import_assets(self):
        self.animations = {'health_bar_3': [], 'health_bar_2': [], 'health_bar_1': [],}

        for animation in self.animations.keys():
            full_path = '../graphics/UI/' + animation
            self.animations[animation] = import_folder(full_path)

    def check_health(self):
        ratio = self.current_bar_width/self.bar_max_width
        if ratio >= 0.7:
            self.health_status = 'health_bar_3'
            self.speed_biting = 1
        elif ratio >= 0.3:
            self.health_status = 'health_bar_2'
            self.speed_biting = 5
        else:
            self.health_status = 'health_bar_1'
            self.speed_biting = 10

    def show_health(self, current, full, dt):
        '''Обновление и отрисовка полоски жизни.'''

        self.health_frame_index += self.speed_biting * dt
        if self.health_frame_index >= len(self.animations[self.health_status]):
            self.health_frame_index = 0
        self.health_bar = self.animations[self.health_status][int(self.health_frame_index)]

        self.display_surface.blit(self.health_bar, (40, 40))
        current_health_ratio = current / full
        self.current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect((self.health_bar_topleft), (self.current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, (185, 23, 64), health_bar_rect)

        self.check_health()

    def display(self, player, dt):

        # оружие
        weapon_surface = self.weapon_surfaces[self.player.selected_weapon]
        weapon_rect = weapon_surface.get_rect(midbottom=OVERLAY_POSITIONS['weapon'])

        # элементы интерфейса
        self.show_health(player.health, player.max_health, dt)
        self.display_surface.blit(weapon_surface, weapon_rect)
