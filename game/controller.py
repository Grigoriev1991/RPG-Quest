from game.dungeon import Dungeon
from game.entities_dataclasses import Room, Enemy
from game.autobattle import AutoBattle


class GameController:
    def __init__(self):
        self.dungeon = Dungeon()
        self.dungeon.generate_dungeon()
        self.player = self.dungeon.player
        self.current_position = 0
        self.is_game_over = False

    def start_game(self) -> None:
        """Запускает игровой цикл."""
        print(f"Вы — {self.player.name}. {self.player.description}")

        while not self.is_game_over:
            self.describe_current_room()
            self.prompt_action()

    def describe_current_room(self) -> None:
        """Выводит описание текущей комнаты."""
        current_room = self.dungeon.get_room(self.current_position)
        print(f"\nПеред вами {current_room.description}")
        if current_room.has_enemy():
            enemy = current_room.enemy
            print(f"Здесь есть враг: {enemy.name}")
            print(f"  Описание: {enemy.description}")
            print(f"  Здоровье: {enemy.health}")

    def prompt_action(self) -> None:
        """Предлагает игроку действия и обрабатывает выбор."""
        current_room = self.dungeon.get_room(self.current_position)
        actions = self.get_available_actions(current_room)

        print("\nВаши действия:")
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")

        choice = self.get_player_choice(len(actions))
        self.execute_action(actions[choice - 1], current_room)

    def get_available_actions(self, room: Room) -> list[str]:
        """Возвращает доступные действия для текущей комнаты."""
        actions = []
        if room.has_enemy():
            actions.append("Атаковать")
        if (
            self.current_position < self.dungeon.get_dungeon_size() - 1
            and not room.has_enemy()
        ):
            actions.append("Пойти дальше")
        if self.current_position > 0:
            actions.append("Вернуться назад")
        if (
            self.current_position == self.dungeon.get_dungeon_size() - 1
            and not room.has_enemy()
        ):
            actions.append("Выйти из подземелья")
        return actions

    def get_player_choice(self, max_choice: int) -> int:
        """Получает выбор игрока."""
        while True:
            try:
                choice = int(input("Введите номер действия: "))
                if 1 <= choice <= max_choice:
                    return choice
                print("Неверный ввод. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите число.")

    def execute_action(self, action: str, room: Room) -> None:
        """Выполняет выбранное действие."""
        if action == "Пойти дальше":
            self.move_to_room(self.current_position + 1)
        elif action == "Вернуться назад":
            self.move_to_room(self.current_position - 1)
        elif action == "Атаковать":
            self.auto_fight(room.enemy)  # Используем автобой
        elif action == "Выйти из подземелья":
            self.exit_dungeon()

    def move_to_room(self, new_position: int) -> None:
        """Перемещает игрока в новую комнату."""
        self.current_position = new_position
        print("\nВы переместились в другую комнату.")

    def auto_fight(self, enemy: Enemy) -> None:
        """Запускает автобой с врагом."""
        AutoBattle.fight(self.player, enemy)
        if not self.player.is_alive():
            self.is_game_over = True

    def exit_dungeon(self) -> None:
        """Выход из подземелья, завершение игры."""
        print("Поздравляем! Вы успешно покинули подземелье!")
        self.is_game_over = True