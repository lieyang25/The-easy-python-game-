import pygame
from settings import Settings


class MY_ship:
    def __init__(self, ai_game):
        """初始化"""
        self.settings = Settings()

        """获取屏幕大小信息"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        """获取图片信息"""
        self.image = pygame.image.load('images/player.png')
        self.rect = self.image.get_rect()
        """控制飞船位置"""
        self.rect.midleft = self.screen_rect.midleft
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_bottom = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.sp_x
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.sp_x
        if self.moving_top and self.rect.top > 0:
            self.rect.y -= self.settings.sp_y
        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.sp_y

    def blitem(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):

        self.rect.midleft = self.screen_rect.midleft
        self.y = self.rect.y
        self.x = self.rect.x