import random
import pandas as pd

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from ClassTeam import Team
from ClassGroup import Group
from ClassKnockoutStage import KnockoutStage


class WorldCupSimulator:
    
    """کلاس اصلی مدیریت شبیه‌سازی جام جهانی، از بارگذاری تیم‌ها تا تعیین قهرمان و نمایش نتایج."""

    def __init__(self):
        """مقداردهی اولیه شبیه‌ساز با وضعیت خالی (بدون تیم و بدون نتیجه)."""
        self.all_teams = []  # لیستی از ابجکت‌های تمام تیم‌ها (۳۲ تیم)
        self.groups = []  # لیست گروه‌ها (شامل ۸ گروه)
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None
        self.last_percentage = None


    def load_teams_from_csv(self, worldcup_2026_teams):
            """  و ذخیره آن‌ها در لیست تیم‌ها.csv بارگذاری فایل 
            Args:
                worldcup_2026_teams (str): مسیر فایل CSV.
            Returns:
                bool: موفقیت یا عدم موفقیت در بارگذاری فایل.
            """
            
            self.all_teams.clear()

            try:
                df = pd.read_csv(worldcup_2026_teams) 
                print(df.to_string())

                for _, row in df.iterrows():
                    new_team = Team(
                        name=row['name'],
                        attack_rating=int(row['attack']),
                        defense_rating=int(row['defense']),
                        fifa_rank=int(row['rank'])
                    )
                    self.all_teams.append(new_team)

                print(f"Tedade {len(self.all_teams)} team ba movaffaghiat load shod.")

            except Exception as error:
                print(f"Khata dar khandane file: {error}")
                return False
            return True
    
    def groups_draw_and_seed(self, show_output=True):
        """قرعه‌کشی و تشکیل گروه‌ها بر اساس سیدبندی فیفا.
        Args:
            show_output (bool): نمایش گروه‌ها در خروجی.
        Returns:
            bool: موفقیت در تشکیل گروه‌ها.
        """
        self.groups.clear()
        self.all_teams.sort(key=lambda team: team.fifa_rank)  # مرتب کردن تیم‌ها بر اساس رنک فیفا

        # ساخت چهار سید
        seeding_pots = [ self.all_teams[0:8] , self.all_teams[8:16],  self.all_teams[16:24], self.all_teams[24:32] ]

        for pot in seeding_pots: # به‌هم زدن ترتیب هر سید
            random.shuffle(pot)

        group_letters = "ABCDEFGH"  # برای نام‌گذاری ۸ گروه

        for index in range(8):
            group_letter = group_letters[index]
            group_teams = []  # لیستی موقت برای نگهداری تیم‌های یک گروه

            # از هر سید یک تیم بردار و به یک گروه اضافه کن
            # چون از هر سید ۸ تایی یک‌دانه برمی‌داریم، ۸ گروه ۴ عضوی داریم
            for pot in seeding_pots:
                team = pot[index]
                team.group_name = group_letter # تعیین نام گروه تیم
                group_teams.append(team)

            new_group = Group(group_letter, group_teams)
            self.groups.append(new_group)

        if show_output:
            print("Groups created successfully.\n")

            for group in self.groups:
                print(f"===== Group {group.stage_name} =====")
                for team in group.member_teams:
                    print(f"{team.name} (Rank {team.fifa_rank})")
                print()
        return True

    def run_group_stage(self, show_output=True):
        """اجرای کامل مرحله گروهی برای تمام گروه‌ها.

        Args:
            show_output (bool): در صورت True، جدول رده‌بندی هر گروه
                پس از اجرا چاپ می‌شود. مقدار پیش‌فرض True است.

        Returns:
            None
        """
        if show_output:
            print("\n========== GROUP STAGE ==========")

        for g in self.groups:
            g.play_all_matches()
            ranking = g.get_ranking()

            if show_output:
                print(f"\n===== Group {g.stage_name} =====")
                for idx, team in enumerate(ranking, start=1):
                    print(
                        f"{idx}. {team.name} | "
                        f"Pts: {team.points} | "
                        f"GD: {team.goal_difference()} | "
                        f"GF: {team.goals_scored}"
                    )

    def creat_round_of_16(self):
        """ساخت مسابقات یک‌هشتم نهایی از تیم‌های صعودکننده گروه‌ها.

        دو تیم برتر هر گروه استخراج می‌شود و مطابق ساختار استاندارد
        براکت جام جهانی (تیم اول یک گروه مقابل تیم دوم گروه بعدی و
        بالعکس) مسابقات ساخته می‌شود.

        Returns:
            None
        """
        list_1_16 = []

        for g in self.groups:
            first, second = g.advance_teams()
            list_1_16.append(first)
            list_1_16.append(second)

        self.round_of_16 = KnockoutStage("Round of 16")

        for i in range(0, len(list_1_16), 4):
            self.round_of_16.creat_match(list_1_16[i], list_1_16[i + 3])
            self.round_of_16.creat_match(list_1_16[i + 2], list_1_16[i + 1])

    def play_knockout_stage(self, show_output=True):
        """اجرای مرحله حذفی از یک‌هشتم نهایی تا فینال و تعیین قهرمان.

        Args:
            show_output (bool): نمایش نتایج هر دور در صورت True.

        Returns:
            Team: تیم قهرمان تورنمنت.
        """
        # Round of 16
        self.round_of_16.play_round()
        if show_output: 
            self.round_of_16.display_results()   # نمایش نتایج یک‌هشتم نهایی
        winners = self.round_of_16.get_winners() # استخراج تیم‌های صعودکننده

        # Quarterfinals 
        self.quarterfinals = KnockoutStage("Quarterfinals")   # ایجاد مرحله یک‌چهارم نهایی
        for i in range(0, len(winners), 2): # ساخت مسابقات یک‌چهارم نهایی
            self.quarterfinals.creat_match(winners[i], winners[i + 1])

        self.quarterfinals.play_round() # اجرای مسابقات یک‌چهارم نهایی
        if show_output: # نمایش نتایج یک‌چهارم نهایی
            self.quarterfinals.display_results() # استخراج تیم‌های صعودکننده
        winners = self.quarterfinals.get_winners()

        # Semifinals
        self.semifinals = KnockoutStage("Semifinals") # ایجاد مرحله نیمه‌نهایی
        for i in range(0, len(winners), 2):# ساخت مسابقات نیمه‌نهایی
            self.semifinals.creat_match(winners[i], winners[i + 1])

        self.semifinals.play_round()# اجرای مسابقات نیمه‌نهایی
        if show_output:    # نمایش نتایج نیمه‌نهایی
            self.semifinals.display_results()
        winners = self.semifinals.get_winners()# استخراج تیم‌های صعودکننده

        # Final
        self.final = KnockoutStage("Final") # ایجاد مسابقه فینال
        self.final.creat_match(winners[0], winners[1])
 
        self.final.play_round() # اجرای مسابقه فینال
        if show_output:
            self.final.display_results()   # نمایش نتیجه فینال

        # Champion
        self.champion = self.final.get_winners()[0] # تعیین تیم قهرمان

        return self.champion

    def simulation_full_run(self, show_output=True):

        """اجرای کامل شبیه‌سازی جام جهانی از قرعه‌کشی تا تعیین قهرمان.

        Args:
            show_output (bool): نمایش جزئیات مراحل در صورت True.

        Returns:
            Team: تیم قهرمان شبیه‌سازی.
        """
        for team in self.all_teams:
            team.reset_stats()

        self.groups_draw_and_seed(show_output)
        self.run_group_stage(show_output)
        self.creat_round_of_16()

        return self.play_knockout_stage(show_output)

    def most_likely_champion(self, num_simulations=1000):

        """اجرای چندباره شبیه‌سازی و محاسبه درصد قهرمانی تیم‌ها.

        Args:
            num_simulations (int): تعداد دفعات اجرای شبیه‌سازی.

        Returns:
            list[tuple[str, float]] | None: درصد قهرمانی هر تیم یا None در صورت نامعتبر بودن ورودی.
        """

        if num_simulations <= 0:
            print("Khata: tedade shabihsazi bayad bozorgtar az sefr bashe.")
            return

        title_counts = {team.name: 0 for team in self.all_teams}

        for _ in range(num_simulations):
            champion = self.simulation_full_run(False)
            title_counts[champion.name] += 1

        percentages = [
            (name, (count / num_simulations) * 100)
            for name, count in title_counts.items()
        ]

        percentages.sort(key=lambda x: x[1], reverse=True)
        self.last_percentage = percentages

        print(f"Shabihsazi {num_simulations} bar anjam shod.")
        print("Darsade ghahremanie har team:")
        for name, pct in percentages:
            if pct > 0:
                print(f"{name}: {pct:.1f}%")

        return percentages

    def bracket_display(self):
        """نمایش کامل براکت حذفی مربوط به آخرین شبیه‌سازی اجراشده.
        Returns:
            None
        """
        if self.round_of_16 is None:
            print("Khata: hanooz hich tournamenti shabihsazi nashode.")
            return

        print("\n========== KNOCKOUT BRACKET ==========\n")
        if self.round_of_16:
            self.round_of_16.display_results()
        if self.quarterfinals:
            self.quarterfinals.display_results()
        if self.semifinals:
            self.semifinals.display_results()
        if self.final:
            self.final.display_results()
        if self.champion:
            print(f"Champion: {self.champion.name}")

    def plot_championship_chances(self, top_n=10):
        """رسم نمودار درصد قهرمانی تیم‌های برتر.

        Args:
            top_n (int): تعداد تیم‌های نمایش‌داده‌شده در نمودار.
        Return : None
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Error: matplotlib is not installed.")
            return

        if not self.last_percentage:
            print("Khata: ebteda gozineye shabihsazie 1000 bare ro ejra konid.")
            return

        top = self.last_percentage[:top_n]
        names = [team for team, _ in top]
        percentages = [pct for _, pct in top]

        plt.figure(figsize=(10, 6))
        plt.bar(names, percentages)
        plt.title("2026 World Cup Championship Probability")
        plt.xlabel("Teams")
        plt.ylabel("Championship Percentage (%)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig("championship_probabilities.png")
        plt.show()

        print("Chart saved as championship_probabilities.png")