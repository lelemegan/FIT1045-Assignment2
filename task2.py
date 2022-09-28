from __future__ import annotations
from cards import Card, Rank, Suit


class BasicAIPlayer:
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
    """

    name: str
    hand: list[Card]
    round_score: int
    total_score: int

    def __init__(self, name: str) -> None:
        """
        Assign name attribute.
        Initialise hand, round_score and total_score to default value.
        """

        self.name = name
        self.hand = []
        self.round_score = 0
        self.total_score = 0

    def check_valid_play(
      self,
      card: Card,
      trick: list[Card],
      broken_hearts: bool
      ) -> tuple[bool, str]:
        '''
        Takes in the game context including the trick (list of Card) and if hearts broken (bool).
        In the environment of game context and currently holding cards,
        determine if a given card is valid to play.
        Return result as tuple of boolean (reuslt) and string (error message) if applicable.
        '''

        # player is not leading
        if trick:
            leading_suit = trick[0].suit

            # check if user has leading Suit
            has_leading_suit = False
            for i in self.hand:
                if i.suit == leading_suit:
                    has_leading_suit = True
                    break

            # if player has leading suit
            if has_leading_suit:
                # player must play same suit
                if card.suit == leading_suit:
                    return True, ""

                return (False,
                        "Player must play the same suit as the leading suit")
            else:
                # player can play any card
                return True, ""

        # player is leading
        else:
            # If Two of clubs exist, player must not play any other
            if Card(Rank.Two, Suit.Clubs) in self.hand:
                if card == Card(Rank.Two, Suit.Clubs):
                    return True, ""

                return False, "Player must play Two of Clubs"

            # If hearts broken, player play any Card
            if broken_hearts:
                return True, ""

            # Check if non heart card exist
            has_none_heart_card = False
            for i in self.hand:
                if i.suit != Suit.Hearts:
                    has_none_heart_card = True
                    break

            # if only has heart, play any card
            if not has_none_heart_card:
                return True, ""

            # if hearts not broken, play non heart card
            if card.suit == Suit.Hearts:
                return False, "You have to play non-heart card"
            else:
                return True, ""

    def play_card(
      self, trick: list[Card], broken_hearts: bool) -> Card:
        """
        Takes in the game context including the trick and if hearts broken
        and in the environment of game context and currently holding cards,
        return the lowest valid card to play from hand
        the card is removed from hand
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
        Return 3 highest cards in hand,
        the 3 cards are being removed from hand
        """

        # sore the hand in decending order
        sorted_hand_cards = sorted(self.hand)[::-1]

        # pass the three largest card and remove them from hand
        result = sorted_hand_cards[:3]
        del sorted_hand_cards[:3]
        self.hand = sorted_hand_cards
        return result

    def __str__(self):
        """
        Override the str() conversion.
        Return the name of the player
        (the __repr__() invokes this method)
        """
        return self.name

    def __repr__(self):
        """
        Override the repr() conversion.
        Return the name of the player
        (the same string as __str__())
        """
        return self.__str__()

