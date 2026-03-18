import random
import sys


HOUSE_LIMIT = 17
BUST_THRESHOLD = 21


class Table:
    """Manages the game state including the deck of cards, player and house hands,
    and calculates the scores. Uses tuples to represent cards as (suit, rank) pairs."""

    suits = ["S", "H", "C", "D"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suit_symbol = {"S": "♠", "H": "♥", "C": "♣", "D": "♦"}

    def __init__(self):
        self.deck = [(suit, rank) for suit in self.suits for rank in self.ranks]
        self.p_cards = []
        self.h_cards = []
        random.shuffle(self.deck)

    def deck_reset(self):
        """Return all cards to the deck and shuffle it"""
        self.deck.extend(self.p_cards)
        self.deck.extend(self.h_cards)
        self.p_cards.clear()
        self.h_cards.clear()
        random.shuffle(self.deck)

    def deal_cards(self, count, target):
        """Draw cards from the deck into the specified target hand"""
        for _ in range(count):
            if self.deck:
                target.append(self.deck.pop())

    def format_card(self, card):
        """Convert a (suit, rank) tuple into a string for display"""
        symbol = self.suit_symbol[card[0]]
        return f"{symbol} {card[1]} {symbol}"

    def format_hand(self, cards):
        """Return a formatted string of all cards in a hand"""
        return " | ".join(self.format_card(c) for c in cards)

    def compute_score(self, cards):
        """Calculate the total value of a hand.
        Ace value defaults to 1. If at least 1 ace, and hand score is lower or equal to 11, then add 10.
        """
        total = 0
        aces = 0
        for _, rank in cards:
            if rank in ("J", "Q", "K"):
                total += 10
            elif rank == "A":
                aces += 1
            else:
                total += int(rank)

        total += aces
        if aces > 0 and total + 10 <= BUST_THRESHOLD:
            total += 10
        return total


def main():
    """Calls the welcome screen and handles the game loop"""
    table = Table()
    if not welcome_screen():
        quit_game()
    username = get_playername()
    print(f"\nWelcome, {username}! The game will begin.\n")
    while True:
        result = game_loop(table, username)
        print(result)
        if not ask_replay():
            quit_game()


def game_loop(table, username):
    """The game loop. Calculates if there is initial blackjack, then starts the player and dealer phase,
    checking if end turn conditions have been met"""
    table.deck_reset()
    p_score, h_score = opening_deal(table)

    if p_score == BUST_THRESHOLD or h_score == BUST_THRESHOLD:
        show_state(table, username, show_player=True, show_house=True)
        if p_score == h_score:
            return "\nBoth players hit 21. It's a push!\n"
        winner = username if p_score == BUST_THRESHOLD else "House"
        return f"\n21! Blackjack — {winner} takes the round!\n"

    show_state(table, username, show_player=True, show_house=True, conceal=True)

    player_result = user_phase(table, username)
    if player_result is not None:
        return player_result
    house_result = house_phase(table, username)
    if house_result is not None:
        return house_result
    return resolve(table, username)


def opening_deal(table):
    """Deals the initial cards and calculates the score."""
    table.deal_cards(2, table.p_cards)
    table.deal_cards(2, table.h_cards)
    return table.compute_score(table.p_cards), table.compute_score(table.h_cards)

def user_phase(table, username):
    """Handle the player's turn with hit / stand decision"""
    while True:
        score = table.compute_score(table.p_cards)
        if score == BUST_THRESHOLD:
            print(f"\n21!")
            return None
        if score > BUST_THRESHOLD:
            return f"\nBust — {username} went over 21. House takes the round!\n"
        choice = input("\n(H)it | (S)tand | (Q)uit: ").strip().lower()
        if choice in ("q", "quit"):
            quit_game()
        elif choice in ("s", "stand"):
            return None
        elif choice in ("h", "hit"):
            table.deal_cards(1, table.p_cards)
            print("\nCard drawn...")
            show_state(table, username, show_player=True)


def house_phase(table, username):
    """Run the house turn : draws until reaching the limit"""
    print("\nThe house reveals its second card...")
    show_state(table, username, show_house=True)
    while True:
        score = table.compute_score(table.h_cards)
        if score > BUST_THRESHOLD:
            return result_message(username, busted=True)
        if score < HOUSE_LIMIT:
            print("House draws a card...")
            table.deal_cards(1, table.h_cards)
            show_state(table, username, show_house=True)
        else:
            print("House stands.")
            return None


def resolve(table, username):
    """Compare final scores and return result message"""
    p_score = table.compute_score(table.p_cards)
    h_score = table.compute_score(table.h_cards)
    if p_score > h_score:
        return result_message(username)
    elif h_score > p_score:
        return result_message("House")
    else:
        return "\nIt's a draw.\n"


def show_state(table, username, show_player=False, show_house=False, conceal=False):
    """Print the current hands and scores. Can be modified by named parameters"""
    if show_player:
        score = table.compute_score(table.p_cards)
        print(f"\n{username}'s cards: | {table.format_hand(table.p_cards)} |")
        print(f"{username}'s total: {score}")
    if show_house:
        if conceal:
            first = table.format_card(table.h_cards[0])
            print(f"\nHouse cards: | {first} | ? |")
        else:
            score = table.compute_score(table.h_cards)
            print(f"\nHouse cards: | {table.format_hand(table.h_cards)} |")
            print(f"House total: {score}")


def result_message(winner, busted=False):
    """Returns the victory/defeat message"""
    prefix = "Bust — " if busted else ""
    return f"\n{prefix}{winner} takes the round!\n"


def welcome_screen():
    """Display the title banner and return True if player wants to start"""
    print("\n+-------------------------------------------+")
    print("|   21 / Blackjack  —  P : Play  Q : Quit   |")
    print("+-------------------------------------------+\n")
    while True:
        cmd = input().strip().lower()
        if cmd in ("q", "quit"):
            return False
        if cmd in ("p", "play"):
            return True


def get_playername():
    """Get player name from argv. If no argv is given, prompt the user"""
    name = (sys.argv[1].strip() if len(sys.argv) > 1 else input("Enter your name: ").strip())
    if name == "":
        name = 'Guest'
    return name


def ask_replay():
    """Ask if the player wants to play again"""
    while True:
        ans = input("Play again? (Y)es | (N)o\n").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False


def quit_game():
    """Exit the game"""
    sys.exit("\nSee you next time!\n")


if __name__ == "__main__":
    main()
