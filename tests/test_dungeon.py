from game.dungeon import Dungeon
from game.entities_dataclasses import Player, Room, Enemy


def test_generate_dungeon_structure(dungeon: Dungeon):
    """Проверяет структуру сгенерированного подземелья."""
    assert len(dungeon.rooms) == 4, (
        "Количество комнат в подземелье должно быть 4."
    )
    assert dungeon.rooms[0].description == "Стартовая комната", (
        "Описание первой комнаты должно быть 'Стартовая комната'."
    )
    assert dungeon.rooms[-1].description == "Выход из подземелья", (
        "Описание последней комнаты должно быть 'Выход из подземелья'."
    )
    assert any(
        isinstance(room.enemy, Enemy) for room in dungeon.rooms if room.enemy
    ), "В подземелье должна быть хотя бы одна комната с врагом."


def test_player_creation(dungeon: Dungeon, player: Player):
    """Проверяет создание игрока."""
    assert isinstance(dungeon.player, Player), (
        "Игрок должен быть объектом Player."
    )
    assert dungeon.player.name == player.name, (
        "Имя игрока в подземелье должно совпадать с именем фикстуры."
    )
    assert dungeon.player.health == player.health, (
        "Здоровье игрока в подземелье должно совпадать с фикстурой."
    )
    assert dungeon.player.weapon.name == player.weapon.name, (
        "Оружие игрока должно совпадать с фикстурой."
    )
    assert dungeon.player.armor.name == player.armor.name, (
        "Броня игрока должна совпадать с фикстурой."
    )


def test_room_descriptions(dungeon: Dungeon):
    """Проверяет, что все комнаты имеют описания."""
    for room in dungeon.rooms:
        assert isinstance(room, Room), "Комната должна быть объектом Room."
        assert room.description, "Комната должна иметь описание."


def test_empty_rooms(dungeon: Dungeon):
    """Проверяет наличие пустых комнат."""
    empty_rooms = [room for room in dungeon.rooms if not room.enemy]
    assert len(empty_rooms) == 3, (
        "В подземелье должно быть три пустые комнаты (включая старт и выход)."
    )
    for room in empty_rooms:
        assert room.enemy is None, "Пустая комната не должна содержать врага."


def test_enemy_rooms(dungeon: Dungeon, enemy: Enemy):
    """Проверяет наличие комнат с врагами."""
    enemy_rooms = [room for room in dungeon.rooms if room.enemy]
    assert len(enemy_rooms) == 1, (
        "В подземелье должна быть одна комната с врагом."
    )
    for room in enemy_rooms:
        assert isinstance(room.enemy, Enemy), (
            "Враг в комнате должен быть объектом Enemy."
        )
        assert room.enemy.name == enemy.name, (
            "Имя врага в комнате должно совпадать с фикстурой."
        )
        assert room.enemy.health == enemy.health, (
            "Здоровье врага в комнате должно совпадать с фикстурой."
        )


def test_start_and_exit_rooms(dungeon: Dungeon):
    """Проверяет корректность стартовой и выходной комнаты."""
    start_room = dungeon.rooms[0]
    exit_room = dungeon.rooms[-1]

    assert start_room.description == "Стартовая комната", (
        "Описание стартовой комнаты должно быть 'Стартовая комната'."
    )
    assert start_room.enemy is None, (
        "В стартовой комнате не должно быть врага."
    )
    assert exit_room.description == "Выход из подземелья", (
        "Описание выходной комнаты должно быть 'Выход из подземелья'."
    )
    assert exit_room.enemy is None, "В выходной комнате не должно быть врага."


def test_get_room(dungeon: Dungeon):
    """Проверяет метод получения комнаты по индексу."""
    room = dungeon.get_room(0)
    assert isinstance(room, Room), (
        "Метод get_room должен возвращать объект Room."
    )
    assert room.description == "Стартовая комната", (
        "Описание комнаты должно быть 'Стартовая комната'."
    )


def test_get_dungeon_size(dungeon: Dungeon):
    """Проверяет метод получения размера подземелья."""
    size = dungeon.get_dungeon_size()
    assert size == 4, "Размер подземелья должен быть 4."


def test_room_with_enemy_properties(dungeon: Dungeon, enemy: Enemy):
    """Проверяет свойства врага в комнате."""
    enemy_rooms = [room for room in dungeon.rooms if room.enemy]
    assert len(enemy_rooms) == 1, (
        "В подземелье должна быть одна комната с врагом."
    )
    for room in enemy_rooms:
        enemy_in_room = room.enemy
        assert isinstance(enemy_in_room, Enemy), (
            "Враг в комнате должен быть объектом Enemy."
        )
        assert enemy_in_room.name == enemy.name, (
            "Имя врага в комнате должно совпадать с фикстурой."
        )
        assert enemy_in_room.health == enemy.health, (
            "Здоровье врага в комнате должно совпадать с фикстурой."
        )
        assert enemy_in_room.weapon.name == enemy.weapon.name, (
            "Оружие врага в комнате должно совпадать с фикстурой."
        )
        assert enemy_in_room.armor.name == enemy.armor.name, (
            "Броня врага в комнате должна совпадать с фикстурой."
        )


def test_create_player_from_fixture(dungeon: Dungeon, player: Player):
    """Проверяет создание игрока через фикстуру."""
    assert isinstance(dungeon.player, Player), (
        "Игрок должен быть объектом Player."
    )
    assert dungeon.player.name == player.name, (
        "Имя игрока в подземелье должно совпадать с фикстурой."
    )
    assert dungeon.player.health == player.health, (
        "Здоровье игрока в подземелье должно совпадать с фикстурой."
    )
    assert dungeon.player.weapon.name == player.weapon.name, (
        "Оружие игрока должно совпадать с фикстурой."
    )
    assert dungeon.player.armor.name == player.armor.name, (
        "Броня игрока должна совпадать с фикстурой."
    )
