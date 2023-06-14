from pygame.math import Vector2


# Экран
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_WIDTH_HALF = SCREEN_WIDTH // 2
SCREEN_HEIGHT_HALF = SCREEN_HEIGHT // 2
TILE_SIZE = 64

# место для оверлея
OVERLAY_POSITIONS = {
    'previous_weapon': (SCREEN_WIDTH//2 - 32, SCREEN_HEIGHT-40),
    'weapon': (SCREEN_WIDTH//2, SCREEN_HEIGHT - 40),
    'next_weapon': (SCREEN_WIDTH//2 + 32, SCREEN_HEIGHT - 40)
}

# враги
monster_data = {
    'mouse': {'health': 100, 'damage': 10, 'resistance': 10, 'speed': 100, 'attack_radius': 50, 'notice_radius': 350}
}

# слои
LAYERS = {
    'water': 0,
    'ground': 1,
    'rain floor': 2,
    'rain drops': 3,
    'house bottom': 4,
    'main': 5,
}