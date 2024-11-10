import pygame.sprite

import assets
import configs
from layer import Layer

class GameOverButton(pygame.sprite.Sprite):
    def __init__(self, option_name, x_position, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite(option_name)
        self.rect = self.image.get_rect(center=(x_position, configs.SCREEN_HEIGHT / 2))
        super().__init__(*groups)

    def highlight(self, is_selected, option_name):
        if is_selected:
            highlight_surface = self.image.copy()
            highlight_surface.fill((200, 200, 200), special_flags=pygame.BLEND_RGB_ADD)
            self.image = highlight_surface
        else:
            self.image = assets.get_sprite(option_name)

class GameOverMessage(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite('gameover')
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2 - 100))
        super().__init__(*groups)

class GameOverBoard(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite('board')
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2))
        super().__init__(*groups)

class GameOver(pygame.sprite.Sprite):
    def __init__(self, sprites):
        self.game_over_board = GameOverBoard(sprites)
        self.game_over_message = GameOverMessage(sprites)

        self.options = [
            GameOverButton('replay', configs.SCREEN_WIDTH / 2 - 20, sprites),
            GameOverButton('home', configs.SCREEN_WIDTH / 2 + 20, sprites),
        ]
        self.selected_option = 0
        self.option_names = ['replay', 'home']

    def update(self):
        for i, option in enumerate(self.options):
            option.highlight(i == self.selected_option, self.option_names[i])
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_RIGHT:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected_option
        return None
    def clear(self):
        for option in self.options:
            option.kill()
        self.game_over_board.kill()
        self.game_over_message.kill()
        
        