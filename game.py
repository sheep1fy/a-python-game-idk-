"""
RPG Game - Main Game Engine
A turn-based RPG with multiple enemies, GUI, and progression system
"""

import pygame
import random
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    COMBAT = 3
    LEVEL_UP = 4
    GAME_OVER = 5
    VICTORY = 6


@dataclass
class Skill:
    name: str
    damage: int
    cost: int  # mana cost
    accuracy: float  # 0-1


class Enemy:
    """Base enemy class with customizable stats"""
    
    def __init__(self, name: str, max_health: int, damage: int, defense: int, 
                 exp_reward: int, loot: dict):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.defense = defense
        self.exp_reward = exp_reward
        self.loot = loot
        self.skills = [
            Skill("Slash", int(damage * 0.8), 0, 0.85),
            Skill("Heavy Hit", int(damage * 1.2), 0, 0.7),
            Skill("Quick Jab", int(damage * 0.6), 0, 0.95),
        ]
    
    def take_damage(self, damage: int) -> int:
        """Take damage and return actual damage taken"""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        self.health = max(0, self.health)
        return actual_damage
    
    def get_action(self):
        """AI chooses a random skill"""
        return random.choice(self.skills)
    
    def is_alive(self) -> bool:
        return self.health > 0


class Player:
    """Player character with leveling system"""
    
    def __init__(self):
        self.name = "Hero"
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.max_health = 100
        self.health = 100
        self.max_mana = 50
        self.mana = 50
        self.attack = 25
        self.defense = 5
        self.gold = 0
        self.potions = 3
        
        # Skills available to player
        self.skills = [
            Skill("Stab", 75, 0, 0.9),
            Skill("Slash", 50, 0, 0.95),
            Skill("Power Strike", 100, 15, 0.75),
            Skill("Defend", 0, 10, 1.0),  # Special skill
        ]
    
    def take_damage(self, damage: int) -> int:
        """Take damage and return actual damage taken"""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        self.health = max(0, self.health)
        return actual_damage
    
    def heal(self, amount: int):
        """Use health potion"""
        if self.potions > 0:
            self.health = min(self.max_health, self.health + amount)
            self.potions -= 1
            return True
        return False
    
    def gain_exp(self, exp: int):
        """Gain experience and level up if needed"""
        self.exp += exp
        while self.exp >= self.exp_to_level:
            self.level_up()
    
    def level_up(self):
        """Level up and increase stats"""
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.2)
        
        # Stat increases
        self.max_health += 20
        self.health = self.max_health
        self.max_mana += 10
        self.mana = self.max_mana
        self.attack += 5
        self.defense += 2
    
    def is_alive(self) -> bool:
        return self.health > 0


class Enemy_Goblin(Enemy):
    """Weak enemy for early game"""
    def __init__(self):
        super().__init__(
            name="Goblin",
            max_health=30,
            damage=12,
            defense=2,
            exp_reward=50,
            loot={"gold": random.randint(10, 20), "potion": 0.3}
        )


class Enemy_Orc(Enemy):
    """Medium enemy"""
    def __init__(self):
        super().__init__(
            name="Orc",
            max_health=60,
            damage=22,
            defense=5,
            exp_reward=100,
            loot={"gold": random.randint(30, 50), "potion": 0.5}
        )


class Enemy_Dragon(Enemy):
    """Boss enemy"""
    def __init__(self):
        super().__init__(
            name="Dragon",
            max_health=150,
            damage=40,
            defense=10,
            exp_reward=500,
            loot={"gold": random.randint(100, 200), "potion": 1.0}
        )


