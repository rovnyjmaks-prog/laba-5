"""Тести класу ColonyManager."""
import unittest

from src.colony_manager import ColonyManager
from src.farming_facility import FarmingFacility
from src.research_lab import ResearchLab
from src.residential_dome import ResidentialDome


class TestColonyManager(unittest.TestCase):
    def setUp(self):
        self.colony = ColonyManager("Атлантида", energy_supply=200)
        self.dome = ResidentialDome("Альфа", 100, 10, residents=5)
        self.lab = ResearchLab("Нептун-Лаб", 500, 6, scientists=3)
        self.farm = FarmingFacility("Ферма-1", 50, 8, plots=4)
        for h in (self.dome, self.lab, self.farm):
            self.colony.add_habitat(h)

    def test_add_and_len(self):
        self.assertEqual(len(self.colony), 3)

    def test_add_duplicate_raises(self):
        with self.assertRaises(ValueError):
            self.colony.add_habitat(ResidentialDome("альфа", 10, 5))

    def test_add_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.colony.add_habitat("не споруда")

    def test_remove(self):
        removed = self.colony.remove_habitat("Альфа")
        self.assertIs(removed, self.dome)
        self.assertEqual(len(self.colony), 2)
        with self.assertRaises(KeyError):
            self.colony.remove_habitat("Немає")

    def test_get_habitat(self):
        self.assertIs(self.colony.get_habitat("ферма-1"), self.farm)
        self.assertIsNone(self.colony.get_habitat("Немає"))

    def test_find_by_name(self):
        self.assertEqual(self.colony.find_by_name("лаб"), [self.lab])
        self.assertEqual(self.colony.find_by_name("xyz"), [])

    def test_filter_by_type(self):
        self.assertEqual(self.colony.filter_by_type(FarmingFacility), [self.farm])

    def test_filter_by_depth(self):
        result = self.colony.filter_by_depth(0, 200)
        self.assertCountEqual(result, [self.dome, self.farm])

    def test_filter_damaged(self):
        self.dome.damage(10)
        self.assertEqual(self.colony.filter_damaged(), [self.dome])

    def test_sort_by_depth(self):
        result = self.colony.sort_habitats("depth")
        self.assertEqual(result, [self.farm, self.dome, self.lab])
        result = self.colony.sort_habitats("depth", reverse=True)
        self.assertEqual(result[0], self.lab)

    def test_sort_invalid_key(self):
        with self.assertRaises(ValueError):
            self.colony.sort_habitats("колір")

    def test_total_population(self):
        self.assertEqual(self.colony.total_population(), 8)

    def test_resource_balance(self):
        balance = self.colony.resource_balance()
        # їжа: ферма +32, купол -5, лабораторія -3
        self.assertEqual(balance["food"], 24.0)
        self.assertIn("research_points", balance)

    def test_energy_check(self):
        self.assertTrue(self.colony.is_energy_sufficient())
        self.colony.energy_supply = 1
        self.assertFalse(self.colony.is_energy_sufficient())

    def test_storm_damages_shallow_more(self):
        self.colony.apply_storm(20)
        self.assertEqual(self.dome.integrity, 80)   # 100 м < 200 м
        self.assertEqual(self.lab.integrity, 90)    # 500 м >= 200 м

    def test_repair_all(self):
        self.colony.apply_storm(20)
        self.colony.repair_all(50)
        self.assertEqual(self.dome.integrity, 100)

    def test_iteration_and_str(self):
        self.assertEqual(len(list(self.colony)), 3)
        self.assertIn("Атлантида", str(self.colony))
        self.assertIn("ColonyManager(", repr(self.colony))

    def test_invalid_colony(self):
        with self.assertRaises(ValueError):
            ColonyManager("  ")
        with self.assertRaises(ValueError):
            ColonyManager("Тест", energy_supply=-1)


if __name__ == "__main__":
    unittest.main()