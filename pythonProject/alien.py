import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        """图片"""
        self.image = pygame.image.load('images/enemy.png')
        self.rect = self.image.get_rect()
        """位置"""
        self.rect.topright = self.screen_rect.topright
        """记录水平位置"""
        self.x = self.rect.x
        self.y = self.rect.y

        self.settings = ai_game.settings

    def update(self):
        self.y += self.settings.alien_y_speed * self.settings.fleet_direction
        self.rect.y = self.y

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.top <= 0) or (self.rect.bottom >= screen_rect.bottom)