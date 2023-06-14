import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.rect.colliderect(self.hitbox):
                    if pygame.sprite.collide_mask(self, sprite):
                        if direction == 'horizontal':
                            if self.direction.x > 0:
                                self.hitbox.centerx -= 3
                            if self.direction.x < 0:
                                self.hitbox.centerx += 3
                            self.rect.centerx, self.pos.x = self.hitbox.centerx, self.hitbox.centerx

                        if direction == 'vertical':
                            if self.direction.y > 0:
                                self.hitbox.centery -= 3
                            if self.direction.y < 0:
                                self.hitbox.centery += 3
                            self.rect.centery, self.pos.y = self.hitbox.centery, self.hitbox.centery

    def move(self, dt):

        # нормализация вектора
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # движение по горизонтали
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = round(self.pos.x)
        self.collision('horizontal')

        # движение по вертикали
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = round(self.pos.y)
        self.collision('vertical')