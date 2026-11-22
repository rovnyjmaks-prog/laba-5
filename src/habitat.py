"""Базовий абстрактний клас середовища проживання (Habitat)."""
from abc import ABC, abstractmethod


class Habitat(ABC):
    """Абстрактна підводна споруда колонії."""

    # Мінімальна цілісність, при якій споруда ще працює
    MIN_OPERATIONAL_INTEGRITY = 20.0

    def __init__(self, name: str, depth: int, capacity: int) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Назва споруди не може бути порожньою")
        if depth <= 0:
            raise ValueError("Глибина має бути додатним числом")
        if capacity <= 0:
            raise ValueError("Місткість має бути додатним числом")
        # Інкапсуляція: атрибути приховані, доступ через властивості
        self._name = name.strip()
        self._depth = depth
        self._capacity = capacity
        self._integrity = 100.0  # цілісність корпусу у відсотках

    # ---------- властивості (інкапсуляція) ----------
    @property
    def name(self) -> str:
        return self._name

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def integrity(self) -> float:
        return self._integrity

    @property
    def is_operational(self) -> bool:
        """Чи працює споруда (достатня цілісність корпусу)."""
        return self._integrity >= self.MIN_OPERATIONAL_INTEGRITY

    @property
    def efficiency(self) -> float:
        """Ефективність роботи від 0.0 до 1.0 залежно від цілісності."""
        return self._integrity / 100.0 if self.is_operational else 0.0

    @property
    def population(self) -> int:
        """Кількість мешканців/працівників (за замовчуванням 0)."""
        return 0

    # ---------- спільна поведінка ----------
    def _depth_factor(self) -> float:
        """Чим глибше, тим більші витрати енергії на тиск."""
        return 1 + self._depth / 1000

    def damage(self, amount: float) -> None:
        """Пошкодити корпус споруди."""
        if amount < 0:
            raise ValueError("Пошкодження не може бути від'ємним")
        self._integrity = max(0.0, self._integrity - amount)

    def repair(self, amount: float) -> None:
        """Відремонтувати корпус споруди."""
        if amount < 0:
            raise ValueError("Ремонт не може бути від'ємним")
        self._integrity = min(100.0, self._integrity + amount)

    # ---------- абстрактні методи (поліморфізм) ----------
    @abstractmethod
    def habitat_type(self) -> str:
        """Українська назва типу споруди."""

    @abstractmethod
    def energy_usage(self) -> float:
        """Споживання енергії за добу."""

    @abstractmethod
    def produce(self) -> dict:
        """Добовий баланс ресурсів: додатні значення — виробництво,
        від'ємні — споживання."""

    # ---------- магічні методи ----------
    def __str__(self) -> str:
        return (
            f"{self.habitat_type()} «{self._name}» | глибина: {self._depth} м | "
            f"цілісність: {self._integrity:.0f}% | "
            f"енергія: {self.energy_usage():.1f}"
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(name={self._name!r}, "
            f"depth={self._depth}, capacity={self._capacity})"
        )