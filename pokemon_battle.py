import random
import time

class Pokemon:
    """Base class demonstrating encapsulation of state and behavior."""
    def __init__(self, name, hp, moves, potions=0):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.moves = moves  # Dictionary mapping move_name -> (damage, move_type)
        self.potions = potions

    def is_fainted(self):
        return self.hp <= 0
        
    def heal(self):
        """Encapsulated healing behavior."""
        if self.potions > 0:
            heal_amount = 25
            self.hp = min(self.max_hp, self.hp + heal_amount)
            self.potions -= 1
            print(f">> {self.name} drank a Potion and recovered HP! ({self.potions} left)")
        else:
            print(f">> {self.name} has no potions left! Turn wasted!")

    def take_damage(self, damage, move_type):
        """Polymorphic method to be overridden by subclasses."""
        self.hp -= damage
        return damage


class WaterPokemon(Pokemon):
    """Subclass demonstrating inheritance and polymorphism."""
    def take_damage(self, damage, move_type):
        # Water is weak to Electric
        if move_type == "Electric":
            damage *= 2
            print(">> It's super effective!")
        self.hp -= damage
        return damage


class ElectricPokemon(Pokemon):
    """Subclass demonstrating inheritance and polymorphism."""
    def take_damage(self, damage, move_type):
        self.hp -= damage
        return damage


def player_action(player, enemy):
    """Handles the user's turn."""
    print(f"\n--- YOUR TURN ---")
    print(f"[{player.name}: {player.hp}/{player.max_hp} HP]  vs  [{enemy.name}: {enemy.hp}/{enemy.max_hp} HP]")
    print("Choose an action:")
    print("  1. Attack")
    print(f"  2. Heal ({player.potions} Potions)")
    
    action = input("> ")
    
    if action == "2":
        player.heal()
        return

    # Attack logic
    print("\nChoose a move:")
    moves_list = list(player.moves.keys())
    for i, move in enumerate(moves_list):
        dmg, m_type = player.moves[move]
        print(f"  {i + 1}. {move} ({dmg} DMG, {m_type})")
    
    choice = input("> ")
    
    try:
        move_name = moves_list[int(choice) - 1]
    except (ValueError, IndexError):
        move_name = moves_list[0]
        print(f"Invalid input! Defaulting to {move_name}.")
    
    base_damage, move_type = player.moves[move_name]
    print(f">> {player.name} used {move_name}!")
    
    # Enemy takes damage polymorphically
    actual_damage = enemy.take_damage(base_damage, move_type)
    print(f">> {enemy.name} took {actual_damage} damage!")


def enemy_action(enemy, player):
    """Handles the AI's turn."""
    print(f"\n--- ENEMY TURN ---")
    
    # AI logic: Heal if low health and has potions, else attack
    if enemy.hp < (enemy.max_hp * 0.3) and enemy.potions > 0:
        enemy.heal()
    else:
        move_name = random.choice(list(enemy.moves.keys()))
        base_damage, move_type = enemy.moves[move_name]
        print(f">> {enemy.name} used {move_name}!")
        
        actual_damage = player.take_damage(base_damage, move_type)
        print(f">> {player.name} took {actual_damage} damage!")


def battle_coroutine(player, enemy):
    """
    COROUTINE LOGIC:
    This generator function yields control back and forth between the player 
    and the enemy. It demonstrates state suspension (pausing execution).
    """
    turn_counter = 0
    
    while not player.is_fainted() and not enemy.is_fainted():
        if turn_counter % 2 == 0:
            yield "player"
        else:
            yield "enemy"
            
        turn_counter += 1


def main():
    print("Welcome to the Coroutine & OOP Battle Simulator!")
    
    # Initialize subclasses with types and potions
    player = ElectricPokemon("Pikachu", 70, {
        "Thunder Shock": (15, "Electric"), 
        "Quick Attack": (10, "Normal")
    }, potions=2)
    
    # Changed enemy to Squirtle to demonstrate the Electric weakness
    enemy = WaterPokemon("Squirtle", 80, {
        "Water Gun": (12, "Water"), 
        "Tackle": (8, "Normal")
    }, potions=1)

    print(f"\nA wild {enemy.name} appeared!")
    time.sleep(1)
    
    battle_sequence = battle_coroutine(player, enemy)
    
    for current_turn in battle_sequence:
        if current_turn == "player":
            player_action(player, enemy)
        elif current_turn == "enemy":
            enemy_action(enemy, player)
            
        time.sleep(1.5)
        
    print("\n=======================")
    if player.is_fainted():
        print(f"Oh no! {player.name} fainted. You whited out...")
    else:
        print(f"Success! {enemy.name} fainted. You won the battle!")
    print("=======================\n")

if __name__ == '__main__':
    main()
