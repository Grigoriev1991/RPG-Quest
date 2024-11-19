import time

from game.entities_dataclasses import Player, Enemy

# Пауза между атаками в секундах
ATTACK_DELAY: int = 1

# Цвета
GREEN = "\033[32m"
PURPLE = "\033[35m"
RESET_COLOR = "\033[0m"


class AutoBattle:
    """Класс для проведения автобоя между игроком и врагом."""

    @staticmethod
    def draw_health_bar(
        entity_name: str, current_health: int,
        max_health: int, color: str = ""
    ) -> None:
        """Отрисовывает текстовую шкалу здоровья длиной, равной max_health."""
        current_health = max(0, current_health)  # Гарантируем, что hp > 0
        bar_length = max_health  # Длина шкалы равна максимальному здоровью
        health_ratio = current_health / max_health  # Доля здоровья
        filled_length = int(bar_length * health_ratio)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        bar = f"{color}{bar}{RESET_COLOR}"

        print(f"{entity_name}: [{bar}] {current_health}/{max_health} HP")

    @staticmethod
    def display_health(player: Player, enemy: Enemy) -> None:
        """Отображает шкалы здоровья игрока и врага."""
        AutoBattle.draw_health_bar(
            player.name, player.health, player.max_health, color=GREEN)
        AutoBattle.draw_health_bar(
            enemy.name, enemy.health, enemy.max_health, color=PURPLE)
        print()

    @staticmethod
    def execute_attack(
        attacker: Player | Enemy, defender: Player | Enemy
    ) -> None:
        """
        Проводит атаку одного персонажа на другого и отображает результаты.
        """
        damage = attacker.attack(defender)
        if damage > 0:
            defender.take_damage(damage)
            print(f"{attacker.name} наносит {damage} "
                  f"ед. урона {defender.name}.")
        else:
            print(f"{attacker.name} промахивается по {defender.name}.")

    @staticmethod
    def fight(player: Player, enemy: Enemy, delay: int = ATTACK_DELAY) -> None:
        """Проводит бой между игроком и врагом."""
        print(f"\nВы вступили в бой с врагом: {enemy.name}")

        while player.is_alive() and enemy.is_alive():
            # Игрок атакует врага
            AutoBattle.execute_attack(player, enemy)
            AutoBattle.display_health(player, enemy)

            if not enemy.is_alive():
                print(f"Враг {enemy.name} побежден!")
                return

            time.sleep(delay)

            # Враг атакует игрока
            AutoBattle.execute_attack(enemy, player)
            AutoBattle.display_health(player, enemy)

            if not player.is_alive():
                print(f"Игрок {player.name} погиб. {player.death_description}")
                return

            time.sleep(delay)
