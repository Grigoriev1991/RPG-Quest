from game.controller import GameController


def main():
    """Главная функция для запуска игры."""
    print("Добро пожаловать в текстовую RPG!")
    print("Вы отправляетесь в опасное подземелье. Будьте осторожны.")
    print("\n" + "=" * 50)

    # Создаем объект контроллера и запускаем игру
    game = GameController()
    game.start_game()


if __name__ == "__main__":
    main()
