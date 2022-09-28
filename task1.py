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
        You can use the less then operator (>) to compare between ranks.
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
        # override "<" operator
        return other.value > self.value


class Suit(Enum):
    """
    DESCRIPTION:
        Suits available in a set of playing cards.

    VALUES:
        The values are in the following ascending order.
        Clubs, Diamonds, Spades, Hearts

    OPERATIONS AVAILABLE:
        You can use the less then operator (>) to compare between suits.
    """

    Clubs = 0
    Diamonds = 1
    Spades = 2
    Hearts = 3

    def __lt__(self, other: Suit) -> bool:
        # override "<" operator
        return other.value > self.value


class Card:
    """
    DESCRIPTION:
        A card that can be found in a regular set of playing card.
        Only capable of general cards (rank and number),
        and incapable of special cards (Joker cards).

    ATTRIBUTES:
        Rank: the rank of the card representing
        Suit: the suit of the card representing

    OPERATIONS AVAILABLE:
        The less than order comparison operator (>) to compare between cards.
        The equality comparison operator (==) to compare between cards.
        The repr or str conversion to convert into readable format.
    """

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
        (the same string as __str__())
        """

        return self.__str__()

    def __str__(self) -> str:
        """
        Override the str() conversion.
        Return a human readable string of the card
        (the __repr__() invokes this method)
        """

        return f"{self.rank.name} of {self.suit.name}"

    def __eq__(self, other: Card) -> bool:
        """
        Override the == operator.
        Compare suit and rank if they are equivalent.
        Return result as boolean
        """

        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other: Card) -> bool:
        """
        Override the < operator.
        Compare suit, if suit is the same, compare rank.
        Return result as boolean.
        """

        # if same suit compare rank
        if self.suit == other.suit:
            return self.rank < other.rank

        # if different suit, compare suit
        return self.suit < other.suit

