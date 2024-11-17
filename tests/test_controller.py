from unittest.mock import patch

from game.controller import GameController
from game.entities_dataclasses import Enemy, Room
from game.dungeon import Dungeon


def test_initialization(controller: GameController, dungeon: Dungeon):
    """Проверяет инициализацию контроллера."""
    assert controller.dungeon == dungeon, "Подземелье не совпадает."
    assert controller.player == dungeon.player, "Игрок не совпадает."
    assert controller.current_position == 0, "Начальная позиция неверна."
    assert not controller.is_game_over, "Игра должна быть не завершена."


def test_move_to_room(controller: GameController):
    """Проверяет перемещение между комнатами."""
    controller.move_to_room(1)
    assert controller.current_position == 1, "Позиция должна быть 1."

    controller.move_to_room(2)
    assert controller.current_position == 2, "Позиция должна быть 2."


def test_execute_action_attack(controller: GameController, enemy: Enemy):
    """Проверяет выполнение действия 'Атаковать'."""
    room = Room(description="Тестовая комната", enemy=enemy)
    with patch("game.autobattle.AutoBattle.fight") as mock_fight:
        controller.execute_action("Атаковать", room)
        mock_fight.assert_called_once_with(
            controller.player, enemy
        ), "Метод 'fight' не был вызван с ожидаемыми аргументами."


def test_execute_action_move_forward(controller: GameController):
    """Проверяет выполнение действия 'Пойти дальше'."""
    initial_position = controller.current_position
    controller.execute_action("Пойти дальше", controller.dungeon.rooms[0])
    assert (
        controller.current_position == initial_position + 1
    ), "Игрок не переместился в следующую комнату."


def test_execute_action_exit(controller: GameController):
    """Проверяет выполнение действия 'Выйти из подземелья'."""
    # Устанавливаем позицию на выход
    controller.current_position = len(controller.dungeon.rooms) - 1
    controller.execute_action(
        "Выйти из подземелья", controller.dungeon.rooms[-1])
    assert controller.is_game_over, "Игра должна быть завершена."


def test_get_available_actions(controller: GameController, enemy: Enemy):
    """Проверяет доступные действия для комнаты."""
    start_room = controller.dungeon.rooms[0]
    enemy_room = Room(description="Тестовая комната", enemy=enemy)

    actions_start = controller.get_available_actions(start_room)
    assert "Пойти дальше" in actions_start, (
        "Действие 'Пойти дальше' должно быть доступно."
    )

    actions_enemy = controller.get_available_actions(enemy_room)
    assert "Атаковать" in actions_enemy, (
        "Действие 'Атаковать' должно быть доступно."
    )
    assert "Пойти дальше" not in actions_enemy, (
        "Действие 'Пойти дальше' не должно быть доступно в комнате с врагом."
    )


def test_auto_fight_end_game(
    controller: GameController, enemy: Enemy, mock_sleep
):
    """Проверяет завершение игры после гибели игрока."""
    controller.player.health = 1  # Устанавливаем низкое здоровье
    enemy.weapon.damage = 10  # Гарантированное убийство
    enemy.weapon.hit_chance = 100  # Гарантированное попадание
    controller.auto_fight(enemy)
    assert controller.is_game_over, (
        "Игра должна быть завершена после гибели игрока."
    )
