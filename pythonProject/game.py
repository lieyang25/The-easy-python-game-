import sys
import pygame
from settings import Settings
from time import sleep
from game_stats import GameStats
from my_ship import MY_ship
from bullets import Bullet
from alien import Alien
from button import Button
from score import Score


class Alien_game:
    def __init__(self):
        """初始化"""
        pygame.init()
        self.settings = Settings()
        """屏幕界面"""
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.ship = MY_ship(self)
        pygame.display.set_caption('Player vs Alien')
        """组"""
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        """添加外星人"""
        self._creat_fleet()
        self.stats = GameStats(self)
        """结束条件"""
        self.game_over = False
        """图"""
        self.play_button = Button(self, 'play')

        self.s_b = Score(self)

    def run_game(self):
        pygame.font.init()
        background = pygame.image.load('images/1-1.png').convert()
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('music/BJ_1.ogg')
        pygame.mixer.music.play(-1, start=0)

        while pygame.mixer.music.get_busy():

            # pygame.time.Clock().tick(10)
            self._check_events()
            if self.game_over:
                self._alien_update()
                self._update_bullets()
                self.ship.update()

            self._update_screen(background)

            self.clock.tick(60)

    def _update_screen(self, background):

        self.screen.fill(self.settings.sc_color)
        self.screen.blit(background, (0, 0))
        self.ship.blitem()  # 绘制飞船
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.s_b.show_score()
        self.aliens.draw(self.screen)

        if not self.game_over:
            self.play_button.draw_button()

        pygame.display.flip()

    def check_alien(self):
        for alien in self.aliens.sprites():
            # print(1)
            if alien.rect.left <= 0:
                print(1)
                self._ship_hit()
                break

    # 玩家碰撞后结果
    def _ship_hit(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            # print(self.stats.ships_left)
            self.bullets.empty()  # 重置子弹和alien
            self.aliens.empty()

            self._creat_fleet()  # 新建外星人和重置玩家位置
            self.ship.center_ship()

            sleep(0.5)  # 暂停0.5秒
        else:
            self.game_over = False
            pygame.mouse.set_visible(True)

    # 检测alien碰撞墙壁
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    # 重置alien位移方向
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.alien_x_speed
        self.settings.fleet_direction *= -1

    # 检测外星人碰撞
    def _alien_update(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            # print('重铸1096之光，人人有责！')
        self.check_alien()

    # 生成alien并控制外星人位移
    def _creat_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_y, current_x = 2 * alien_height, 25 * alien_width
        while current_x < (self.settings.screen_width - alien_width):
            while current_y < (self.settings.screen_height - 2 * alien_height):
                self._current_y(current_y, current_x)
                current_y += 2 * alien_width
            current_y = 2 * alien_height
            current_x += 2 * alien_width

    #   控制alien
    def _current_y(self, current_y, current_x):
        new_alien = Alien(self)
        new_alien.y = current_y
        new_alien.rect.y = current_y
        new_alien.rect.x = current_x
        self.aliens.add(new_alien)

    # 生成子弹
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_()

    # 检测子弹的碰撞
    def _check_bullet_(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)

            self.s_b.prep_score()
        if not self.aliens:
            self.bullets.empty()
            self._creat_fleet()

            self.settings.speed_up()
            self.stats.level += 1
            self.s_b.prep_level()

    # 键盘控制
    def _check_events(self):
        '''游戏主体循环'''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mous_pop = pygame.mouse.get_pos()
                self._check_button(mous_pop)
            elif event.type == pygame.KEYDOWN:
                self._KEY_TR(event)
            elif event.type == pygame.KEYUP:
                self._KEY_FA(event)

    def _check_button(self, mous_pos):
        button_clicked = self.play_button.rect.collidepoint(mous_pos)
        if button_clicked and not self.game_over:
            self.game_over = True

            self.stats.rest_stats()
            self.s_b.prep_score()
            self.s_b.prep_level()
            self.bullets.empty()
            self.aliens.empty()

            self.ship.center_ship()
            self._creat_fleet()

            self.settings.speed_reduction()
            pygame.mouse.set_visible(False)

    # 刷新屏幕

    # 开火
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullets = Bullet(self)
            self.bullets.add(new_bullets)

    def _KEY_TR(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        if event.key == pygame.K_a:
            self.ship.moving_left = True
        if event.key == pygame.K_w:
            self.ship.moving_top = True
        if event.key == pygame.K_s:
            self.ship.moving_bottom = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _KEY_FA(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        if event.key == pygame.K_a:
            self.ship.moving_left = False
        if event.key == pygame.K_w:
            self.ship.moving_top = False
        if event.key == pygame.K_s:
            self.ship.moving_bottom = False


if __name__ == '__main__':
    ai = Alien_game()
    ai.run_game()

