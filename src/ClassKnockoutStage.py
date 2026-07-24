from ClassMatch import Match
from ClassTeam import Team

class KnockoutStage:

    """کلاس نماینده یک مرحله از دور حذفی.
    مدیریت مسابقات، اجرای بازی‌ها و تعیین تیم‌های صعودکننده.
    """

    def __init__(self, round_name):
        """مقداردهی اولیه یک مرحله حذفی.

        Args:
            round_name (str): نام دور (مثلاً "Round of 16", "Final").
        """
        self.round_name = round_name
        self.matches = []

    def creat_match(self, team1: Team, team2: Team):

        """ساخت و افزودن یک مسابقه حذفی جدید بین دو تیم به این دور.

        Args:
            team1 (Team): تیم اول (میزبان فرضی).
            team2 (Team): تیم دوم (میهمان فرضی).

        Returns:
            None
        """
        self.matches.append(Match(team1, team2, is_knockout_stage=True))

    def play_round(self):
        """اجرای تمام مسابقات این دور حذفی.

        Returns:
            None
        """
        for match in self.matches:
            match.play()

    def get_winners(self):

        """برگرداندن لیست تیم‌های برنده که به مرحله بعدی صعود می‌کنند.

        Returns:
            list[Team]: لیست تیم‌های برنده به همان ترتیب مسابقات.
        """
        return [m.winner for m in self.matches]

    def display_results(self):

        """چاپ نتایج تمام مسابقات این دور به همراه برنده هر مسابقه.

        Returns:
            None
        """
        print(f"\n========== {self.round_name} ==========")
        for match in self.matches:
            print(match.score_str())
            if match.winner:
                print(f"Winner: {match.winner.name}")
            print("-" * 40)
