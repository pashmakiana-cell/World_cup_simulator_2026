import random 

from functools import cmp_to_key

from ClassMatch import Match

class Group:

    """کلاس نماینده یک گروه در مرحله گروهی.
    مدیریت تیم‌ها، مسابقات، رتبه‌بندی و تعیین تیم‌های صعودکننده گروه. 
    """

    def __init__(self, stage_name, member_teams):
        
        """مقداردهی اولیه گروه.
        Args:
            stage_name (str): نام گروه.
            member_teams (list[Team]): تیم‌های عضو گروه.
        """
        self.stage_name = stage_name
        self.matches = []  # ذخیره مسابقات انجام‌شده گروه
        self.member_teams = member_teams  # نشان‌دهنده لیست تیم‌های عضو آن گروه

    def play_all_matches(self):

        """اجرای تمام مسابقات گروه، به‌طوری که هر دو تیم فقط یک‌بار با هم بازی کنند."""

        for i in range(len(self.member_teams)):
            for j in range(i + 1, len(self.member_teams)):
                match = Match(self.member_teams[i], self.member_teams[j])  # is_knockout_stage=False چون مرحله گروهی است
                match.play()
                self.matches.append(match)

    def _head_to_head_winner(self, team1, team2):
        """پیدا کردن برنده بازی مستقیم بین دو تیم مشخص."""
        for match in self.matches:
            if (match.home_team == team1 and match.away_team == team2) or \
               (match.home_team == team2 and match.away_team == team1):
                return match.winner
        return None

    def get_ranking(self):

        """رتبه‌بندی تیم‌های گروه بر اساس قوانین مسابقات.

        Returns:
            list[Team]: لیست تیم‌ها به ترتیب رتبه.
        """

        def compare(team1, team2):
            if team1.points != team2.points:
                return team2.points - team1.points

            if team1.goal_difference() != team2.goal_difference():
                return team2.goal_difference() - team1.goal_difference()

            if team1.goals_scored != team2.goals_scored:
                return team2.goals_scored - team1.goals_scored

            winner = self._head_to_head_winner(team1, team2)

            if winner is team1:
                return -1  # در ترتیب قرارگیری، تیم اول قبل از تیم دوم قرار گیرد
            if winner is team2:
                return 1  # در ترتیب قرارگیری، تیم دوم قبل از تیم اول قرار گیرد

            return random.choice([-1, 1])

        return sorted(self.member_teams, key=cmp_to_key(compare))

    def advance_teams(self):

        """تعیین دو تیم صعودکننده گروه بر اساس رتبه‌بندی.

        Returns:
            tuple[Team, Team]: تیم اول و تیم دوم گروه به‌ترتیب رتبه.
        """

        ranking = self.get_ranking()
        return ranking[0], ranking[1]