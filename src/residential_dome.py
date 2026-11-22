"""Житловий купол."""
from src.habitat import Habitat


class ResidentialDome(Habitat):
    """Житловий купол: у ньому живуть колоністи, які споживають кисень і їжу."""

    OXYGEN_PER_RESIDENT = 2.0
    FOOD_PER_RESIDENT = 1.0

    def __init__(self, name: str, depth: int, capacity: int, residents: int = 0) -> None:
        super().__init__(name, depth, capacity)
        if residents < 0 or residents > capacity:
            raise ValueError("Кількість мешканців має бути від 0 до місткості")
        self._residents = residents

    @property
    def population(self) -> int:
        return self._residents

    def add_resident(self, count: int = 1) -> None:
        if count <= 0:
            raise ValueError("Кількість має бути додатною")
        if self._residents + count > self._capacity:
            raise ValueError("Недостатньо місця в куполі")
        self._residents += count

    def remove_resident(self, count: int = 1) -> None:
        if count <= 0:
            raise ValueError("Кількість має бути додатною")
        if count > self._residents:
            raise ValueError("У куполі немає стільки мешканців")
        self._residents -= count

    def habitat_type(self) -> str:
        return "Житловий купол"

    def energy_usage(self) -> float:
        return (10 + 0.5 * self._residents) * self._depth_factor()

    def produce(self) -> dict:
        # Мешканці лише споживають ресурси
        return {
            "oxygen": -self.OXYGEN_PER_RESIDENT * self._residents,
            "food": -self.FOOD_PER_RESIDENT * self._residents,
        }

    def __str__(self) -> str:
        return f"{super().__str__()} | мешканці: {self._residents}/{self._capacity}"

    def __repr__(self) -> str:
        return (
            f"ResidentialDome(name={self._name!r}, depth={self._depth}, "
            f"capacity={self._capacity}, residents={self._residents})"
        )