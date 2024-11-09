import assets
import pygame
import configs
from layer import Layer

class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.PLAYER

        self.images = [
            assets.get_sprite('redbird-upflap'),
            assets.get_sprite('redbird-midflap'),
            assets.get_sprite('redbird-downflap')
        ]

        self.image = self.images[0]
        sprite_floor_height = assets.get_sprite('floor').get_rect().height
        self.rect = self.image.get_rect(topleft=(0, (configs.SCREEN_HEIGHT - sprite_floor_height) // 2))

        # Initialize target position
        self.target_y = self.rect.y
        super().__init__(*groups)

    def update(self):
        # Cycle through bird images for flapping animation
        self.images.append(self.images.pop(0))
        self.image = self.images[0]

        # Smoothly move toward target_y
        self.rect.y += (self.target_y - self.rect.y) * 0.2

        # Keep bird within screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > configs.SCREEN_HEIGHT:
            self.rect.bottom = configs.SCREEN_HEIGHT

    def update_marker_position(self, marker):
        # Update target y position based on the marker
        screen_center = configs.SCREEN_HEIGHT / 2
        self.target_y = int((marker - 0.5) * 1.5 * configs.SCREEN_HEIGHT + screen_center)
