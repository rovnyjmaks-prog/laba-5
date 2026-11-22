"""Симулятор підводної цивілізації — демонстраційний скрипт."""
from src import PROJECT_NAME, __version__
from src.colony_manager import ColonyManager
from src.farming_facility import FarmingFacility
from src.research_lab import ResearchLab
from src.residential_dome import ResidentialDome

def main() -> None:
    print("=" * 50)
    print(f"  {PROJECT_NAME}  v{__version__}")
    print("=" * 50)

    colony = ColonyManager("Атлантида-2", energy_supply=150)

    print("\n--- 1. Створення споруд ---")
    colony.add_habitat(ResidentialDome("Альфа", 100, 20, residents=12))
    colony.add_habitat(ResidentialDome("Бета", 250, 15, residents=6))
    colony.add_habitat(ResearchLab("Нептун-Лаб", 600, 8, scientists=4,
                                   specialization="глибоководна біологія"))
    colony.add_habitat(FarmingFacility("Ферма-1", 50, 10, plots=5))
    colony.add_habitat(FarmingFacility("Ферма-2", 120, 6, plots=2, crop="ламінарія"))
    print(colony)
    print(repr(colony))

    print("\n--- 2. Звіт про стан колонії ---")
    print(colony.status_report())

    print("\n--- 3. Поліморфізм: кожна споруда по-своєму виробляє ресурси ---")
    for habitat in colony:
        print(f"{habitat.name}: {habitat.produce()}")

    print("\n--- 4. Пошук за назвою («ферма») ---")
    for habitat in colony.find_by_name("ферма"):
        print(" ", habitat)

    print("\n--- 5. Фільтрація: лише житлові куполи ---")
    for habitat in colony.filter_by_type(ResidentialDome):
        print(" ", habitat)

    print("\n--- 6. Фільтрація за глибиною 0–200 м ---")
    for habitat in colony.filter_by_depth(0, 200):
        print(" ", repr(habitat))

    print("\n--- 7. Сортування за споживанням енергії (за спаданням) ---")
    for habitat in colony.sort_habitats("energy", reverse=True):
        print(f"  {habitat.name}: {habitat.energy_usage():.1f}")

    print("\n--- 8. Шторм інтенсивністю 30 ---")
    colony.apply_storm(30)
    for habitat in colony.filter_damaged():
        print(" ", habitat)

    print("\n--- 9. Сильний шторм і втрата працездатності ---")
    colony.apply_storm(60)
    for habitat in colony:
        status = "працює" if habitat.is_operational else "НЕ ПРАЦЮЄ"
        print(f"  {habitat.name}: {status}")
    print("Баланс ресурсів:", colony.resource_balance())

    print("\n--- 10. Ремонт і новий звіт ---")
    colony.repair_all(100)
    print(colony.status_report())

    print("\n--- 11. Обробка помилок ---")
    try:
        colony.get_habitat("Альфа").add_resident(100)
    except ValueError as error:
        print("Помилка:", error)


if __name__ == "__main__":
    main()