from game.entities_dataclasses import Enemy, Weapon, Player


def test_weapon_attack_success(weapon: Weapon, enemy: Enemy):
    """Проверяет успешную атаку оружием."""
    enemy.health = enemy.max_health
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert 0 <= damage <= weapon.damage - enemy.armor.defense, (
        "Урон должен быть в пределах возможного диапазона."
    )
    assert enemy.health == enemy.max_health - damage, (
        "Здоровье врага должно корректно уменьшиться."
    )


def test_weapon_attack_miss(weapon: Weapon, enemy: Enemy):
    """Проверяет промах атаки оружием."""
    weapon.hit_chance = 0  # Исключаем вероятность попадания
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 0, "Урон при промахе должен быть равен 0."
    assert enemy.health == enemy.max_health, (
        "Здоровье врага не должно измениться при промахе."
    )


def test_character_take_damage(player: Player):
    """Проверяет уменьшение здоровья персонажа."""
    player.take_damage(3)
    assert player.health == player.max_health - 3, (
        "Здоровье должно уменьшиться на величину урона."
    )


def test_character_take_excessive_damage(player: Player):
    """Проверяет, что здоровье не уходит в отрицательное значение."""
    player.take_damage(15)
    assert player.health == 0, "Здоровье не должно быть отрицательным."


def test_character_attack(player: Player, enemy: Enemy):
    """Проверяет атаку игрока на врага."""
    damage = player.attack(enemy)
    enemy.take_damage(damage)
    assert 0 <= damage <= player.weapon.damage - enemy.armor.defense, (
        "Урон должен быть в пределах возможного диапазона."
    )
    assert enemy.health == enemy.max_health - damage, (
        "Здоровье врага должно корректно уменьшиться."
    )


def test_enemy_attack(enemy: Enemy, player: Player):
    """Проверяет атаку врага на игрока."""
    damage = enemy.attack(player)
    player.take_damage(damage)
    assert 0 <= damage <= enemy.weapon.damage - player.armor.defense, (
        "Урон должен быть в пределах возможного диапазона."
    )
    assert player.health == player.max_health - damage, (
        "Здоровье игрока должно корректно уменьшиться."
    )


def test_is_alive(player: Player, enemy: Enemy):
    """Проверяет, жив ли персонаж."""
    assert player.is_alive(), "Игрок должен быть жив при создании."
    player.take_damage(player.max_health)
    assert not player.is_alive(), "Игрок не должен быть жив после смерти."

    assert enemy.is_alive(), "Враг должен быть жив при создании."
    enemy.take_damage(enemy.max_health)
    assert not enemy.is_alive(), "Враг не должен быть жив после смерти."


def test_character_defense_effect(player: Player, enemy: Enemy):
    """Проверяет, что броня снижает урон."""
    player.armor.defense = 5  # Полностью блокирует урон врага
    damage = enemy.attack(player)
    player.take_damage(damage)
    assert damage == 0, "Урон должен быть полностью заблокирован броней."
    assert player.health == player.max_health, (
        "Здоровье игрока не должно измениться при заблокированном уроне."
    )


def test_character_no_defense(player: Player, enemy: Enemy) -> None:
    """Проверяет атаку без брони."""
    player.armor.defense = 0  # Броня не блокирует урон
    damage = enemy.attack(player)
    player.take_damage(damage)
    assert damage == enemy.weapon.damage, (
        "Урон должен быть равен базовому урону оружия врага."
    )
    assert player.health == player.max_health - damage, (
        "Здоровье игрока должно корректно уменьшиться."
    )


def test_weapon_damage_calculation(weapon: Weapon, enemy: Enemy) -> None:
    """Проверяет расчет урона с учетом брони."""
    weapon.damage = 6  # Базовый урон оружия
    weapon.hit_chance = 100  # Гарантированное попадание
    enemy.armor.defense = 4  # Защита врага
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 2, (
        "Урон должен быть равен разнице между атакой и защитой."
    )
    assert enemy.health == enemy.max_health - damage, (
        "Здоровье врага должно корректно уменьшиться."
    )


def test_weapon_damage_when_fully_blocked(weapon: Weapon, enemy: Enemy):
    """Проверяет, что урон равен 0, если защита больше урона."""
    weapon.damage = 3  # Урон оружия меньше защиты врага
    enemy.armor.defense = 5  # Защита врага блокирует весь урон
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 0, "Урон должен быть равен 0, если защита больше урона."
    assert enemy.health == enemy.max_health, (
        "Здоровье врага не должно измениться при полном блоке."
    )


def test_character_health_reduction_on_multiple_attacks(
    player: Player, enemy: Enemy
):
    """Проверяет здоровье игрока после нескольких атак врага."""
    damage1 = enemy.attack(player)
    player.take_damage(damage1)
    damage2 = enemy.attack(player)
    player.take_damage(damage2)
    assert player.health == player.max_health - (damage1 + damage2), (
        "Здоровье игрока должно уменьшиться на сумму всех атак."
    )


def test_character_full_health_on_creation(player: Player):
    """Проверяет, что здоровье персонажа на максимуме при создании."""
    assert player.health == player.max_health, (
        "Здоровье игрока должно быть на максимуме при создании."
    )
