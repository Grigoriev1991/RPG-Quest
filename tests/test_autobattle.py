from game.entities_dataclasses import Player, Enemy
from game.autobattle import AutoBattle


def test_fight_player_wins(player: Player, enemy: Enemy, mock_sleep):
    """Проверяет завершение боя с победой игрока."""
    player.weapon.hit_chance = 100  # Гарантированное попадание
    enemy.weapon.hit_chance = 0  # Гарантированный промах врага
    AutoBattle.fight(player, enemy)

    assert player.is_alive(), (
        "Игрок должен быть жив после победы над врагом."
    )
    assert not enemy.is_alive(), (
        "Враг должен быть мертв после поражения от игрока."
    )


def test_fight_enemy_wins(player: Player, enemy: Enemy, mock_sleep):
    """Проверяет завершение боя с победой врага."""
    enemy.weapon.hit_chance = 100  # Гарантированное попадание
    player.weapon.hit_chance = 0  # Гарантированный промах героя
    AutoBattle.fight(player, enemy)

    assert not player.is_alive(), (
        "Игрок должен быть мертв после поражения от врага."
    )
    assert enemy.is_alive(), (
        "Враг должен быть жив после победы над игроком."
    )
