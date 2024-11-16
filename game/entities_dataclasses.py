from __future__ import annotations

import random
from typing import Optional
from dataclasses import dataclass


@dataclass
class Weapon:
    name: str
    damage: int
    hit_chance: int
    description: str

    def attack(self, character: Character) -> int:
        """Рассчитывает нанесенный урон с учетом защиты цели."""
        if random.randint(0, 100) <= self.hit_chance:
            defense = character.armor.defense
            damage = self.damage - defense
            actual_damage = max(damage, 0)
            print(f"{self.name} здорово колечит.")
            return actual_damage
        return 0


@dataclass
class Armor:
    name: str
    defense: int
    description: str


@dataclass
class Character:
    """Базовый класс для игрока и врага."""
    name: str
    health: int
    max_health: int
    description: str
    death_description: str
    weapon: Weapon
    armor: Armor

    def is_alive(self) -> bool:
        """Проверяет, жив ли персонаж."""
        return self.health > 0

    def take_damage(self, damage: int) -> None:
        """Уменьшает здоровье персонажа."""
        if damage > 0:
            self.health = max(0, self.health - damage)
            print(f"{self.name} получает {damage} урона.")
        else:
            print(f"{self.name} сегодня родился в рубашке.")

    def attack(self, target: Character) -> int:
        """Атакует другого персонажа и возвращает нанесенный урон."""
        damage = self.weapon.attack(target)
        return damage


@dataclass
class Enemy(Character):
    """Класс для врага."""
    pass


@dataclass
class Player(Character):
    """Класс для игрока."""
    pass


@dataclass
class Room:
    description: str
    enemy: Optional[Enemy] = None

    def has_enemy(self) -> bool:
        """Проверяет, есть ли враг в комнате."""
        return self.enemy is not None and self.enemy.is_alive()
