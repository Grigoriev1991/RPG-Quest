import json
import random
from pathlib import Path

from game.entities_dataclasses import Room, Enemy, Weapon, Armor, Player

# Переменные для типов комнат
START_ROOM: str = 'St'
EMPTY_ROOM: str = ' '
ENEMY_ROOM: str = 'E'
EXIT_ROOM: str = 'Ex'

# Путь к json файлам
DATA_DIR: Path = Path(__file__).parent.parent / "data"


def load_json(file_name: str) -> dict:
    try:
        with open(DATA_DIR / file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_name} не найден.")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: Некорректный формат JSON в файле {file_name}.")
        return {}


class Dungeon:
    def __init__(self):
        self.__dungeon = ['St', ' ', 'E', 'E', ' ', 'E', 'Ex']
        self.rooms = []
        self.player = None

    def generate_dungeon(self) -> None:
        """Создает подземелье, включая комнаты, игрока и врагов."""
        # Загрузка данных
        room_data = load_json("rooms_data.json")
        enemy_data = load_json("enemies_data.json")
        enemy_items = load_json("enemy_items.json")
        player_data = load_json("player_data.json")
        player_items = load_json("player_items.json")

        # Генерация игрока
        self.player = self._create_player(player_data, player_items)

        # Генерация комнат
        for room_type in self.__dungeon:
            if room_type == EMPTY_ROOM:
                self.rooms.append(self._create_empty_room(room_data))
            elif room_type == ENEMY_ROOM:
                self.rooms.append(self._create_enemy_room(
                    room_data, enemy_data, enemy_items))
            elif room_type == START_ROOM:
                self.rooms.append(Room(description="Стартовая комната"))
            elif room_type == EXIT_ROOM:
                self.rooms.append(Room(description="Выход из подземелья"))

    def _create_player(self, player_data: dict, player_items: dict) -> Player:
        """Создает игрока."""
        name = random.choice(player_data["names"])
        description = random.choice(player_data["descriptions"])
        death_description = random.choice(player_data["death_descriptions"])
        weapon_data = random.choice(player_items["weapons"])
        armor_data = random.choice(player_items["armor"])

        weapon = Weapon(
            name=weapon_data["name"],
            damage=weapon_data["damage"],
            hit_chance=weapon_data["hit_chance"],
            description=weapon_data["description"],
        )
        armor = Armor(
            name=armor_data["name"],
            defense=armor_data["defense"],
            description=armor_data["description"],
        )
        return Player(
            name=name,
            health=player_data["health"],
            max_health=player_data["health"],
            description=description,
            death_description=death_description,
            weapon=weapon,
            armor=armor,
        )

    def _create_empty_room(self, room_data: dict) -> Room:
        """Создает пустую комнату."""
        description = random.choice(room_data["descriptions"])
        return Room(description=description)

    def _create_enemy_room(
            self, room_data: dict,
            enemy_data: dict, enemy_items: dict
    ) -> Room:
        """Создает комнату с врагом."""
        room_description = random.choice(room_data["descriptions"])
        enemy_type = random.choice(list(enemy_data.keys()))
        enemy_info = enemy_data[enemy_type]

        # Генерация оружия и брони для врага
        weapon_data = random.choice(enemy_items["weapons"])
        armor_data = random.choice(enemy_items["armor"])

        weapon = Weapon(
            name=weapon_data["name"],
            damage=weapon_data["damage"],
            hit_chance=weapon_data["hit_chance"],
            description=weapon_data["description"],
        )
        armor = Armor(
            name=armor_data["name"],
            defense=armor_data["defense"],
            description=armor_data["description"],
        )
        enemy = Enemy(
            name=enemy_type.capitalize(),
            health=enemy_info["health"],
            max_health=enemy_info["health"],
            description=enemy_info["description"],
            death_description=enemy_info["death_description"],
            weapon=weapon,
            armor=armor,
        )
        return Room(description=room_description, enemy=enemy)

    def get_room(self, index: int) -> Room:
        """Возвращает комнату по индексу."""
        return self.rooms[index]

    def get_dungeon_size(self) -> int:
        """Возвращает размер подземелья."""
        return len(self.rooms)
