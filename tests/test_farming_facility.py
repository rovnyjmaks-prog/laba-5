"""Тести класу FarmingFacility."""
import unittest

from src.farming_facility import FarmingFacility


class TestFarmingFacility(unittest.TestCase):
    def test_produces_food_and_oxygen(self):
        farm = FarmingFacility("Ферма", 50, 10, plots=2)
        balance = farm.produce()
        self.assertEqual(balance["food"], 16.0)
        self.assertEqual(balance["oxygen"], 6.0)

    def test_add_plot(self):
        farm = FarmingFacility("Ферма", 50, 3, plots=1)
        farm.add_plot(2)
        self.assertEqual(farm.plots, 3)

    def test_plots_limit(self):
        farm = FarmingFacility("Ферма", 50, 2, plots=2)
        with self.assertRaises(ValueError):
            farm.add_plot()

    def test_invalid_initial_plots(self):
        with self.assertRaises(ValueError):
            FarmingFacility("Ферма", 50, 2, plots=5)

    def test_damage_reduces_output(self):
        farm = FarmingFacility("Ферма", 50, 10, plots=2)
        full = farm.produce()["food"]
        farm.damage(50)
        self.assertLess(farm.produce()["food"], full)

    def test_no_population(self):
        self.assertEqual(FarmingFacility("Ферма", 50, 10).population, 0)

    def test_str_and_repr(self):
        farm = FarmingFacility("Ферма", 50, 10, plots=2, crop="ламінарія")
        self.assertIn("ламінарія", str(farm))
        self.assertIn("FarmingFacility(", repr(farm))


if __name__ == "__main__":
    unittest.main()