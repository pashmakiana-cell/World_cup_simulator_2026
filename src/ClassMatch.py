class Match:

    """کلاس نماینده یک مسابقه بین دو تیم.
    مدیریت اجرای مسابقه و تعیین نتیجه و برنده.
    """

    def __init__(self, home_team, away_team, is_knockout_stage=False):

        """مقداردهی اولیه مسابقه.
        Args:
            home_team (Team): تیم میزبان.
            away_team (Team): تیم میهمان.
            is_knockout_stage (bool): مشخص‌کننده حذفی بودن مسابقه.
        """

        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.is_knockout_stage = is_knockout_stage
        self.penalty_score = None
        self.winner = None

    def simulate_penalty_shootout(self):

        """شبیه‌سازی ضربات پنالتی تا مشخص شدن برنده.
        Returns:
            tuple[Team, tuple[int, int]]: تیم برنده و نتیجه پنالتی.
        """

        home_penalty_score = 0
        away_penalty_score = 0
        for _ in range(5):
            if self.home_team._penalty_kick_scored(self.away_team):
                home_penalty_score += 1
            if self.away_team._penalty_kick_scored(self.home_team):
                away_penalty_score += 1

        while home_penalty_score == away_penalty_score:
            if self.home_team._penalty_kick_scored(self.away_team):
                home_penalty_score += 1
            if self.away_team._penalty_kick_scored(self.home_team):
                away_penalty_score += 1

        winner = self.home_team if home_penalty_score > away_penalty_score else self.away_team
        self.winner = winner
        return winner, (home_penalty_score, away_penalty_score)

    def play_full_match(self):

        """اجرای مسابقه شامل وقت اصلی و در صورت نیاز وقت اضافه و پنالتی.
        Returns:
            tuple[int, int]: نتیجه نهایی دو تیم. 
        """

        self.home_score, self.away_score = self.home_team.simulate_match(self.away_team)
        if self.home_score == self.away_score and self.is_knockout_stage:
            et_home, et_away = self.home_team.simulate_match(self.away_team, 0.33)
            self.home_score += et_home
            self.away_score += et_away

            if self.home_score == self.away_score:
                winner_penalty, info_penalty = self.simulate_penalty_shootout()
                self.winner = winner_penalty
                self.penalty_score = info_penalty
            else:
                self.winner = self.home_team if self.home_score > self.away_score else self.away_team

        elif self.home_score > self.away_score:
            self.winner = self.home_team
        elif self.home_score < self.away_score:
            self.winner = self.away_team
        else:
            self.winner = None  # تساوی در مرحله گروهی نیازی به پنالتی ندارد

        return self.home_score, self.away_score

    def play(self):

        """اجرای مسابقه و به‌روزرسانی گل‌ها و امتیاز تیم‌ها.
        Returns:
            Team | None: تیم برنده یا None در صورت تساوی.
        """

        self.home_score, self.away_score = self.play_full_match()
        self.home_team.goals_scored += self.home_score
        self.home_team.goals_conceded += self.away_score
        self.away_team.goals_scored += self.away_score
        self.away_team.goals_conceded += self.home_score

        if not self.is_knockout_stage:
            if self.home_score > self.away_score:
                self.home_team.points += 3
            elif self.home_score < self.away_score:
                self.away_team.points += 3
            else:
                self.home_team.points += 1
                self.away_team.points += 1

        return self.winner

    def score_str(self):

        """تولید رشته متنی نتیجه مسابقه برای نمایش.
        Returns:
            str: رشته‌ای شامل نام و گل دو تیم، و در صورت وجود نتیجه
            ضربات پنالتی.
        """
        
        text = f"{self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}"
        if self.penalty_score:
            text += f" ({self.penalty_score[0]}-{self.penalty_score[1]} pens)"
        return text