from __future__ import annotations
import random
from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer
from round import Round


class Hearts:
    """
    DESCRIPTION:
        A hearts game.
        2 integer inputs (target_score, player_count) are being read from
        standard input in the begninning.
        Rounds are being executed until atleast one player reached the
        target_score and there is only one winner.
        Before each round is executed, players are generated,
        during each round, random deck are dealt to player, with the deck
        validity being validated.
        The player then pass the cards if necessary.
        The player pass the card to (round_number % len(players)) players to
        the right (in incrementing order).
        When the offset (round_number % len(players)) is 0, player do not pass
        cards
        The round begins by invoking the Round class
        Player statistics are printed at the end of each round.
        End of game is being checked after execution of each round.

    ATTRIBUTES:
        target_score: int, the minimum target score as a game ending threshold
        player_cound: int, the number of player playing, has to be 3, 4 or 5
        players: list of Players, a ordered list of the player playing
        round_number: int, the number of round currently at. Starting from 1

    OPERATIONS AVAILABLE:
        the game will start execution when the object is created
        (when __init__ is called)
    """

    target_score: int
    player_count: int
    players: list
    round_number: int

    def __init__(self) -> None:
        """
        Get user input, initialise attributes and execute the game.
        """

        self.get_initalize_inputs()
        self.generate_players()
        self.round_number = 1
        self.execute_rounds()

    def generate_players(self) -> None:
        """
        Generate a list of players based on player_count.
        The generated players are assigned to self.players.
        """

        self.players = []
        for i in range(self.player_count):
            self.players.append(BasicAIPlayer(f"Player {i+1}"))

    def generate_deck(self) -> list[Card]:
        """
        Generate a deck based on player_count.
        Removes specific cards if the necessary.
        Return the list of cards unshuffled.
        """

        deck = []
        for suit in Suit:
            for rank in Rank:
                deck.append(Card(rank, suit))

        if self.player_count == 5:
            deck.remove(Card(Rank.Two, Suit.Diamonds))
            deck.remove(Card(Rank.Two, Suit.Spades))

        if self.player_count == 3:
            deck.remove(Card(Rank.Two, Suit.Diamonds))

        return deck

    def validate_card_segment(self, cards: list[Card]) -> bool:
        """
        Validate if a segment is valid for a player to receive as hand cards.
        Return the result as a boolean.
        """

        for card in cards:
            if card.suit == Suit.Spades and card.rank == Rank.Queen:
                continue

            if card.suit != Suit.Hearts:
                return True

        return False

    def dealt_card(self) -> None:
        """
        Generate a deck, shuffle and dealt to players.
        The player will hold the cards after this function,
        No return value applicable.
        """

        while True:
            cards = self.generate_deck()
            random.shuffle(cards)
            deck_size = len(cards)
            segment_size = deck_size / self.player_count
            for i in range(self.player_count):
                seg_from = int(i*segment_size)
                seg_to = int((i+1)*segment_size)
                deck_segment = cards[seg_from:seg_to]
                if not self.validate_card_segment(deck_segment):
                    continue
                self.players[i].hand = deck_segment
            return

    def get_initalize_inputs(self) -> None:
        """
        Get and validate user input (targest_score, player_count) from 
        standard input.
        The result is directly assigned to the attributes.
        """

        # get target_score
        while True:
            try:
                input_score = int(input("Please enter a target score: "))

                if input_score <= 0:
                    print("Target score needs to be atleast 1")
                    continue

                self.target_score = input_score
                break

            except ValueError:
                print("Target score has to be a whole number")

        # get player_count
        while True:
            try:
                input_score = int(
                    input("Please enter a player count (3 to 5): ")
                )

                if input_score < 3 or input_score > 5:
                    print("Player count needs to be 3, 4 or 5")
                    continue

                self.player_count = input_score
                break

            except ValueError:
                print("Player count has to be 3, 4 or 5")

    def get_absolute_index(self, index: int) -> int:
        """
        Return absolute index of a player.
        Example: when there is 3 players, player index 3 will return 0,
        and index 4 will return 1 as it wraps around.
        """

        return index % self.player_count

    def pass_cards(self) -> None:
        """
        Pass 3 cards to a n-th player to the right for all player
        (in ascending order).
        when the n-th offset is 0, do not pass.
        """

        player_offset = self.round_number % self.player_count

        if not player_offset:
            return

        target_cards = {}
        for i in range(self.player_count):
            target_index = self.get_absolute_index(i + player_offset)
            source_player = self.players[i]
            target_player = self.players[target_index]
            cards = source_player.pass_cards()
            target_cards[target_index] = cards

            print(f"{source_player} passed {cards} to {target_player}")

        for i in target_cards.keys():
            self.players[i].hand += target_cards[i]

    def calculate_points(self) -> None:
        """
        Calculate the points,
        assign the round_points of a player to total_point.
        A player does not receive points if they have 26 points,
        all other player recieve 26 points (Shot the moon).
        """

        for i in range(len(self.players)):
            player = self.players[i]

            # shoot the moon
            if player.round_score == 26:
                print(f"{player} has shot the moon! Everyone else receives 26"
                      + " points")
                # add 26 to other players
                player.round_score = 0
                for j in range(len(self.players)):
                    if j == i:
                        continue
                    self.players[j].total_score += 26
                return

            player.total_score += player.round_score
            player.round_score = 0

    def end_of_game(self) -> bool:
        """
        Check if at least one player reached target_score and
        there is only one winner with minimum score.
        Return the result as boolean.
        """

        target_score_reached = False
        for player in self.players:
            if player.total_score >= self.target_score:
                target_score_reached = True
                break

        if not target_score_reached:
            return False

        scores = []
        for player in self.players:
            scores.append(player.total_score)

        min_score_count = 0
        for score in scores:
            if score == min(scores):
                min_score_count += 1

        return min_score_count == 1

    def determine_winner(self) -> int:
        """
        Determine the player who has the lowest score.
        Return the index of the player.
        """

        min_score = self.players[0].total_score
        min_score_player_index = 0
        for i in range(len(self.players)):
            player = self.players[i]
            if player.total_score < min_score:
                min_score = player.total_score
                min_score_player_index = i

        return min_score_player_index

    def print_player_statistics(self) -> None:
        """
        Print the total scores of all players.
        """

        for player in self.players:
            print(f"{player}'s total score: {player.total_score}")

    def execute_rounds(self) -> None:
        """
        Prepare a game and execute the rounds.
        The game continues until end_of_game() conditions reached
        (until the function returns True).
        In each round, cards are dealt, 3 cards are passed
        (or not depending on round number).
        Player play their round.
        After each round, player notified of moon shot if there are any.
        Player statistics printed.
        Winner announced if the game ends.
        """

        while True:

            print(f"========= Starting round {self.round_number} =========")
            self.dealt_card()
            
            for player in self.players:
                print(f"{player} was dealt {player.hand}")

            self.pass_cards()
            Round(self.players)

            print(f"========= End of round {self.round_number} =========")
            self.calculate_points()
            self.print_player_statistics()

            # check if game ends
            if self.end_of_game():
                winner_index = self.determine_winner()
                winner = self.players[winner_index]
                print(f"{winner} is the winner!")
                break

            self.round_number += 1


if __name__ == "__main__":
    Hearts()
