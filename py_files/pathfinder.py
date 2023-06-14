import pygame
from settings import *

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


class Pathfinder:
    def __init__(self, matrix, player):

        # поиск пути
        self.path = []
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.player = player

        self.display_surface = pygame.display.get_surface()

        pygame.mouse.set_visible(False)
        self.cursor_image = pygame.image.load('../graphics/UI/cursor.png').convert_alpha()
        self.cursor_rect = self.cursor_image.get_rect()

        self.cursor_image_ban = pygame.image.load('../graphics/UI/cursor_ban.png').convert_alpha()
        self.cursor_ban_rect = self.cursor_image_ban.get_rect()

    def create_path(self):
        '''Функция для поиска пути от игрока к нажатой точке.'''

        # старт - сам игрок
        start_x, start_y = self.player.rect.centerx//64, self.player.rect.centery//64
        start = self.grid.node(start_x, start_y)

        # конец - позиция мышки
        mouse_pos = pygame.mouse.get_pos()
        end_x, end_y = (mouse_pos[0] + self.different_x) // 64, \
                       (mouse_pos[1] + self.different_y) // 64
        end = self.grid.node(end_x, end_y)

        # путь
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)
        print(self.path)
        print(f"{list((self.matrix[point[0]][point[1]]for point in self.path))}")


        for index_x, x in enumerate(self.matrix):
            for index_y, y in enumerate(x):
                if end_y - 20 <= index_y <= end_y + 10:
                    if end_x - 10 <= index_x <= end_x + 10:
                        print(self.matrix[index_y][index_x], end=' ')
            print()

        self.grid.cleanup()

    def draw_path(self):
        if len(self.path) > 1:
            points = []
            for point in self.path:
                x_true = point[0] * 64 + 32
                y_true = point[1] * 64 + 32

                x_display = x_true - self.player.pos.x + SCREEN_WIDTH_HALF
                y_display = y_true - self.player.pos.y + SCREEN_HEIGHT_HALF

                points.append((x_display, y_display))
                color = (0, 255, 0) if self.matrix[point[0]][point[1]] else (255, 0, 0)
                pygame.draw.rect(self.display_surface, color, (x_display - 32, y_display - 32, 64, 64), 2)

            pygame.draw.lines(self.display_surface, (0, 0, 255), False, points, 2)

    def draw_active_cell(self):
        self.cursor_rect.center = self.cursor_ban_rect.center = pygame.mouse.get_pos()

        self.different_x = self.player.rect.centerx - SCREEN_WIDTH_HALF
        self.different_y = self.player.rect.centery - SCREEN_HEIGHT_HALF

        row = (self.cursor_rect.center[0] + self.different_x) // 64
        col = (self.cursor_rect.center[1] + self.different_y) // 64

        current_cell_value = self.matrix[row][col]

        if current_cell_value:
            self.display_surface.blit(self.cursor_image, self.cursor_rect)
        else:
            self.display_surface.blit(self.cursor_image_ban, self.cursor_ban_rect)

    def update(self):
        self.draw_active_cell()
        self.draw_path()
