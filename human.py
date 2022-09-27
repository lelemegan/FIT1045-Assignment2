from __future__ import annotations
from cards import Card
from player import Player


class Human(Player):
    def __init__(self) -> None:
        raw_name = input("Please enter your name: ")
        super().__init__(raw_name)
        self.delimiter = ','

    def get_single_user_input(
      self, prompt: str, range: tuple[int] = ()) -> int:
        while True:
            try:
                val = int(input(prompt))
                err = (f"You must enter a number in the range of {range[0]} to"
                       + f"{range[1]}")
                assert val >= range[0], err
                assert val <= range[1], err
                return val
            except ValueError:
                print("You must input an integer")
            except AssertionError as err:
                print(err)

    def get_user_input_cs(
      self, prompt: str, count: int, range: tuple[int] = ()) -> tuple[int]:
        while True:
            try:
                raw_seperated = input(prompt).split(self.delimiter)
                result = [int(i) for i in raw_seperated]
                all_value_in_range = all((i >= range[0])
                                         and (i <= range[1])
                                         for i in result)
                range_err_msg = ("All number must be in the range of"
                                 + f" {range[0]} to {range[1]}")
                assert all_value_in_range, range_err_msg
                assert len(result) == count, f"You must input {count} integers"
                return tuple(result)
            except ValueError:
                print("You must input integers seperated by '"
                      + self.delimiter + "'")
            except AssertionError as err:
                print(err)

    def get_card_art_from_list(self, cards: list[Card]):
        card_arts = [str(card) for card in cards]
        card_lines = [art.split("\n") for art in card_arts]
        card_appended_lines = zip(*card_lines)
        card_appended_arts = ["".join(line) for line in card_appended_lines]
        return "\n".join(card_appended_arts)


    def print_hand(self) -> None:
        print("Cards available:")
        print(self.get_card_art_from_list(self.hand))
        numberings = ""
        for i in range(len(self.hand)):
            numberings += " " * (4 - len(str(i + 1)))
            numberings += str(i + 1)
            numberings += "   "
        print(numberings)

    def print_trick(self, trick) -> None:
        if not trick:
            print("Trick is currently empty.")
            return

        print("Current Trick:")
        print(self.get_card_art_from_list(trick))

    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
        self.print_trick(trick)
        self.print_hand()
        print("Hearts are {}broken".format("" if broken_hearts else "not "))
        print()

        while True:
            card_index = self.get_single_user_input("Select a card to play:",
                                                    (1, len(self.hand))) - 1
            card = self.hand[card_index]

            validate = self.check_valid_play(card, trick, broken_hearts)

            if not validate[0]:
                print(validate[1])
                continue

            del self.hand[card_index]

            return card

    def pass_cards(self, passing_to: str) -> list[Card]:
        self.print_hand()
        print()

        prompt = (f"Select 3 cards to pass to {passing_to} \n"
                  + f"(Enter numbers seperated with '{self.delimiter}'):")
        
        while True:
            card_indices = self.get_user_input_cs(prompt, 3, (1, len(self.hand)))
            # check duplication
            if not any(card_indices.count(i) > 1 for i in card_indices):
                break
            print("You cannot enter the same number multiple times")

        cards = [self.hand[i - 1] for i in card_indices]
        
        for card in cards:
            self.hand.remove(card)

        print(f"You have passed the following cards to {passing_to}:\n"
              + self.get_card_art_from_list(cards) + "\n")
        return cards