from __future__ import annotations
from cards import Card, Rank, Suit


class Player:
    '''
    DESCRIPTION:
    

    ATTRIBUTES:
        name: str, the name of the player
        hand: list of Cards, the list of cards this player holds
        round_score: int, the score for a current round
        total_score: int, the score for the entire game

    OPERATIONS AVAILABLE:
        str/repr conversion to get the string of a player name
    '''
    
    name: str
    hand: list[Card]
    round_score: int
    total_score: int

    def __init__(self, name: str) -> None:
        '''
        Assign name attribute.
        Initialise hand, round_score and total_score to default value.
        '''
        
        self.name = name
        self.hand = []
        self.round_score = 0
        self.total_score = 0

    def __str__(self) -> None:
        return self.name

    def __repr__(self) -> None:
        return self.__str__()

    def check_valid_play(self, card: Card, trick: list[Card], broken_hearts: bool) -> tuple(bool, str):
        '''
        Takes in the game context including the trick and if hearts broken
        and in the environment of game context and currently holding cards,
        determine if a given card is valid to play.
        Return result as tuple.
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
                        "You must play a card that has the same suit as the leading card")
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

