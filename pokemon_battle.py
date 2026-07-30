import random
import time

class Pokemon:
    """A basic class to represent a combatant in our turn-based game."""
    def __init__(self, name, hp, moves):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.moves = moves  # Dictionary mapping move names to damage values

    def is_fainted(self):
        return self.hp <= 0


def player_action(player, enemy):
    """Handles the user's turn."""
    print(f"\n--- YOUR TURN ---")
    print(f"[{player.name}: {player.hp}/{player.max_hp} HP]  vs  [{enemy.name}: {enemy.hp}/{enemy.max_hp} HP]")
    print("Choose a move:")
    
    moves_list = list(player.moves.keys())
    for i, move in enumerate(moves_list):
        print(f"  {i + 1}. {move} ({player.moves[move]} DMG)")
    
    choice = input("> ")
    
    # Basic input validation
    try:
        move_name = moves_list[int(choice) - 1]
    except (ValueError, IndexError):
        move_name = moves_list[0]
        print(f"Invalid input! Defaulting to {move_name}.")
    
    damage = player.moves[move_name]
    enemy.hp -= damage
    print(f">> {player.name} used {move_name} and dealt {damage} damage to {enemy.name}!")


def enemy_action(enemy, player):
    """Handles the AI's turn."""
    print(f"\n--- ENEMY TURN ---")
    move_name = random.choice(list(enemy.moves.keys()))
    damage = enemy.moves[move_name]
    player.hp -= damage
    print(f">> {enemy.name} used {move_name} and dealt {damage} damage to {player.name}!")


def battle_coroutine(player, enemy):
    """
    COROUTINE LOGIC:
    This generator function yields control back and forth between the player 
    and the enemy. It demonstrates state suspension (pausing execution) 
    instead of relying on standard subroutines or complex loop variables.
    """
    turn_counter = 0
    
    # The coroutine loops until a win condition is met, yielding the turn owner
    while not player.is_fainted() and not enemy.is_fainted():
        if turn_counter % 2 == 0:
            yield "player"
        else:
            yield "enemy"
            
        turn_counter += 1


def main():
    print("Welcome to the Coroutine Battle Simulator!")
    
    # Initialize objects
    player = Pokemon("Pikachu", 60, {"Thunder Shock": 15, "Iron Tail": 20, "Quick Attack": 10})
    enemy = Pokemon("Charmander", 70, {"Ember": 12, "Scratch": 8, "Dragon Breath": 18})

    print(f"\nA wild {enemy.name} appeared!")
    time.sleep(1)
    
    # Initialize the coroutine
    battle_sequence = battle_coroutine(player, enemy)
    
    # The main event loop driving the coroutine
    for current_turn in battle_sequence:
        if current_turn == "player":
            player_action(player, enemy)
        elif current_turn == "enemy":
            enemy_action(enemy, player)
            
        time.sleep(1.5) # Pause for readability in the console
        
    # Check win/loss state after the coroutine finishes
    print("\n=======================")
    if player.is_fainted():
        print(f"Oh no! {player.name} fainted. You whited out...")
    else:
        print(f"Success! {enemy.name} fainted. You won the battle!")
    print("=======================\n")

if __name__ == '__main__':
    main()
