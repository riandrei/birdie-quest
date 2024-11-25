import pygame
import configs
import assets
from layer import Layer

class GameName(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite('game_name')
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, 100))
        super().__init__(*groups)

class MenuOption(pygame.sprite.Sprite):
    def __init__(self, option_name, y_position, *groups):
        self._layer = Layer.UI
        self.original_image = assets.get_sprite(option_name)
        self.image =  self.image = pygame.transform.scale(
                self.original_image, 
                (int(self.original_image.get_width() * 2), int(self.original_image.get_height() * 2))
            )
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, y_position ))
        super().__init__(*groups)
    def highlight(self, is_selected, option_name):
        if is_selected:
            highlight_surface = self.original_image.copy().convert_alpha()
            overlay = pygame.Surface(highlight_surface.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 100)) 
        
            highlight_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.image = pygame.transform.scale(
                highlight_surface, 
                (int(self.original_image.get_width() * 2), int(self.original_image.get_height() * 2))
            )
        else:
            self.original_image = assets.get_sprite(option_name)
            self.image =  self.image = pygame.transform.scale(
                self.original_image, 
                (int(self.original_image.get_width() * 2), int(self.original_image.get_height() * 2))
            )

class Overlay(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.OVERLAY
        self.image = pygame.Surface((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 200))
        self.rect = self.image.get_rect()
        super().__init__(*groups)

class Menu:
    def __init__(self, sprites):
        self.options = [
            MenuOption('start', configs.SCREEN_HEIGHT / 2 - 40, sprites),
            MenuOption('scores', configs.SCREEN_HEIGHT / 2 + 40, sprites),
            MenuOption('exit', configs.SCREEN_HEIGHT / 2 + 120, sprites)
        ]
        self.game_name = GameName(sprites)
        self.overlay = Overlay(sprites)
        self.selected_option = 0
        self.show_menu = True
        self.option_names = ['start', 'scores', 'exit']
    
    def update(self):
        for i, option in enumerate(self.options):
            option.highlight(i == self.selected_option, self.option_names[i])
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected_option
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click
                print("Left mouse button clicked")
                for i, option in enumerate(self.options):
                    if option.rect.collidepoint(event.pos):
                        print(f"{self.option_names[i]} selected via left-click")
                        return i
        if event.type == pygame.MOUSEMOTION:
            for i, option in enumerate(self.options):
                if option.rect.collidepoint(event.pos):
                    self.selected_option = i
        return None
        
    def clear(self):
        for option in self.options:
            option.kill()
        self.game_name.kill()
        self.overlay.kill()



