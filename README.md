**Video Walkthrough:** [Click here to watch the video](https://youtu.be/iXhgubcr5C4)

# Coroutine-Based Turn Battle System

**Course:** CS3003-001 - Programming Languages
**Project Type:** Solo Project
**Name:** Sterling Hofmann

## Project Overview
This project is a text-based, turn-based battle simulator (similar to a Pokémon battle) implemented in Python. It demonstrates the use of **coroutines and generator functions** to manage game state and control flow, alongside basic Object-Oriented principles for data encapsulation.

## How to Run
Ensure you have Python installed on your machine. Open a terminal, navigate to the directory containing the project, and run:
`python pokemon_battle.py`

## Programming Language Concepts Applied

### 1. Coroutines vs. Standard Subroutines
In standard imperative programming, subroutines (functions) execute from top to bottom and then terminate, clearing their local state. To make a turn-based game using only subroutines, we would have to maintain a complex global/loop state to track whose turn it is.

By utilizing Python's `yield` keyword in the `battle_coroutine()` function, this project leverages a **coroutine**. The generator function is able to suspend its execution, yield control back to the main event loop, and resume exactly where it left off on the next iteration. This flattens the control flow and makes the turn-management logic significantly more expressive and declarative.

### 2. Object-Oriented Data Encapsulation
The combatants are instances of the `Pokemon` class, which encapsulates their state (`hp`, `moves`) and their behaviors (`is_fainted()`). This design choice keeps the coroutine logic clean, as the coroutine only needs to evaluate `player.is_fainted()` without caring about the underlying math or implementation details.
