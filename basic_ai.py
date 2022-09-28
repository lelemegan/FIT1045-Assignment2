from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player


class BasicAIPlayer(Player):
    """
    DESCRIPTION:
        A basic AI player that automatically plays and passes cards.
        Does not guarantee any advanced strategies.

        When playing a card, it plays the lowest valid card (see Card.__lt__)
        When passing card, it passes the highest 3 cards (see Card.__lt__)

    ATTRIBUTES:
        name: str, the name of the player
        hand: list of Cards, the list of cards this player holds
        round_score: int, the score for a current round
        total_score: int, the score for the entire game

    OPERATIONS AVAILABLE:
        str conversion will return the player name
        repr connversion will return what str returns (the player name).
        (Inherited from Player)
    """

    name: str
    hand: list[Card]
    round_score: int
    total_score: int

    def play_card(
      self, trick: list[Card], broken_hearts: bool) -> Card:
        """
        Takes in the game context including the trick (list of Card) and if hearts broken (bool).
        Remove the lowest valid card to play from hand.
        Return the card that is removed.
        """

        sorted_hand_cards = sorted(self.hand)

        # play the first card that is valid
        for i in range(len(sorted_hand_cards)):
            card = sorted_hand_cards[i]
            if self.check_valid_play(card, trick, broken_hearts)[0]:
                # delete the card from list before returning
                del sorted_hand_cards[i]
                self.hand = sorted_hand_cards
                return card

    def pass_cards(self) -> list[Card]:
        """
        Remove the 3 highest cards from hand.
        Return the 3 highest cards that is removed as list.
        """

        # sort in decending order
        sorted_hand_cards = sorted(self.hand)[::-1]
        
        # pass the three largest card and remove them from hand
        result = sorted_hand_cards[:3]
        del sorted_hand_cards[:3]
        self.hand = sorted_hand_cards
        return result

