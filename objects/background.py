import pygame.sprite
import assets
import configs
from layer import Layer

class Background(pygame.sprite.Sprite):
    def __init__(self, index, *groups):
        self._layer = Layer.BACKGROUND
        self.image = assets.get_sprite('bg')
        self.rect = self.image.get_rect(topleft=((configs.SCREEN_WIDTH * 2) * index, 0))

        super().__init__(*groups)

    def update(self):
        self.rect.x -= 1

        if self.rect.right <= 0:
            self.rect.x = configs.SCREEN_WIDTH * 2
