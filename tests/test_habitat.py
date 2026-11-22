"""Тести базового класу Habitat."""
import unittest

from src.habitat import Habitat
from src.research_lab import ResearchLab
from src.residential_dome import ResidentialDome


class TestHabitat(unittest.TestCase):
    def test_abstract_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Habitat("Тест", 100, 10)

    def test_validation(self):
        with self.assertRaises(ValueError):
            ResidentialDome("", 100, 10)
        with self.assertRaises(ValueError):
            ResidentialDome("Купол", -5, 10)
        with self.assertRaises(ValueError):
            ResidentialDome("Купол", 100, 0)

    def test_name_is_stripped(self):
        self.assertEqual(ResidentialDome("  Альфа  ", 100, 10).name, "Альфа")

    def test_damage_and_repair(self):
        dome = ResidentialDome("Альфа", 100, 10)
        dome.damage(30)
        self.assertEqual(dome.integrity, 70)
        dome.repair(50)
        self.assertEqual(dome.integrity, 100)

    def test_negative_values_raise(self):
        dome = ResidentialDome("Альфа", 100, 10)
        with self.assertRaises(ValueError):
            dome.damage(-1)
        with self.assertRaises(ValueError):
            dome.repair(-1)

    def test_not_operational_when_heavily_damaged(self):
        lab = ResearchLab("Лаб", 200, 5, scientists=2)
        lab.damage(90)
        self.assertFalse(lab.is_operational)
        self.assertEqual(lab.efficiency, 0.0)
        self.assertEqual(lab.produce()["research_points"], 0.0)

    def test_integrity_not_below_zero(self):
        dome = ResidentialDome("Альфа", 100, 10)
        dome.damage(500)
        self.assertEqual(dome.integrity, 0)


if __name__ == "__main__":
    unittest.main()