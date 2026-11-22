"""Ферма водоростей."""
from src.habitat import Habitat


class FarmingFacility(Habitat):
    """Підводна ферма: вирощує їжу та виробляє кисень."""

    FOOD_PER_PLOT = 8.0
    OXYGEN_PER_PLOT = 3.0

    def __init__(self, name: str, depth: int, capacity: int,
                 plots: int = 1, crop: str = "водорості") -> None:
        super().__init__(name, depth, capacity)
        if plots < 0 or plots > capacity:
            raise ValueError("Кількість грядок має бути від 0 до місткості")
        self._plots = plots
        self._crop = crop

    @property
    def plots(self) -> int:
        return self._plots

    @property
    def crop(self) -> str:
        return self._crop

    def add_plot(self, count: int = 1) -> None:
        if count <= 0:
            raise ValueError("Кількість має бути додатною")
        if self._plots + count > self._capacity:
            raise ValueError("Немає місця для нових грядок")
        self._plots += count

    def habitat_type(self) -> str:
        return "Ферма"

    def energy_usage(self) -> float:
        return (15 + 4 * self._plots) * self._depth_factor()

    def produce(self) -> dict:
        return {
            "food": self.FOOD_PER_PLOT * self._plots * self.efficiency,
            "oxygen": self.OXYGEN_PER_PLOT * self._plots * self.efficiency,
        }

    def __str__(self) -> str:
        return (
            f"{super().__str__()} | грядки: {self._plots}/{self._capacity} "
            f"| культура: {self._crop}"
        )

    def __repr__(self) -> str:
        return (
            f"FarmingFacility(name={self._name!r}, depth={self._depth}, "
            f"capacity={self._capacity}, plots={self._plots}, crop={self._crop!r})"
        )