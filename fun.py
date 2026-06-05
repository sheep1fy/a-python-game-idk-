#Imports
import random
import time

#Damage & Health Attributes
damage_slash = 75
damage_punch = 50
damage_stab = 90
all_star_super = damage_punch, damage_slash, damage_stab

player_health = 100
enemy_health = 125
health_pots = 1
health_heal = 50

#Player Attack
attack = input(
    f"Enemy Spotted! What is your attack? "
    f"They have {enemy_health} health. "
    f"Choose your attack! ([st]ab/[sl]ash/[pu]nch) "
)
while attack not in ["st", "sl", "pu"]:
    print("Invalid Attack! Please try again.")
    attack = input(
        f"Enemy Spotted! What is your attack? "
        f"They have {enemy_health} health. "
        f"Choose your attack! ([St]ab/[Sl]ash/[Pu]nch) "
    )

if attack == "st":
    enemy_health -= damage_stab
    print("Enemy Stabbed!")
    print(f"You have done {damage_stab} damage and the enemy has {enemy_health} health left.")

elif attack == "sl":
    enemy_health -= damage_slash
    print("Enemy Slashed!")
    print(f"You have done {damage_slash} damage and the enemy has {enemy_health} health left.")

elif attack == "pu":
    enemy_health -= damage_punch
    print("Enemy Punched!")
    print(f"You have done {damage_punch} damage and the enemy has {enemy_health} health left.")

while player_health > 0 and enemy_health > 0:
#Enemy Attacks
  if enemy_health > 0:
    print("Enemy is choosing an attack...")
    time.sleep(5)

    enemy_attack = random.choice(["st", "sl", "pu"])

    if enemy_attack == "st":
        player_health -= damage_stab
        print("The enemy stabbed you!")

    elif enemy_attack == "sl":
        player_health -= damage_slash
        print("The enemy slashed you!")

    elif enemy_attack == "pu":
        player_health -= damage_punch
        print("The enemy punched you!")

    player_health = max(player_health, 0)

    print(f"You have {player_health} health left.")

# Check if player died
  if player_health <= 0:
    print("You have been defeated!")

  else:
    heal = "n"
    star = "n"

    # Potion
    if health_pots > 0:
        heal = input(
            f"Would you like to use your health potion? (y/n) "
        ).lower()

    if heal == "y":
        player_health += health_heal
        player_health = min(player_health, 100)
        health_pots -= 1

        print(
            f"You have been healed! "
            f"Now at {player_health} health."
        )

    elif heal == "n":
        star = input(
            "All Star Super is available! "
            "Would you like to use it? (y/n) "
        ).lower()

    if star == "y":
        enemy_health -= sum(all_star_super)
        enemy_health = max(enemy_health, 0)

        print(
            f"Enemy has been hit with "
            f"{sum(all_star_super)} damage!"
        )

    if enemy_health > 0 and (star == "n" or heal == "y"):

        attack = input(
            f"What is your attack? "
            f"They have {enemy_health} health. "
            f"Choose your attack! "
            f"([st]ab/[sl]ash/[pu]nch) "
        ).lower()

        while attack not in ["st", "sl", "pu"]:
            print("Invalid Attack! Please try again.")
            attack = input(
                f"What is your attack? "
                f"They have {enemy_health} health. "
                f"Choose your attack! "
                f"([st]ab/[sl]ash/[pu]nch) "
            ).lower()

        if attack == "st":
            enemy_health -= damage_stab
            print("Enemy Stabbed!")

        elif attack == "sl":
            enemy_health -= damage_slash
            print("Enemy Slashed!")

        elif attack == "pu":
            enemy_health -= damage_punch
            print("Enemy Punched!")

        enemy_health = max(enemy_health, 0)

        print(f"Enemy has {enemy_health} health left.")

# Win condition
  if enemy_health <= 0:
    print("Enemy Has Been Defeated!")

