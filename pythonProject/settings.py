class Settings:
    def __init__(self):
        """屏幕颜色和高宽"""
        self.sc_color = (230, 230, 230)
        self.screen_width = 1200
        self.screen_height = 800

        """飞船速度"""
        self.sp_x = 10
        self.sp_y = 10
        self.ship_limit = 3

        """子弹设置"""
        self.bullet_speed = 10
        self.bullet_width = 3
        self.bullet_height = 25
        self.bullet_color = (215, 45, 205)
        self.bullet_allowed = 5

        """alien速度"""
        self.alien_y_speed = 2
        self.alien_x_speed = 2
        self.fleet_direction = 1

        """速度提升"""
        self.speed_up_number = 1.5
        self.alien_points_upspeed = 2
        """还原"""
        self.speed_reduction()

    def speed_reduction(self):
        self.alien_y_speed = 2
        self.alien_x_speed = 2
        self.fleet_direction = 1

        self.sp_x = 5
        self.sp_y = 5
        self.ship_limit = 3

        self.bullet_speed = 10

        self.bullet_width = 3
        self.bullet_height = 25

        self.alien_points = 50

    def speed_up(self):
        self.alien_y_speed *= self.speed_up_number
        self.alien_x_speed *= self.speed_up_number

        self.sp_x *= self.speed_up_number
        self.sp_y *= self.speed_up_number

        self.bullet_speed *= self.speed_up_number

        self.bullet_width *= self.speed_up_number
        self.bullet_height *= self.speed_up_number

        self.alien_points *= self.alien_points_upspeed