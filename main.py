import pygame
import configs
import assets
from objects.background import Background
from objects.floor import Floor
from objects.column import Column


pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT)) 
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True

assets.load_sprites()

sprites = pygame.sprite.LayeredUpdates()

Background(0, sprites)
Background(1, sprites)

Floor(0, sprites)
Floor(1, sprites)

pygame.time.set_timer(column_create_event, 2500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == column_create_event:
            Column(sprites)
    
    screen.fill("black")

    sprites.draw(screen)
    sprites.update()

    pygame.display.flip()
    clock.tick(configs.FPS)
    
pygame.quit()