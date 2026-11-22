"""Тести класу ResearchLab."""
import unittest

from src.research_lab import ResearchLab


class TestResearchLab(unittest.TestCase):
    def test_produces_research_points(self):
        lab = ResearchLab("Лаб", 300, 10, scientists=4)
        self.assertEqual(lab.produce()["research_points"], 20.0)

    def test_consumes_resources(self):
        lab = ResearchLab("Лаб", 300, 10, scientists=4)
        self.assertEqual(lab.produce()["oxygen"], -8.0)
        self.assertEqual(lab.produce()["food"], -4.0)

    def test_hire_scientist(self):
        lab = ResearchLab("Лаб", 300, 3, scientists=2)
        lab.hire_scientist()
        self.assertEqual(lab.population, 3)
        with self.assertRaises(ValueError):
            lab.hire_scientist()

    def test_invalid_initial_scientists(self):
        with self.assertRaises(ValueError):
            ResearchLab("Лаб", 300, 2, scientists=3)

    def test_damage_reduces_research(self):
        lab = ResearchLab("Лаб", 300, 10, scientists=4)
        lab.damage(50)
        self.assertEqual(lab.produce()["research_points"], 10.0)

    def test_repr_contains_specialization(self):
        lab = ResearchLab("Лаб", 300, 3, specialization="біологія")
        self.assertIn("біологія", repr(lab))
        self.assertIn("біологія", str(lab))


if __name__ == "__main__":
    unittest.main()