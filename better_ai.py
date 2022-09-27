from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player


class BetterAIPlayer(Player):
    def play_lowest_card(
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

    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
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

            # if player has no card lesser then the largest_card
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