class RPGGame:
    """Main game class"""
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 20, 60)
    GREEN = (34, 139, 34)
    BLUE = (30, 144, 255)
    GOLD = (218, 165, 32)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("RPG Game - Defeat Enemies & Level Up!")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_med = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # Game state
        self.state = GameState.MENU
        self.player = Player()
        self.current_enemy: Optional[Enemy] = None
        self.combat_log: List[str] = []
        self.selected_skill_idx = 0
        self.enemy_classes = [Enemy_Goblin, Enemy_Orc, Enemy_Dragon]
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    if event.key == pygame.K_q:
                        return False
                
                elif self.state == GameState.COMBAT:
                    if event.key == pygame.K_UP:
                        self.selected_skill_idx = max(0, self.selected_skill_idx - 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_skill_idx = min(len(self.player.skills) - 1, 
                                                      self.selected_skill_idx + 1)
                    elif event.key == pygame.K_RETURN:
                        self.player_attack()
                    elif event.key == pygame.K_p:
                        if self.player.potions > 0:
                            self.player.heal(40)
                            self.combat_log.append(f"Used potion! Healed for 40 HP. "
                                                 f"Potions left: {self.player.potions}")
                            self.enemy_attack()
                    elif event.key == pygame.K_f:
                        self.state = GameState.PLAYING
                        self.current_enemy = None
                        self.combat_log.clear()
                        self.selected_skill_idx = 0
                
                elif self.state == GameState.LEVEL_UP:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                
                elif self.state == GameState.GAME_OVER or self.state == GameState.VICTORY:
                    if event.key == pygame.K_SPACE:
                        self.__init__()
        
        return True
    
    def start_game(self):
        """Start a new game"""
        self.state = GameState.PLAYING
        self.player = Player()
        self.combat_log.clear()
    
    def spawn_enemy(self):
        """Spawn a random enemy based on player level"""
        if self.player.level <= 3:
            enemy_class = Enemy_Goblin
        elif self.player.level <= 8:
            if random.random() < 0.3:
                enemy_class = Enemy_Orc
            else:
                enemy_class = Enemy_Goblin
        else:
            if random.random() < 0.2:
                enemy_class = Enemy_Dragon
            else:
                enemy_class = random.choice([Enemy_Goblin, Enemy_Orc])
        
        self.current_enemy = enemy_class()
        self.state = GameState.COMBAT
        self.combat_log = [f"{self.current_enemy.name} appeared!"]
        self.selected_skill_idx = 0
    
    def player_attack(self):
        """Player uses a skill"""
        skill = self.player.skills[self.selected_skill_idx]
        
        # Check mana
        if skill.cost > self.player.mana:
            self.combat_log.append("Not enough mana!")
            return
        
        self.player.mana -= skill.cost
        
        # Calculate hit
        if random.random() > skill.accuracy:
            self.combat_log.append(f"Miss! {skill.name} failed!")
        else:
            # Special case for Defend skill
            if skill.name == "Defend":
                old_defense = self.player.defense
                self.player.defense += 15
                self.combat_log.append(f"Defense stance! Defense increased from {old_defense} to {self.player.defense}")
                self.player.defense = old_defense  # Reset after this turn
            else:
                damage = skill.damage + random.randint(-5, 5)
                actual_damage = self.current_enemy.take_damage(damage)
                self.combat_log.append(f"Hit! {skill.name} dealt {actual_damage} damage!")
        
        # Enemy attacks
        if self.current_enemy.is_alive():
            self.enemy_attack()
        else:
            self.end_combat()
    
    def enemy_attack(self):
        """Enemy attacks player"""
        skill = self.current_enemy.get_action()
        
        if random.random() > skill.accuracy:
            self.combat_log.append(f"{self.current_enemy.name} missed!")
        else:
            damage = skill.damage + random.randint(-5, 5)
            actual_damage = self.player.take_damage(damage)
            self.combat_log.append(f"{self.current_enemy.name} used {skill.name}! "
                                 f"You took {actual_damage} damage!")
        
        if not self.player.is_alive():
            self.state = GameState.GAME_OVER
    
    def end_combat(self):
        """Handle end of combat"""
        self.player.gain_exp(self.current_enemy.exp_reward)
        self.player.gold += self.current_enemy.loot["gold"]
        
        if random.random() < self.current_enemy.loot["potion"]:
            self.player.potions += 1
            self.combat_log.append(f"Found a potion!")
        
        self.combat_log.append(f"Victory! Gained {self.current_enemy.exp_reward} EXP")
        self.combat_log.append(f"Gold: +{self.current_enemy.loot['gold']}")
        
        if self.player.level > 5:  # Boss fight after level 5
            if isinstance(self.current_enemy, Enemy_Dragon):
                self.state = GameState.VICTORY
            else:
                self.state = GameState.PLAYING
        else:
            self.state = GameState.PLAYING
        
        self.current_enemy = None
    
    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(self.DARK_GRAY)
        
        title = self.font_large.render("RPG GAME", True, self.GOLD)
        subtitle = self.font_med.render("Fight Enemies & Level Up", True, self.WHITE)
        space_text = self.font_small.render("Press SPACE to Start", True, self.GREEN)
        q_text = self.font_small.render("Press Q to Quit", True, self.RED)
        
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 100))
        self.screen.blit(subtitle, (self.width // 2 - subtitle.get_width() // 2, 200))
        self.screen.blit(space_text, (self.width // 2 - space_text.get_width() // 2, 350))
        self.screen.blit(q_text, (self.width // 2 - q_text.get_width() // 2, 400))
    
    def draw_playing(self):
        """Draw exploration screen"""
        self.screen.fill(self.DARK_GRAY)
        
        # Player stats
        stats_title = self.font_med.render(f"Level {self.player.level} - {self.player.name}", 
                                          True, self.GOLD)
        hp_text = self.font_small.render(f"HP: {self.player.health}/{self.player.max_health}", 
                                        True, self.GREEN)
        mana_text = self.font_small.render(f"Mana: {self.player.mana}/{self.player.max_mana}", 
                                          True, self.BLUE)
        exp_text = self.font_small.render(f"EXP: {self.player.exp}/{self.player.exp_to_level}", 
                                         True, self.GOLD)
        gold_text = self.font_small.render(f"Gold: {self.player.gold}", True, self.GOLD)
        potions_text = self.font_small.render(f"Potions: {self.player.potions}", True, self.RED)
        
        self.screen.blit(stats_title, (20, 20))
        self.screen.blit(hp_text, (20, 70))
        self.screen.blit(mana_text, (20, 100))
        self.screen.blit(exp_text, (20, 130))
        self.screen.blit(gold_text, (20, 160))
        self.screen.blit(potions_text, (20, 190))
        
        # Instructions
        instructions = [
            "SPACE - Fight an enemy",
            "ESC - Return to menu"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, self.WHITE)
            self.screen.blit(inst_text, (self.width // 2 - inst_text.get_width() // 2, 
                                        self.height // 2 + i * 40))
        
        fight_text = self.font_med.render("Press SPACE to Fight!", True, self.GREEN)
        self.screen.blit(fight_text, (self.width // 2 - fight_text.get_width() // 2, 
                                     self.height - 100))
    
    def draw_combat(self):
        """Draw combat screen"""
        self.screen.fill(self.DARK_GRAY)
        
        # Enemy info
        enemy_name = self.font_med.render(self.current_enemy.name, True, self.RED)
        self.screen.blit(enemy_name, (self.width - 300, 20))
        
        # Enemy health bar
        pygame.draw.rect(self.screen, self.RED, (self.width - 300, 70, 250, 30))
        health_ratio = self.current_enemy.health / self.current_enemy.max_health
        pygame.draw.rect(self.screen, self.GREEN, (self.width - 300, 70, 250 * health_ratio, 30))
        
        enemy_hp_text = self.font_small.render(
            f"HP: {self.current_enemy.health}/{self.current_enemy.max_health}", 
            True, self.WHITE)
        self.screen.blit(enemy_hp_text, (self.width - 290, 75))
        
        # Player info
        player_name = self.font_med.render(f"Level {self.player.level} {self.player.name}", 
                                          True, self.BLUE)
        self.screen.blit(player_name, (20, 20))
        
        # Player health bar
        pygame.draw.rect(self.screen, self.RED, (20, 70, 250, 30))
        health_ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.screen, self.GREEN, (20, 70, 250 * health_ratio, 30))
        
        player_hp_text = self.font_small.render(
            f"HP: {self.player.health}/{self.player.max_health}", 
            True, self.WHITE)
        self.screen.blit(player_hp_text, (30, 75))
        
        # Mana bar
        pygame.draw.rect(self.screen, (50, 50, 100), (20, 110, 250, 20))
        mana_ratio = self.player.mana / self.player.max_mana
        pygame.draw.rect(self.screen, self.BLUE, (20, 110, 250 * mana_ratio, 20))
        
        # Skills menu
        skills_title = self.font_med.render("Skills (↑/↓ to select, ENTER to use):", 
                                           True, self.WHITE)
        self.screen.blit(skills_title, (20, 200))
        
        for i, skill in enumerate(self.player.skills):
            color = self.GOLD if i == self.selected_skill_idx else self.WHITE
            skill_text = self.font_small.render(
                f"[{i+1}] {skill.name} - DMG: {skill.damage} | Cost: {skill.cost} Mana | "
                f"Acc: {int(skill.accuracy*100)}%", 
                True, color)
            self.screen.blit(skill_text, (40, 240 + i * 30))
        
        # Potions info
        potion_text = self.font_small.render(f"P - Use Potion ({self.player.potions} left)", 
                                            True, self.GREEN)
        self.screen.blit(potion_text, (20, 380))
        
        # Combat log
        log_title = self.font_med.render("Combat Log:", True, self.WHITE)
        self.screen.blit(log_title, (20, 430))
        
        for i, log_entry in enumerate(self.combat_log[-4:]):
            log_text = self.font_tiny.render(log_entry, True, self.WHITE)
            self.screen.blit(log_text, (30, 470 + i * 25))
        
        # Flee info
        flee_text = self.font_small.render("F - Flee from combat", True, self.RED)
        self.screen.blit(flee_text, (20, self.height - 40))
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(self.DARK_GRAY)
        
        game_over_text = self.font_large.render("GAME OVER", True, self.RED)
        stats_text = self.font_med.render(
            f"Level: {self.player.level} | Gold: {self.player.gold} | EXP: {self.player.exp}", 
            True, self.WHITE)
        restart_text = self.font_small.render("Press SPACE to restart", True, self.GREEN)
        
        self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, 150))
        self.screen.blit(stats_text, (self.width // 2 - stats_text.get_width() // 2, 300))
        self.screen.blit(restart_text, (self.width // 2 - restart_text.get_width() // 2, 400))
    
    def draw_victory(self):
        """Draw victory screen"""
        self.screen.fill(self.DARK_GRAY)
        
        victory_text = self.font_large.render("VICTORY!", True, self.GOLD)
        dragon_text = self.font_med.render("You defeated the Dragon!", True, self.RED)
        stats_text = self.font_med.render(
            f"Final Level: {self.player.level} | Gold: {self.player.gold}", 
            True, self.WHITE)
        restart_text = self.font_small.render("Press SPACE to play again", True, self.GREEN)
        
        self.screen.blit(victory_text, (self.width // 2 - victory_text.get_width() // 2, 100))
        self.screen.blit(dragon_text, (self.width // 2 - dragon_text.get_width() // 2, 200))
        self.screen.blit(stats_text, (self.width // 2 - stats_text.get_width() // 2, 300))
        self.screen.blit(restart_text, (self.width // 2 - restart_text.get_width() // 2, 450))
    
    def draw(self):
        """Draw current game state"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_playing()
        elif self.state == GameState.COMBAT:
            self.draw_combat()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.VICTORY:
            self.draw_victory()
        
        pygame.display.flip()
    
    def update(self):
        """Update game logic"""
        if self.state == GameState.PLAYING:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.spawn_enemy()
    
    def run(self):
        """Main game loop"""
        running = True
        space_pressed = False
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = RPGGame()
    game.run()
