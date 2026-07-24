import random
import numpy as np

class Team:

    """ کلاس نشان دهنده یک تیم ملی فوتبال است اطلاعات و آمار تیم را نگهداری کرده و امکان شبیه‌سازی بازی و ضربات پنالتی را فراهم می‌کند."""

    def __init__(self, name, attack_rating, defense_rating, fifa_rank):

        """مقداردهی اولیه یک تیم.
        Args:
            name (str): نام تیم.
            attack_rating (int): امتیاز خط حمله (۰ تا ۱۰۰).
            defense_rating (int): امتیاز خط دفاع (۰ تا ۱۰۰).
            fifa_rank (int): رنک فیفا.
        """
        self.name = name
        self.attack_rating = attack_rating
        self.defense_rating = defense_rating
        self.fifa_rank = fifa_rank
        self.goals_scored = 0
        self.goals_conceded = 0
        self.points = 0
        self.group_name = None


    def goal_difference(self):

        """محاسبه تفاضل گل‌ها.
        Returns:
            int: تفاضل گل زده منهای گل خورده.
        """

        return self.goals_scored - self.goals_conceded

    def reset_stats(self):

        """بازنشانی آمار تیم برای شروع تورنمنت جدید.
        گل زده، گل خورده و امتیاز را صفر می‌کند.
        Returns:
            None
        """

        self.goals_scored = 0
        self.goals_conceded = 0
        self.points = 0

    def simulate_match(self, opponent_team, time_factor=1.0):

        """شبیه‌سازی نتیجه یک بازی با استفاده از توزیع پواسون.
        Args:
            opponent_team (Team): تیم حریف.
            time_factor (float): ضریب زمان بازی.
        Returns:
            tuple[int, int]: گل‌های دو تیم.
        """
        expected_goals_self = (self.attack_rating / 100) * 1.5 + (1 - opponent_team.defense_rating / 100) * 0.8
        expected_goals_opponent = (opponent_team.attack_rating / 100) * 1.5 + (1 - self.defense_rating / 100) * 0.8

        expected_goals_self *= time_factor
        expected_goals_opponent *= time_factor

        goals_self = np.random.poisson(expected_goals_self)  #  تولید یک عدد تصادفی از توضیع پواسون برای محاسبه تعداد گل تیم خودی
        goals_opponent = np.random.poisson(expected_goals_opponent)  # تولید یک عدد تصادفی از توضیع پواسون برای محاسبه تعداد گل تیم مقابل
        return goals_self, goals_opponent

    def _penalty_kick_scored(self, opponent_team):
        """شبیه‌سازی یک ضربه پنالتی و برگرداندن True/False."""
        penalty = 0.75 + (self.attack_rating - opponent_team.defense_rating) / 250
        penalty = max(0.6, min(0.9, penalty))
        return random.random() < penalty
