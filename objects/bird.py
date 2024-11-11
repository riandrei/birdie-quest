import assets
import pygame
import configs
from layer import Layer
from objects.obstacle import Obstacle
from objects.obstacle import SmallObstacle
from objects.floor import Floor

class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.PLAYER

        self.images = [
            pygame.transform.scale(assets.get_sprite('blue_hat_upflap'), (68, 48)),
            pygame.transform.scale(assets.get_sprite('blue_hat_midflap'), (68, 48)),
            pygame.transform.scale(assets.get_sprite('blue_hat_downflap'), (68, 48))
        ]

        self.image = self.images[0]
        sprite_floor_height = assets.get_sprite('floor').get_rect().height
        self.rect = self.image.get_rect(topleft=(0, (configs.SCREEN_HEIGHT - sprite_floor_height) // 2))

        self.mask = pygame.mask.from_surface(self.image)
        self.target_y = self.rect.y
        self.target_x = self.rect.x
        super().__init__(*groups)

    def update(self):
        self.images.append(self.images.pop(0))
        self.image = self.images[0]

        self.rect.y += (self.target_y - self.rect.y) * 0.2
        self.rect.x += (self.target_x - self.rect.x) * 0.2 

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > configs.SCREEN_WIDTH:
            self.rect.right = configs.SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > configs.SCREEN_HEIGHT:
            self.rect.bottom = configs.SCREEN_HEIGHT

    def update_marker_position(self, marker_x, marker_y):
        screen_center_y = configs.SCREEN_HEIGHT / 2
        screen_center_x = configs.SCREEN_WIDTH / 2

        self.target_y = int((marker_y - 0.5) * 1.5 * configs.SCREEN_HEIGHT + screen_center_y)
        self.target_x = int((1 - marker_x - 0.5) * 1.5 * configs.SCREEN_WIDTH + screen_center_x)


    def check_collision(self, sprites):
        for sprite in sprites:
            if (type(sprite) is Obstacle or type(sprite) is SmallObstacle or type(sprite) is Floor) and sprite.mask.overlap(self.mask, (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)):
                self.image =  pygame.transform.scale(assets.get_sprite('blue_lost'), (68, 48))
                return True
        return False
