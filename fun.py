player_health = 100
player_punched = 1
player_slashed = 1
health_pots = 1
# Don't Edit Below This Line

damage_punch = 50
damage_slash = 75

if health_pots >= 1:
    health_pot_use = input("Health Potion available, do you use it? (y/n) ")
else:
    print("No health potion available")
    health_pot_use = "n"

if health_pot_use == "y" and health_pots <= 0:
    print("No health potion available")
elif health_pot_use == "y" and health_pots >= 1:
    player_health += 50
    health_pots -= 1
    print("You used a health potion, health is now", player_health)
elif health_pot_use == "n" and health_pots >= 0:
    print("You did not use a health potion.")

if player_punched == 1 and player_health > damage_punch:
    print("You got Punched!")
    player_health -= damage_punch
    print("Health is", player_health)
elif player_punched == 0:
    print("You were not punched.")
elif player_punched == 1 and player_health <= damage_punch:
    print("You got Punched!")
    print("You have died.")

if player_slashed == 1 and player_health > damage_slash:
    print("You have been slashed!")
    player_health -= damage_slash
    print("Health is", player_health)
elif player_slashed == 0:
    print("You were not slashed.")
elif player_slashed == 1 and player_health <= damage_slash:
    print("You have been slashed!")
    print("You have died.")
