import pygame
import json
import configs
import assets
from layer import Layer
from datetime import datetime

import os

class ScoreEntry(pygame.sprite.Sprite):
    def __init__(self, text, y_position, *groups):
        print('test')
        self._layer = Layer.UI
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, y_position))
        super().__init__(*groups)

class ScoresText(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite('gameover')
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2 - 150))
        super().__init__(*groups)

class BackButton(pygame.sprite.Sprite):
    def __init__(self, option_name, y_position, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite(option_name)
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, y_position))
        super().__init__(*groups)

    def highlight(self, is_selected, option_name):
        if is_selected:
            highlight_surface = self.image.copy()
            highlight_surface.fill((200, 200, 200), special_flags=pygame.BLEND_RGB_ADD)
            self.image = highlight_surface
        else:
            self.image = assets.get_sprite(option_name)

class Scores:
    FILE_PATH = 'scores.json'

    def __init__(self, sprites):
        self.options = [
            BackButton('start', configs.SCREEN_HEIGHT - 50, sprites),
        ]
        self.scores_text = ScoresText(sprites)
        self.selected_option = 0
        self.option_names = ['start']

        self.entries = []
        self.scores = self.load_scores()
        start_y = configs.SCREEN_HEIGHT / 2 - 80
        spacing = 20

        self.show_scores = False

        for i, (name, score) in enumerate(self.scores):
            entry_text = f'{name}         {score}'
            y_position = start_y + i * spacing
            entry = ScoreEntry(entry_text, y_position, sprites)
            self.entries.append(entry)
    
    def load_scores(self):
        try:
            with open(Scores.FILE_PATH, 'r') as file:
                scores = json.load(file)
                # Sort scores by the score value (index 0), in descending order
                scores.sort(key=lambda x: x[0], reverse=True)
                return scores
        except FileNotFoundError:
            return [(100, datetime.now().strftime("%m-%d-%y")), (20, datetime.now().strftime("%m-%d-%y")), (30, datetime.now().strftime("%m-%d-%y"))]

    def clear(self):
        for entry in self.entries:
            entry.kill()
        for option in self.options:
            option.kill()
        self.scores_text.kill()

    def update(self):
        for i, option in enumerate(self.options):
            option.highlight(i == self.selected_option, self.option_names[i])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.selected_option
        return None