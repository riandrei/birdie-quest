import pygame
import configs
import assets
from layer import Layer

class MenuOption(pygame.sprite.Sprite):
    def __init__(self, option_name, y_position, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite(option_name)
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, y_position ))
        super().__init__(*groups)
    def highlight(self, is_selected, option_name):
        if is_selected:
            highlight_surface = self.image.copy()
            highlight_surface.fill((200, 200, 200), special_flags=pygame.BLEND_RGB_ADD)
            self.image = highlight_surface
        else:
            self.image = assets.get_sprite(option_name)

class Menu:
    def __init__(self, sprites):
        self.options = [
            MenuOption('start', configs.SCREEN_HEIGHT / 2 - 80, sprites),
            MenuOption('scores', configs.SCREEN_HEIGHT / 2, sprites),
            MenuOption('quit', configs.SCREEN_HEIGHT / 2 + 80, sprites)
        ]
        self.selected_option = 0
        self.show_menu = True
        self.option_names = ['start', 'scores', 'quit']
    
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
        return None
        
    def clear(self):
        for option in self.options:
            option.kill()



