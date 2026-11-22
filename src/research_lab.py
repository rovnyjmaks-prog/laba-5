"""Дослідницька лабораторія."""
from src.habitat import Habitat


class ResearchLab(Habitat):
    """Лабораторія: науковці виробляють очки досліджень, але споживають ресурси."""

    POINTS_PER_SCIENTIST = 5.0

    def __init__(self, name: str, depth: int, capacity: int,
                 scientists: int = 0, specialization: str = "океанографія") -> None:
        super().__init__(name, depth, capacity)
        if scientists < 0 or scientists > capacity:
            raise ValueError("Кількість науковців має бути від 0 до місткості")
        self._scientists = scientists
        self._specialization = specialization

    @property
    def specialization(self) -> str:
        return self._specialization

    @property
    def population(self) -> int:
        return self._scientists

    def hire_scientist(self, count: int = 1) -> None:
        if count <= 0:
            raise ValueError("Кількість має бути додатною")
        if self._scientists + count > self._capacity:
            raise ValueError("Недостатньо місця в лабораторії")
        self._scientists += count

    def habitat_type(self) -> str:
        return "Дослідницька лабораторія"

    def energy_usage(self) -> float:
        return (25 + 3 * self._scientists) * self._depth_factor()

    def produce(self) -> dict:
        return {
            "research_points": self.POINTS_PER_SCIENTIST * self._scientists * self.efficiency,
            "oxygen": -2.0 * self._scientists,
            "food": -1.0 * self._scientists,
        }

    def __str__(self) -> str:
        return (
            f"{super().__str__()} | науковці: {self._scientists}/{self._capacity} "
            f"| напрям: {self._specialization}"
        )

    def __repr__(self) -> str:
        return (
            f"ResearchLab(name={self._name!r}, depth={self._depth}, "
            f"capacity={self._capacity}, scientists={self._scientists}, "
            f"specialization={self._specialization!r})"
        )