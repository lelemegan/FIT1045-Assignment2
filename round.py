from __future__ import annotations
from cards import Card, Rank, Suit
from time import sleep
from player import Player


class Round:
    """
    DESCRIPTION:
        The execution of a round
        Rounds has iterations where each iterations plays with a new empty
        trick.
        Each iterations lets each player plays card in ascending order of
        players in a list
        At the end of each iteration, penalty is calculated depending on the
        cards in trick,
        and the penalty is added to round_point of the taking player.
        In the first iteration, player who holds Two of Clubs leads
        Starting from the 2nd iteration, player who took the previous trick
        leads
        When an action happened, including player plays a card, hearts being
        broken and
        player takes the trick, the respecitve messages are being printed.
    ATTRIBUTES:
        players: list of Players, a ordered list of the player playing
        hearts_broken: boolean, to record if hearts are broken in this round
        starting_player_index: int, the index of the player who holds Two of
        clubs
        current_trick: list of Cards, the trick of the current iteration
        current_starting_player_index: the index of leading player of the
        current iteration
    OPERATIONS AVAILABLE:
        the round will start execution when the object is created (when
        __init__ is called)
    """

    players: list[Player]
    hearts_broken: bool
    starting_player_index: int
    current_trick: list[Card]
    current_starting_player_index: int

    def __init__(self, players: list) -> None:
        """
        initialise the round, and execute the round.
        """
        self.players = players
        self.hearts_broken = False
        self.starting_player_index = self.determin_first_player()
        self.current_trick = []
        self.current_starting_player_index = self.starting_player_index
        self.execute_round()

    def determin_first_player(self) -> int:
        """
        determine the index of the player holding Two of Clubs,
        assign the attribute and return the index
        """
        player_index = 0
        for player in self.players:
            if Card(Rank.Two, Suit.Clubs) in player.hand:
                return player_index
            player_index += 1

    def get_absolute_player_index(self, index: int) -> None:
        """
        take in a integer and get the remainder dividing the length of player.
        """
        return index % len(self.players)

    def determine_taker_index(self) -> int:
        """
        determine the player index of the player who takes the trick
        and return as integer
        """
        max_card_index = 0
        max_card = self.current_trick[0]
        for card_index in range(len(self.current_trick)):
            card = self.current_trick[card_index]
            if card > max_card and card.suit == max_card.suit:
                max_card = card
                max_card_index = card_index

        taker_index = self.current_starting_player_index + max_card_index
        return self.get_absolute_player_index(taker_index)

    def determine_penalty(self) -> int:
        """
        determine the points the taker get, and return as integer
        """
        points = 0
        for card in self.current_trick:
            if card.suit == Suit.Hearts:
                points += 1
            if card.suit == Suit.Spades and card.rank == Rank.Queen:
                points += 13
        return points

    def prepare_new_iteration(self, new_player_starting_index) -> None:
        """
        prepare a new iteration by clearing up the trick and assigning the
        new_player_index
        """
        self.current_starting_player_index = new_player_starting_index
        self.current_trick = []

    def execute_player_turn(self, player_index) -> Card:
        """
        Execute a player turn in an iteration. Messages are printed for action
        done by player.
        The played card is returned.
        """
        player = self.players[player_index]
        
        print(f"It is {player}'s turn")
        
        card_played = player.play_card(self.current_trick, self.hearts_broken)

        sleep(1)

        if self.current_trick:
            print(f"{player} plays \n{card_played}")
        else:
            print(f"{player} leads the trick with \n{card_played}")

        if card_played.suit == Suit.Hearts and not self.hearts_broken:
            print("Hearts have been broken!")
            self.hearts_broken = True
        self.current_trick.append(card_played)

        return card_played

    def execute_iteration(self) -> None:
        """
        Execute a an iteration. Players executes their turn in ascending index
        order
        """
        starting_index = self.current_starting_player_index
        player_length = len(self.players)
        for i in range(starting_index, starting_index + player_length):
            player_index = self.get_absolute_player_index(i)
            self.execute_player_turn(player_index)

    def execute_round(self) -> None:
        """
        Execute a round, controls the flow of game including determining the
        leading player of each iteration
        """
        while len(self.players[0].hand) > 0:
            self.execute_iteration()
            penalty = self.determine_penalty()
            taker_index = self.get_absolute_player_index(
                self.determine_taker_index()
            )
            taker = self.players[taker_index]
            taker.round_score += penalty
            print(f"{taker} takes the trick. Points received: {penalty}")
            self.prepare_new_iteration(taker_index)
