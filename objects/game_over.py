import pygame

import assets
import configs
import json
from layer import Layer
from objects.scores import Scores

class GameOverButton(pygame.sprite.Sprite):
    def __init__(self, option_name, y_position, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite(option_name)
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, y_position))
        super().__init__(*groups)

    def highlight(self, is_selected, option_name):
        if is_selected:
            highlight_surface = self.image.copy()
            highlight_surface.fill((255, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
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
        self.original_image = assets.get_sprite('ice_frame')
        self.image = pygame.transform.scale(
                self.original_image, 
                (int(self.original_image.get_width() * 1.5), int(self.original_image.get_height() * 1.5))
            )

        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT/ 2 + 110))
        super().__init__(*groups)

class GameOverScores(pygame.sprite.Sprite):
    def __init__(self, asset_name, y_position, score, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite(asset_name)
        
        self.score_images = []
        for digit in str(score):
            digit_image = assets.get_sprite(digit)
            self.score_images.append(digit_image)
        
        total_width = self.image.get_width() + sum([img.get_width() for img in self.score_images]) + (len(self.score_images) - 1) * 5  
        total_height = max(self.image.get_height(), max([img.get_height() for img in self.score_images])) 
        
        combined_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        
        combined_surface.blit(self.image, (0, 0))
        
        x_offset = self.image.get_width() 
        for score_img in self.score_images:
            combined_surface.blit(score_img, (x_offset, (total_height - score_img.get_height()) // 2)) 
            x_offset += score_img.get_width() + 5  
        
        self.image = combined_surface
        
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, y_position))
        
        super().__init__(*groups)


class Overlay(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.OVERLAY
        self.image = pygame.Surface((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 200))  # Black with 200 alpha for semi-transparent overlay
        self.rect = self.image.get_rect()
        super().__init__(*groups)

class GameOver(pygame.sprite.Sprite):
    def __init__(self, sprites,current_score=0,):
        self.scores = Scores.load_scores(Scores)
        self.best_score = self.scores[0][0] if len(self.scores) > 0 else 0
        self.game_over_board = GameOverBoard(sprites)
        self.game_over_message = GameOverMessage(sprites)
        self.game_over_best = GameOverScores('best', configs.SCREEN_HEIGHT / 2 - 20, self.best_score, sprites)
        self.game_over_score = GameOverScores('score', configs.SCREEN_HEIGHT / 2 + 20, current_score, sprites)

        self.options = [
            GameOverButton('retry', configs.SCREEN_HEIGHT / 2 + 100, sprites),
            GameOverButton('home', configs.SCREEN_HEIGHT/ 2 + 120, sprites),
        ]
        self.overlay = Overlay(sprites)
        self.selected_option = 0
        self.option_names = ['retry', 'home']


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
        self.game_over_board.kill()
        self.game_over_message.kill()
        self.overlay.kill()
        self.game_over_best.kill()
        self.game_over_score.kill()
        
        