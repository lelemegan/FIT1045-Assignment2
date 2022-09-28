from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player


class BetterAIPlayer(Player):
    """
    DESCRIPTION:
        A better AI player that automatically plays and passes cards.
        Guarantee more advanced strategies (compared to basic AI player).

        When playing a card, it plays according to scenarios.
        When passing card, it prioritises king/ace of spades then largest cards.
    
    ATTRIBUTES:
        Inherit the attributes of base player.

    OPERATIONS AVAILABLE:
        str conversion will return the player name
        repr connversion will return what str returns (the player name).
        (Inherited from Player)
    """

    def play_lowest_card(self, trick: list[Card], broken_hearts: bool) -> Card:
        """
        Takes in the game context including the trick (list of Card) and if hearts broken (bool) status.
        Removes and returns the lowest valid card to play from hand.
        """

        sorted_hand_cards = sorted(self.hand)
        for i in range(len(sorted_hand_cards)):
            card = sorted_hand_cards[i]
            if self.check_valid_play(card, trick, broken_hearts)[0]:
                del sorted_hand_cards[i]
                self.hand = sorted_hand_cards
                return card

    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
        '''
        Takes in the game context including the trick (list of Card) and if hearts broken (bool).
        Implements advanced strategies of playing cards compared to basic AI.
        
        Strategy used depends on four scenarios namely:
        - when player is lead
        - when player is not lead, when player hand has card that is same suit
          as lead, when player hand has card smaller than largest card
        - when player is not lead, when player hand has card that is same suit
          as lead, when player hand does not have card smaller than largest card
        - when player is not lead, when player hand does not have card that is 
          same suit as lead

        The card to play is removed from player hand and returned according 
        to the scenario.
        '''
        
        # if player leads
        if not trick:
            return self.play_lowest_card(trick, broken_hearts)

        valid_cards = list(filter(
            lambda card: self.check_valid_play(card, trick, broken_hearts)[0],
            self.hand))

        leading_suit = trick[0].suit
        same_suits = sorted(list(filter(
            lambda card: card.suit == leading_suit,
            valid_cards)))[::-1]

        # if player has leading card suit,
        # play largest card in hand that < largest card in trick
        if same_suits:
            largest_card = trick[0]
            for card in trick:
                if card > largest_card and card.suit == largest_card.suit:
                    largest_card = card

            # if player has no card lesser than the largest_card
            if all(i < largest_card for i in same_suits):
                # play the smallest
                self.hand.remove(same_suits[-1])
                return same_suits[-1]

            for card in same_suits:
                if card < largest_card:
                    self.hand.remove(card)
                    return card

        # if player has no leading suit, play the largest heart
        # if no heart card, play the largest card
        hearts = sorted(list(filter(
            lambda card: card.suit == Suit.Hearts,
            valid_cards)))[::-1]
        if hearts:
            self.hand.remove(hearts[0])
            return hearts[0]

        card = sorted(valid_cards)[::-1][-1]
        self.hand.remove(card)
        return card

    def pass_cards(self) -> list[Card]:
        """
        Implements advanced strategies of passing cards compared to basic AI.

        Checks if king of spades or ace of spades is in player hand.
        King of spades and ace of spades are prioritised to pass.
        Other card(s) chosen to pass from largest.
        
        Return chosen cards to pass as list.
        """

        # check if K/A of spades exists
        k_of_spades = Card(Rank.King, Suit.Spades)
        a_of_spades = Card(Rank.Ace, Suit.Spades)
        selected = []
        if k_of_spades in self.hand:
            selected.append(k_of_spades)
            self.hand.remove(k_of_spades)

        if a_of_spades in self.hand:
            selected.append(a_of_spades)
            self.hand.remove(a_of_spades)

        # prioritse on largest hearts
        sorted_hand = sorted(self.hand)[::-1]
        for card in sorted_hand:
            if len(selected) >= 3:
                break

            selected.append(card)
            self.hand.remove(card)

        return selected
