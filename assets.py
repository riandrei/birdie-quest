import os
import pygame
from objects.scores import resource_path

sprites = {}

def load_sprites():
    # Use resource_path to locate the assets/sprites folder
    path = resource_path('assets/sprites')
    for file in os.listdir(path):
        # Load each sprite and store it in the sprites dictionary
        sprite_name = file.split('.')[0]
        sprites[sprite_name] = pygame.image.load(os.path.join(path, file))

def get_sprite(name):
    return sprites[name]