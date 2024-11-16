import time

from game.entities_dataclasses import Player, Enemy

# Пауза между атаками в секундах
ATTACK_DELAY: int = 3


class AutoBattle:
    """Класс для проведения автобоя между игроком и врагом."""

    @staticmethod
    def draw_health_bar(
        entity_name: str, current_health: int,
        max_health: int, color: str = ""
    ) -> None:
        """
        Отрисовывает текстовую шкалу здоровья длиной, равной max_health.
        """
        current_health = max(0, current_health)  # Гарантируем, что hp > 0
        bar_length = max_health  # Длина шкалы равна максимальному здоровью
        health_ratio = current_health / max_health  # Доля здоровья
        filled_length = int(bar_length * health_ratio)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)

        # Применение цвета к шкале
        color_reset = "\033[0m"
        bar = f"{color}{bar}{color_reset}"

        print(f"{entity_name}: [{bar}] {current_health}/{max_health} HP")

    @staticmethod
    def fight(player: Player, enemy: Enemy) -> str:
        """
        Проводит бой между игроком и врагом.
        Возвращает результат боя как строку.
        """
        print(f"\nВы вступили в бой с врагом: {enemy.name}")

        while player.is_alive() and enemy.is_alive():
            # Игрок атакует врага
            damage_to_enemy = player.attack(enemy)
            enemy.take_damage(damage_to_enemy)

            # Отображение здоровья после атаки игрока
            AutoBattle.draw_health_bar(
                player.name, player.health, player.max_health, color="\033[32m"
            )  # Зеленый цвет для игрока
            AutoBattle.draw_health_bar(
                enemy.name, enemy.health, enemy.max_health, color="\033[35m"
            )  # Фиолетовый цвет для врага
            print()

            if not enemy.is_alive():
                print(f"Враг {enemy.name} побежден!")
                return
            time.sleep(ATTACK_DELAY)

            # Враг атакует игрока
            damage_to_player = enemy.attack(player)
            player.take_damage(damage_to_player)

            # Отображение здоровья после атаки врага
            AutoBattle.draw_health_bar(
                player.name, player.health, player.max_health, color="\033[32m"
            )
            AutoBattle.draw_health_bar(
                enemy.name, enemy.health, enemy.max_health, color="\033[35m"
            )
            print()

            if not player.is_alive():
                print(f"Игрок {player.name} погиб. {player.death_description}")
                return
            time.sleep(ATTACK_DELAY)
