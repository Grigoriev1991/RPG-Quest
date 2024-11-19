import sys
from game.controller import GameController


def run_game():
    """Запускает игру."""
    print("Добро пожаловать в текстовую RPG!")
    print("Вы отправляетесь в опасное подземелье. Будьте осторожны.\n")
    game = GameController()
    game.start_game()


def run_tests():
    """Запускает тесты."""
    import pytest
    pytest.main(["-v"])


if __name__ == "__main__":
    # Устанавливаем режим по умолчанию на "game"
    mode = "game" if len(sys.argv) == 1 else sys.argv[1]
    if mode == "game":
        run_game()
    elif mode == "test":
        run_tests()
    else:
        print("Неизвестный аргумент. Используйте 'game' или 'test'.")
