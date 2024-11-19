from game.entities_dataclasses import Enemy, Player, Weapon


# Тесты для Weapon
def test_weapon_attack_hit_chance_success(weapon: Weapon, enemy: Enemy):
    """Оружие наносит урон при попадании."""
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage > 0, "Оружие должно наносить урон при попадании."
    assert enemy.health == enemy.max_health - damage, (
        "Здоровье врага должно корректно уменьшиться."
    )


def test_weapon_damage_reduction_by_armor(weapon: Weapon, enemy: Enemy):
    """Урон оружия корректно уменьшается защитой."""
    enemy.armor.defense = weapon.damage - 3  # Частичная защита
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == weapon.damage - enemy.armor.defense, (
        "Урон должен уменьшиться на значение защиты."
    )
    assert enemy.health == enemy.max_health - damage, (
        "Здоровье врага должно уменьшиться на нанесенный урон."
    )


def test_weapon_attack_miss(weapon: Weapon, enemy: Enemy):
    """Оружие не наносит урон при промахе."""
    weapon.hit_chance = 0  # Исключаем вероятность попадания
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 0, (
        "Урон не должен наноситься при промахе."
    )
    assert enemy.health == enemy.max_health, (
        "Здоровье врага не должно изменяться."
    )


def test_weapon_negative_damage(weapon: Weapon, enemy: Enemy):
    """Оружие с отрицательным уроном не наносит урона."""
    weapon.damage = -5
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 0, "Отрицательный урон не должен наноситься."
    assert enemy.health == enemy.max_health, (
        "Здоровье врага не должно изменяться."
    )


def test_weapon_damage_exactly_blocked(weapon: Weapon, enemy: Enemy):
    """Урон полностью блокируется броней."""
    weapon.damage = 10
    enemy.armor.defense = weapon.damage  # Броня равна урону
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 0, (
        "Урон должен быть полностью заблокирован."
    )
    assert enemy.health == enemy.max_health, (
        "Здоровье врага не должно изменяться."
    )


def test_weapon_damage_calculation(weapon: Weapon, enemy: Enemy):
    """Урон корректно рассчитывается как разница между атакой и защитой."""
    weapon.damage = 10
    enemy.armor.defense = weapon.damage - 2
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 2, (
        "Урон должен быть равен разнице между атакой и защитой."
    )
    assert enemy.health == enemy.max_health - damage, (
        "Здоровье врага должно уменьшиться на нанесенный урон."
    )


# Тесты для Armor
def test_armor_reduces_damage(weapon: Weapon, enemy: Enemy):
    """Броня уменьшает урон."""
    weapon.damage = 8
    enemy.armor.defense = 5
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 3, "Урон должен уменьшиться на значение защиты."
    assert enemy.health == enemy.max_health - damage, (
        "Здоровье врага должно уменьшиться на нанесенный урон."
    )


def test_armor_no_effect_with_zero_defense(weapon: Weapon, enemy: Enemy):
    """Броня с защитой 0 не влияет на урон."""
    weapon.damage = 5
    enemy.armor.defense = 0
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == weapon.damage, (
        "Урон должен быть равен базовому урону оружия."
    )
    assert enemy.health == enemy.max_health - damage, (
        "Здоровье врага должно уменьшиться на нанесенный урон."
    )


def test_armor_blocks_negative_damage(weapon: Weapon, enemy: Enemy):
    """Броня корректно обрабатывает оружие с отрицательным уроном."""
    weapon.damage = -4
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 0, "Урон не должен наноситься."
    assert enemy.health == enemy.max_health, (
        "Здоровье врага не должно изменяться."
    )


def test_armor_blocks_zero_damage(weapon: Weapon, enemy: Enemy):
    """Броня корректно обрабатывает оружие с уроном 0."""
    weapon.damage = 0
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 0, "Урон не должен наноситься."
    assert enemy.health == enemy.max_health, (
        "Здоровье врага не должно изменяться."
    )


def test_armor_blocks_exact_damage(weapon: Weapon, enemy: Enemy):
    """Броня блокирует урон, равный значению защиты."""
    weapon.damage = 10
    enemy.armor.defense = 10
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 0, (
        "Урон должен быть полностью заблокирован."
    )
    assert enemy.health == enemy.max_health, (
        "Здоровье врага не должно изменяться."
    )


def test_armor_blocks_partial_damage(weapon: Weapon, enemy: Enemy):
    """Броня блокирует часть урона."""
    weapon.damage = 15
    enemy.armor.defense = 10
    damage = weapon.attack(enemy)
    enemy.take_damage(damage)
    assert damage == 5, (
        "Урон должен быть частично заблокирован."
    )
    assert enemy.health == enemy.max_health - damage, (
        "Здоровье врага должно уменьшиться на нанесенный урон."
    )


# Тесты для Character
def test_character_health_reduces_on_damage(player: Player):
    """Здоровье персонажа уменьшается при получении урона."""
    player.take_damage(5)
    assert player.health == player.max_health - 5, (
        "Здоровье должно уменьшиться на 5."
    )


def test_character_stays_alive_with_partial_damage(player: Player):
    """Персонаж остается жив, если урон меньше текущего здоровья."""
    player.take_damage(player.health - 1)
    assert player.is_alive(), "Персонаж должен быть жив."


def test_character_health_never_negative(player: Player):
    """Здоровье персонажа не уходит в отрицательное значение."""
    player.take_damage(player.max_health + 10)
    assert player.health == 0, "Здоровье не должно быть отрицательным."


def test_character_is_dead_on_zero_health(player: Player):
    """Персонаж считается мертвым при 0 здоровье."""
    player.take_damage(player.max_health)
    assert not player.is_alive(), "Персонаж должен быть мертв при 0 здоровье."


def test_character_health_at_max_on_creation(player: Player):
    """Здоровье персонажа на максимуме при создании."""
    assert player.health == player.max_health, (
        "Здоровье должно быть максимальным."
    )


def test_character_health_one_after_damage(player: Player):
    """Здоровье персонажа равно 1, если он получил урон max_health - 1."""
    player.take_damage(player.max_health - 1)
    assert player.health == 1, "Здоровье должно быть равно 1."
