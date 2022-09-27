from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player


class BasicAIPlayer(Player):
    """
    DESCRIPTION:
        A basic AI player that automatically plays and passes cards.
        Does not garentee any advanced stratagies.

        When playing a card, it plays the lowest valid card (see Card.__lt__)
        When passing card, it passes the highest 3 cards (see Card.__lt__)
    ATTRIBUTES:
        name: str, the name of the player
        hand: list of Cards, the list of cards this player holds
        round_score: int, the score for a current round
        total_score: int, the score for the entier game
    OPERATIONS AVAILABLE:
        str/repr conversion to get the string of a player name
    """

    name: str
    hand: list[Card]
    round_score: int
    total_score: int

    def play_card(
      self, trick: list[Card], broken_hearts: bool) -> Card:
        """
        takes in the game context including the trick and if hearts broken
        and in the environment of game context and currently holding cards,
        return the lowest valid card to play from hand
        the card is removed from hand
        """
        sorted_hand_cards = sorted(self.hand)
        for i in range(len(sorted_hand_cards)):
            card = sorted_hand_cards[i]
            if self.check_valid_play(card, trick, broken_hearts)[0]:
                del sorted_hand_cards[i]
                self.hand = sorted_hand_cards
                return card

    def pass_cards(self) -> list[Card]:
        """
        return 3 highest cards in hand,
        the 3 cards are being removed from hand
        """
        sorted_hand_cards = sorted(self.hand)[::-1]  # in decending order
        result = sorted_hand_cards[:3]
        del sorted_hand_cards[:3]
        self.hand = sorted_hand_cards
        return result

