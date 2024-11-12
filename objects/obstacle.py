import pygame.sprite
import assets
import configs
import random
from layer import Layer

class SmallObstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_top_gap, obstacle_bottom_gap, *groups):
        self._layer = Layer.OBSTACLE
        self.image = assets.get_sprite('ice-block')
        
        self.movement_direction = 'right' if random.random() < 0.5 else 'down'
        if self.movement_direction == 'right':
            self.rect = self.image.get_rect(bottomleft=(configs.SCREEN_WIDTH + random.randint(100, 280), random.randint(0, configs.SCREEN_HEIGHT)))
        else:
            self.rect = self.image.get_rect(topleft=(random.randint(0, configs.SCREEN_WIDTH), -random.randint(100, 280)))
        
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = random.uniform(2, 3) if random.random() < 0.5 else 2

        super().__init__(*groups)

    def update(self):
        if self.movement_direction == 'right':
            self.rect.x -= self.speed
            if self.rect.right <= 0:
                self.kill()
        elif self.movement_direction == 'down':
            self.rect.y += self.speed
            if self.rect.top >= configs.SCREEN_HEIGHT:
                self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.PIPE
        self.gap = 100

        self.sprite = assets.get_sprite('pipe-ice')
        self.sprite_rect = self.sprite.get_rect()

        self.pipe_bottom = self.sprite
        self.pipe_bottom_rect = self.pipe_bottom.get_rect(topleft=(0, self.sprite_rect.height + self.gap))

        self.pipe_top = pygame.transform.flip(self.sprite, False, True)
        self.pipe_top_rect = self.pipe_top.get_rect(topleft=(0, 0))

        self.image = pygame.Surface((self.sprite_rect.width, self.sprite_rect.height * 2 + self.gap), pygame.SRCALPHA)
        self.image.blit(self.pipe_bottom, self.pipe_bottom_rect)
        self.image.blit(self.pipe_top, self.pipe_top_rect)

        
        self.mask = pygame.mask.from_surface(self.image)

        sprite_floor_height = assets.get_sprite('gnd').get_rect().height
        min_y = 100
        max_y = configs.SCREEN_HEIGHT - sprite_floor_height - 100

        self.rect = self.image.get_rect(midleft=(configs.SCREEN_WIDTH, random.uniform(min_y, max_y)))

        self.gap_top_y = self.rect.y + self.pipe_top_rect.height
        self.gap_bottom_y = self.rect.y + self.pipe_top_rect.height + self.gap

        self.small_obstacles = pygame.sprite.Group()
        for _ in range(random.randint(3, 8)):
            small_obstacle = SmallObstacle(self.gap_top_y, self.gap_bottom_y, *groups)

        self.passed = False
        super().__init__(*groups)

    def update(self):
        self.rect.x -= 2
        self.small_obstacles.update()

        if self.rect.right <= 0:
            self.kill()

    def is_passed(self):
        if self.rect.x < -2 and not self.passed:
            self.passed = True
            return True
        return False