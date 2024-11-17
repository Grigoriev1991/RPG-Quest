import pytest

from game.entities_dataclasses import Armor, Enemy, Player, Room, Weapon
from game.dungeon import Dungeon
from game.controller import GameController


@pytest.fixture
def weapon() -> Weapon:
    """
    Создает тестовое оружие для игрока или врага.
    """
    return Weapon(
        name="Тестовое оружие",
        damage=5,
        hit_chance=75,
        description="Описание оружия",
    )


@pytest.fixture
def armor() -> Armor:
    """
    Создает тестовую броню для игрока или врага.
    """
    return Armor(
        name="Тестовая броня",
        defense=2,
        description="Описание брони",
    )


@pytest.fixture
def player(armor: Armor) -> Player:
    """
    Создает тестового игрока.
    """
    weapon = Weapon(
        name="Меч игрока",
        damage=5,
        hit_chance=100,
        description="Оружие игрока",
    )
    return Player(
        name="Игрок",
        health=10,
        max_health=10,
        description="Тестовый игрок",
        death_description="Игрок погиб",
        weapon=weapon,
        armor=armor,
    )


@pytest.fixture
def enemy(armor: Armor) -> Enemy:
    """
    Создает тестового врага.
    """
    weapon = Weapon(
        name="Когти врага",
        damage=5,
        hit_chance=100,
        description="Оружие врага",
    )
    return Enemy(
        name="Враг",
        health=10,
        max_health=10,
        description="Тестовый враг",
        death_description="Враг уничтожен",
        weapon=weapon,
        armor=armor,
    )


@pytest.fixture
def room(enemy: Enemy) -> Room:
    """
    Создает тестовую комнату с врагом.
    """
    return Room(
        description="Тестовая комната с врагом",
        enemy=enemy,
    )


@pytest.fixture
def dungeon(player: Player, room: Room) -> Dungeon:
    """
    Создает тестовое подземелье с фиксированными данными.

    Подземелье содержит:
    - Стартовую комнату.
    - Комнату с врагом.
    - Пустую комнату.
    - Комнату-выход.
    """
    dungeon = Dungeon()
    dungeon.rooms = [
        Room(description="Стартовая комната"),
        room,
        Room(description="Пустая комната"),
        Room(description="Выход из подземелья"),
    ]
    dungeon.player = player
    return dungeon


@pytest.fixture
def controller(dungeon: Dungeon) -> GameController:
    """Создает экземпляр контроллера игры."""
    controller = GameController()
    controller.dungeon = dungeon
    controller.player = dungeon.player
    return controller


@pytest.fixture
def mock_sleep(monkeypatch):
    """Мокирует time.sleep для исключения задержек."""
    monkeypatch.setattr("time.sleep", lambda _: None)
