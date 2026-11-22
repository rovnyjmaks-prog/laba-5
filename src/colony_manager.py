"""Клас-менеджер підводної колонії."""
from typing import Iterator, List, Optional, Type

from src.habitat import Habitat


class ColonyManager:
    """Керує колекцією споруд: додавання, пошук, фільтрація, сортування, баланс."""

    # Допустимі ключі сортування
    _SORT_KEYS = {
        "name": lambda h: h.name.lower(),
        "depth": lambda h: h.depth,
        "energy": lambda h: h.energy_usage(),
        "integrity": lambda h: h.integrity,
        "population": lambda h: h.population,
    }

    def __init__(self, name: str, energy_supply: float = 100.0) -> None:
        if not name.strip():
            raise ValueError("Назва колонії не може бути порожньою")
        if energy_supply < 0:
            raise ValueError("Постачання енергії не може бути від'ємним")
        self._name = name.strip()
        self._energy_supply = energy_supply
        self._habitats: dict = {}

    # ---------- властивості ----------
    @property
    def name(self) -> str:
        return self._name

    @property
    def energy_supply(self) -> float:
        return self._energy_supply

    @energy_supply.setter
    def energy_supply(self, value: float) -> None:
        if value < 0:
            raise ValueError("Постачання енергії не може бути від'ємним")
        self._energy_supply = value

    # ---------- керування колекцією ----------
    def add_habitat(self, habitat: Habitat) -> None:
        if not isinstance(habitat, Habitat):
            raise TypeError("Можна додавати лише об'єкти типу Habitat")
        key = habitat.name.lower()
        if key in self._habitats:
            raise ValueError(f"Споруда «{habitat.name}» уже існує")
        self._habitats[key] = habitat

    def remove_habitat(self, name: str) -> Habitat:
        key = name.strip().lower()
        if key not in self._habitats:
            raise KeyError(f"Споруду «{name}» не знайдено")
        return self._habitats.pop(key)

    def get_habitat(self, name: str) -> Optional[Habitat]:
        return self._habitats.get(name.strip().lower())

    # ---------- пошук, фільтрація, сортування ----------
    def find_by_name(self, query: str) -> List[Habitat]:
        """Пошук споруд, у назві яких міститься підрядок."""
        q = query.strip().lower()
        return [h for h in self._habitats.values() if q in h.name.lower()]

    def filter_by_type(self, habitat_class: Type[Habitat]) -> List[Habitat]:
        return [h for h in self._habitats.values() if isinstance(h, habitat_class)]

    def filter_by_depth(self, min_depth: int, max_depth: int) -> List[Habitat]:
        return [h for h in self._habitats.values()
                if min_depth <= h.depth <= max_depth]

    def filter_damaged(self, threshold: float = 100.0) -> List[Habitat]:
        """Споруди з цілісністю нижче за поріг."""
        return [h for h in self._habitats.values() if h.integrity < threshold]

    def sort_habitats(self, key: str = "name", reverse: bool = False) -> List[Habitat]:
        if key not in self._SORT_KEYS:
            raise ValueError(
                f"Невідомий ключ сортування «{key}». "
                f"Доступні: {', '.join(self._SORT_KEYS)}"
            )
        return sorted(self._habitats.values(), key=self._SORT_KEYS[key], reverse=reverse)

    # ---------- розрахунки ----------
    def total_energy_usage(self) -> float:
        return sum(h.energy_usage() for h in self._habitats.values())

    def is_energy_sufficient(self) -> bool:
        return self.total_energy_usage() <= self._energy_supply

    def total_population(self) -> int:
        return sum(h.population for h in self._habitats.values())

    def resource_balance(self) -> dict:
        """Сумарний добовий баланс ресурсів усієї колонії (поліморфізм produce)."""
        balance: dict = {}
        for habitat in self._habitats.values():
            for resource, amount in habitat.produce().items():
                balance[resource] = balance.get(resource, 0.0) + amount
        return balance

    def apply_storm(self, intensity: float) -> None:
        """Шторм: мілководні споруди (до 200 м) страждають вдвічі більше."""
        for habitat in self._habitats.values():
            habitat.damage(intensity if habitat.depth < 200 else intensity / 2)

    def repair_all(self, amount: float) -> None:
        for habitat in self._habitats.values():
            habitat.repair(amount)

    def status_report(self) -> str:
        lines = [f"=== Колонія «{self._name}» ==="]
        lines += [f"  {h}" for h in self._habitats.values()]
        lines.append(f"Населення: {self.total_population()}")
        lines.append(
            f"Енергія: {self.total_energy_usage():.1f} / {self._energy_supply:.1f} "
            f"({'достатньо' if self.is_energy_sufficient() else 'ДЕФІЦИТ'})"
        )
        for resource, amount in self.resource_balance().items():
            lines.append(f"  {resource}: {amount:+.1f}")
        return "\n".join(lines)

    # ---------- магічні методи ----------
    def __len__(self) -> int:
        return len(self._habitats)

    def __iter__(self) -> Iterator[Habitat]:
        return iter(self._habitats.values())

    def __str__(self) -> str:
        return f"Колонія «{self._name}»: споруд — {len(self)}, населення — {self.total_population()}"

    def __repr__(self) -> str:
        return (
            f"ColonyManager(name={self._name!r}, "
            f"energy_supply={self._energy_supply}, habitats={len(self)})"
        )