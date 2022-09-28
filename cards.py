from __future__ import annotations  # for type hints of a class in itself
from enum import Enum


class Rank(Enum):
    """
    DESCRIPTION:
        Ranks available in a set of playing cards.

    VALUES:
        The values are in the following ascending order.
        (Note that Two is the lowest rank and Ace is the highest rank.)
        Two, Three, ..., Ten, Jak, Queen, King, Ace

    OPERATIONS AVAILABLE:
        You can use the less then operator (>) to compare between ranks
    """

    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    def __lt__(self, other: Rank) -> bool:
        """
        Override the '<' operator.
        Compare two ranks value, return result as bool
        """
        return other.value > self.value


class Suit(Enum):
    """
    DESCRIPTION:
        Suits available in a set of playing cards.

    VALUES:
        The values are in the following ascending order.
        Clubs, Diamonds, Spades, Hearts

    OPERATIONS AVAILABLE:
        You can use the less then operator (>) to compare between suits
    """

    Clubs = 0
    Diamonds = 1
    Spades = 2
    Hearts = 3

    def __lt__(self, other: Suit) -> bool:
        """
        Override the '<' operator.
        Compare two suits value, return result as bool
        """
        return other.value > self.value


class Card:
    """
    DESCRIPTION:
        A card that can be found in a regular set of playing card.
        Only capable of general cards (rank and number),
        and incapable of special cards (Joker cards).

    ATTRIBUTES:
        rank: the rank of the card representing
        suit: the suit of the card representing
        settings: STATIC, a dictionary for card settings across all cards.
          - pretty_print: bool, pretty text art when copnverting to str.

    OPERATIONS AVAILABLE:
        The less than order comparison operator (>) to compare between cards.
        The equality comparison operator (==) to compare between cards.
        The repr or str conversion to convert into readable format.
    """

    # static variable for settings
    settings: bool = {
        "pretty_print": False
    }
    rank: Rank
    suit: Suit

    def __init__(self, rank: Rank, suit: Suit) -> None:
        """
        Initialise the object with rank and suit.
        """

        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        """
        Override the repr() conversion.
        Return a human readable string of the card
        (the same string as __str__()).
        """

        return self.__str__()

    def pretty_print(value: bool = True):
        """
        Important ! Should be called on the Class, not object.
        Use Card.pretty_print() instead of card_object.pretty_print()
        (This is a static method)
        Takes in an optional value, on or off in the form of boolean.
        Value is defaulted to True
        Toggles pretty print in self.settings (a static variable).
        Applys across all instances of Card
        """

        Card.settings["pretty_print"] = value

    def __str__(self) -> str:
        """
        Override the str() conversion.
        Returns a human readable representation in string of the card
        If pretty_print is enabled:
        Return a char art for better user experience.
        (the __repr__() invokes this method).
        """

        if not Card.settings["pretty_print"]:
            return f"{self.rank.name} of {self.suit.name}"

        suit_symbols = {
            "Clubs": "♣",
            "Diamonds": "♦",
            "Spades": "♠",
            "Hearts": "♥"
        }

        rank_values = [
            "",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "J",
            "Q",
            "K",
            "A",
        ]
        
        # get values to be inserted into the card template
        suit_symbol = suit_symbols[self.suit.name]
        value_top = rank_values[self.rank.value] + " "
        value_bottom = " " + rank_values[self.rank.value]
        if self.rank == Rank.Ten:
            value_top = value_bottom = "10"

        # insert the values into the card template
        shape = ("┌─────┐\n"
                 + f"│{value_top}   │\n"
                 + f"│  {suit_symbol}  │\n"
                 + f"│   {value_bottom}│\n"
                 + "└─────┘")

        return shape

    def __eq__(self, other: Card) -> bool:
        """
        Override the == operator.
        Compare suit and rank if they are equivalent.
        Return result as boolean.
        """

        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other: Card) -> bool:
        """
        Override the < operator.
        Compare suit, if suit is the same, compare rank.
        Return result as boolean.
        """

        # If same suit, compare rank
        if self.suit == other.suit:
            return self.rank < other.rank

        # if different suit, compare suit
        return self.suit < other.suit