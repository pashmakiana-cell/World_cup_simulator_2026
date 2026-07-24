# ================================
# دانشجو: [Amir Hossein Pashmakian]
# شماره دانشجویی: [404130493]
# عنوان پروژه: شبیه‌ساز جام جهانی
# تاریخ تحویل: [1405/04/26]
# ================================

from pathlib import Path

from ClassWorldCupSimulator import WorldCupSimulator

# مسیر ریشه‌ی پروژه (یک پوشه بالاتر از src/) و مسیر پیش‌فرض فایل CSV

BASE_DIR = Path(__file__).resolve().parent.parent  # یک پوشه بالاتر از src (ریشه‌ی پروژه)
DEFAULT_CSV_PATH = BASE_DIR / "data" / "worldcup_2026_teams.csv"

# ----------------------Menu / Main----------------------

def print_menu():
    """Chape menuye aslie barname."""
    print("\n===== Shabih saze Jame Jahani =====")
    print("1) Bargozarie team ha az file CSV")
    print("2) Anjame ghorekeshie group ha (seed bandi e khodkar)")
    print("3) Ejraye marhaleye goroohi va namayeshe jadvale har group")
    print("4) Ejraye kamele Jam (goroohi + hazfi) va namayeshe ghahreman")
    print("5) Shabihsazie 1000 bare va gozareshe darsade ghahremani")
    print("6) Namayeshe brackete hazfie akharin shabihsazi")
    print("7) Namayeshe nemoodare ehtemale ghahremani")
    print("8) Khorooj")


def main():
    """حلقه اصلی برنامه و مدیریت منو."""
    simulator = WorldCupSimulator()
    teams_loaded = False        # وضعیت بارگذاری تیم‌ها از فایل
    groups_drawn = False        # وضعیت انجام قرعه‌کشی گروه‌ها

    while True:
        print_menu()
        choice = input("Entekhabe shoma: ").strip()

# ================= بارگذاری فایل تیم‌ها ================= 

        if choice == '1':
            try:
                file_ip = input(f"Enter your file path (press Enter for {DEFAULT_CSV_PATH.name}): ").strip()
                if file_ip == '':  # یعنی کاربر فایل ورلد کاپ ۲۰۲۶ تیمز رو انتخاب کرده
                    file_ip = str(DEFAULT_CSV_PATH)
                teams_loaded = simulator.load_teams_from_csv(file_ip)

            except Exception:
                print("Value eshtebah.")

# ================= قرعه‌کشی گروه‌ها =================

        elif choice == '2':
            if not teams_loaded:
                print("Ebteda team ha ro bargozari konid.")
                continue
            groups_drawn = simulator.groups_draw_and_seed() # انجام قرعه‌کشی و تشکیل گروه‌ها

# ================= اجرای مرحله گروهی =================

        elif choice == '3':
            if not groups_drawn:
                print("Ebteda team ha ro bargozari konid.")
                continue
            simulator.run_group_stage()
            group_stage_played = True
            
 # ================= اجرای کامل جام جهانی =================

        elif choice == '4':
            if not teams_loaded:
                print("Ebteda team ha ro bargozari konid.")
                continue

            champion = simulator.simulation_full_run()    # اجرای کامل جام جهانی
            groups_drawn = True

            print(f"\n🏆 Ghahremane Jame Jahani: {champion.name}")

# ================= اجرای چندباره شبیه‌سازی ================= 

        elif choice == '5':
            if not teams_loaded:
                print("Ebteda team ha ro bargozari konid.")
                continue

            raw = input("Tedade shabihsazi (Enter = 1000): ").strip()

            try:
                num = 1000 if raw == "" else int(raw)
            except ValueError:
                print("Khata: adad motabar vared konid.")
                continue

            simulator.most_likely_champion(num)

# ================= نمایش براکت مرحله حذفی =================

        elif choice == '6':
            if simulator.champion is None:
                print("Ebteda yek jam ra ejra konid.")
                continue
            simulator.bracket_display()

# ================= رسم نمودار احتمال قهرمانی =================

        elif choice == '7':
            simulator.plot_championship_chances() # نمایش نمودار درصد قهرمانی تیم‌ها

# ================= خروج از برنامه =================

        elif choice == '8':
            print("Khorooj az barname. Movaffagh bashid")
            break

# ================= انتخاب نامعتبر =================

        else:
            print("Gozine namotabar. Lotfan adadi beyn 1 ta 8 vared konid.")

if __name__ == "__main__":
    main()