"""
Black Jack card game

A player plays Black Jack card game against computer dealer. The player starts with 100 chips from
which can place a bet. The goal is to have total value of all cards on hand as close as possible to
value 21. At the beginning, the player gets two cards from the deck and then opts even to take
another card (hit) or to stop playing. The player can take as many cards as needs but once total
value of all cards on player's hand exceeds value 21, player immediately loses (player is busted).
After player stops hitting, it's dealer's turn. Whoever (player or dealer) is at the end closer to
value 21 and isn't busted, wins. Jack, Queen and King has value 10, Ace has value 11 or 1, whatever
is closer to 21 and doesn't cause loss.
"""

from random import shuffle

suits = ('spades', 'hearts', 'clubs', 'diamonds')
ranks = ('ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack',
		 'queen', 'king')
values_dict = {'ace_low':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8,
          'nine':9, 'ten':10, 'jack':10, 'queen':10, 'king':10, 'ace_high':11}

CARDS_NUMBER = 2
CHIPS_INIT = 100
BUSTED_VALUE = 21


class Card:
    """
    Playing card representation.
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:
    """
    Card deck representation.
    
    Constructor creates deck of 52 unique playing cards.
    Method deal() takes one of the cards in the deck
    and returns it.
    """
    def __init__(self):
        self.cards = []

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

        shuffle(self.cards)

    def deal(self):
        """
		Deal one card from the deck.
        """
        return self.cards.pop()


class Account:
    """
    Chip account representation.
    
    Possible operations: place bet, win bet, lose bet.
    """
    def __init__(self, chips = 0):
        self.chips = chips
        self.bet = 0

    def lose_chips(self):
        """
        Lose betted chips.
        """
        self.chips -= self.bet

    def win_chips(self):
        """
        Win betted chips.
        """
        self.chips += self.bet

    def place_bet(self, chips):
        """
        Set given number of chips as a bet.
        """
        self.bet = chips


class Hand:
    """
    Represents cards held by player or dealer.
    """
    def __init__(self):
        self.cards = []
        self.value = 0

    def get_card(self, card):
        """
        Get a card and add it to the hand.
        """
        self.cards.append(card)
        self.value = eval_cards(self.cards, values_dict)

    def clear_cards(self):
        """
        Remove all cards from the hand.
        """
        self.cards = []
        self.value = 0


    def __str__(self):
        if len(self.cards) == 0:
            return 'no cards'

        cards_list = [str(card) for card in self.cards]
        return ', '.join(cards_list) + f' - best value: {self.value}'


class Player(Hand):
    """
    Player representation.
    
    Player holds cards in his hand and has its own chips account.
    """
    def __init__(self, chips):
        self.account = Account(chips)
        Hand.__init__(self)

    def ask_bet(self):
        """
        Ask player how many chips wants to bet.
        Funds available are checked before chips are betted.
        """
        while True:
            try:
                bet = int(input('What is your bet? '))
            except ValueError:
                print('Bet must be whole number!')
            else:
                if bet > self.account.chips:
                    print(f'Not enough funds! You have only {self.account.chips}.')
                else:
                    self.account.place_bet(bet)
                    print()
                    break


def ask(question):
    """
    Asks player given question and expects yes or no as an answer.
    """
    while True:
        answer = input(f'Do you want to {question}? [Y/N] ').upper()

        if answer in ('Y', 'N'):
            print()
            break

    return answer == 'Y'


def eval_cards(cards, values):
    """
    Function takes list of cards, dictionary of card values
    and calculates total value of all cards in the list.
    """
    vals = [0]
    aces = 0
    best = 0

    for card in cards:
        if card.rank == 'ace':
            aces += 1
            vals[0] +=  values['ace_low']
        else:
            vals[0] += values[card.rank]

    for ace in range(1, aces+1):
        vals.append(vals[0] + (ace*(values['ace_high']-values['ace_low'])))

    best = vals[0]

    for value in vals:

        if abs(value - BUSTED_VALUE) < abs(best - BUSTED_VALUE) and value <= BUSTED_VALUE:
            best = value

    return best


print('Welcome in Black Jack game!')
player = Player(CHIPS_INIT)
dealer = Hand()

while True:
    deck = Deck()
    print(f"You're account: {player.account.chips}")
    player.ask_bet()

    for i in range(CARDS_NUMBER):
        player.get_card(deck.deal())
        dealer.get_card(deck.deal())

    print(f'Dealer has {dealer.cards[0]}.')

    while True:
        print(f'You have {player}.')

        if player.value > BUSTED_VALUE:
            player.account.lose_chips()
            print("You're busted!")
            break

        if ask('hit'):
            player.get_card(deck.deal())
        else:
            print("Now it's dealer's turn.")
            break

    while player.value <= BUSTED_VALUE:
        print(f'Dealer has {dealer}.')

        if dealer.value > BUSTED_VALUE:
            player.account.win_chips()
            print('Dealer is busted!')
            print(f"You've won! Scored {player.value}.")
            break

        if dealer.value > player.value:
            player.account.lose_chips()
            print('Dealer has won!')
            break

        dealer.get_card(deck.deal())

    print(f"You're account: {player.account.chips}")

    if player.account.chips <= 0:
        print('You have no chips! Game over!')
        break

    if not ask('play again'):
        break

    player.clear_cards()
    dealer.clear_cards()
