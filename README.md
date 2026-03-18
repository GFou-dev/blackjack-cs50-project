# 21 / Blackjack

A command-line Blackjack game written in Python. Play against the house in your terminal, with standard Blackjack rules and score tracking.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [How to Play](#how-to-play)
- [Game Rules](#game-rules)
- [Project Structure](#project-structure)
- [Running the Tests](#running-the-tests)

---

## Features

- Standard Blackjack rules with proper Ace scoring (1 or 11)
- Opening deal Blackjack detection
- House plays automatically until it reaches 17 or busts
- Replay loop — keep playing without restarting the program
- Pass your name as a command-line argument or enter it at the prompt

---

## Requirements

- Python 3.14 or higher
- (optional) `pytest` for running tests

---

## Installation

Use git to install the repository on your computer:

```bash
git clone https://github.com/GFou-dev/blackjack-CS50-project
```

No external dependencies are required to play the game. If you want to run the tests, install pytest:

```bash
pip install pytest
```

---

## How to Use

You can run the game without any extra command-line argument, you will be prompted for your name:

```bash
python blackjack_game.py
```

Or add your name directly as a command-line argument:

```bash
python blackjack_game.py Cat
```

---

## How to Play

1. Run the program and press **P** to start or **Q** to quit.
2. You and the dealer are each dealt two cards. The dealer's second card is hidden.
3. On your turn, choose an action:
   - **H** — Hit: draw another card.
   - **S** — Stand: end your turn and let the dealer play.
   - **Q** — Quit: exit the game at any time.
4. The dealer then reveals the hidden card and draws until reacing 17 or higher.
5. The highest score without going over 21 wins.
6. After each round you are asked if you want to play again.

---

## Game Rules

| Rule | Value |
|---|---|
| Goal | Get as close to 21 as possible without going over |
| Bust | Going over 21 loses the round immediately |
| Blackjack | A two-card hand totalling exactly 21 wins instantly |
| Ace | Counts as 11 unless that would cause a bust, in which case it counts as 1 |
| Face cards (J, Q, K) | Worth 10 points each |
| House limit | The house must draw until it reaches at least 17 |
| Push | If both players tie on 21 from the opening deal, the round is a push |

---

## Project Structure

```
blackjack-cs50-project/
├── blackjack_game.py       # Main game
├── test_blackjack_game.py  # Pytest test suite
└── README.md
```

### Key components

**`Table` (class)**
Manages the deck, player and house hands, card formatting, and score calculation. A single `Table` instance is reused across rounds — `deck_reset()` returns all cards to the deck and reshuffles between games.

**`game_loop`**
Simulates a single round: opening deal, Blackjack check, player turn, house turn, and resolution.

**`user_phase`**
Handles the player's hit/stand loop. Returns a result message if the player busts, or `None` to signal the game should continue.

**`house_phase`**
Runs the house turn automatically. The house draws until it reaches `HOUSE_LIMIT` (17) or busts.

**`resolve`**
Compares final scores and returns the outcome message when neither side busted.

---

## Running the Tests

The test suite covers score calculation edge cases, deck integrity, result messages, and name input handling.

```bash
pytest test_blackjack_game.py -v
```


## License

This project is released under the MIT License.

## Authors

This project was developped collaboratively with a classmate.
