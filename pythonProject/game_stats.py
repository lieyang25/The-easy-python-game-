class GameStats:

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.rest_stats()

    def rest_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1