"""Тести класу ResidentialDome."""
import unittest

from src.residential_dome import ResidentialDome


class TestResidentialDome(unittest.TestCase):
    def test_add_and_remove_residents(self):
        dome = ResidentialDome("Альфа", 100, 5)
        dome.add_resident(3)
        self.assertEqual(dome.population, 3)
        dome.remove_resident(2)
        self.assertEqual(dome.population, 1)

    def test_overflow(self):
        dome = ResidentialDome("Альфа", 100, 2, residents=2)
        with self.assertRaises(ValueError):
            dome.add_resident()
        with self.assertRaises(ValueError):
            dome.remove_resident(3)

    def test_invalid_initial_residents(self):
        with self.assertRaises(ValueError):
            ResidentialDome("Альфа", 100, 2, residents=5)

    def test_consumption(self):
        dome = ResidentialDome("Альфа", 100, 10, residents=4)
        balance = dome.produce()
        self.assertEqual(balance["oxygen"], -8.0)
        self.assertEqual(balance["food"], -4.0)

    def test_energy_grows_with_depth(self):
        shallow = ResidentialDome("А", 100, 10, residents=2)
        deep = ResidentialDome("Б", 900, 10, residents=2)
        self.assertGreater(deep.energy_usage(), shallow.energy_usage())

    def test_habitat_type(self):
        self.assertEqual(ResidentialDome("А", 10, 5).habitat_type(), "Житловий купол")

    def test_str_and_repr(self):
        dome = ResidentialDome("Альфа", 100, 10, residents=3)
        self.assertIn("Альфа", str(dome))
        self.assertIn("3/10", str(dome))
        self.assertIn("ResidentialDome(", repr(dome))


if __name__ == "__main__":
    unittest.main()