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
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:
    def __init__(self):
        self.cards = []

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

        shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class Account:
    def __init__(self, chips = 0):
        self.chips = chips
        self.bet = 0

    def lose_chips(self):
        self.chips -= self.bet

    def win_chips(self):
        self.chips += self.bet

    def place_bet(self, chips):
        self.bet = chips


class Player:
    def __init__(self, chips = 0):
        self.account = Account(chips)
        self.cards = []
        self.value = 0

    def get_card(self, card):
        self.cards.append(card)
        self.value = eval_cards(self.cards, values_dict)

    def clear_cards(self):
        self.cards = []
        self.value = 0

    def ask_bet(self):
        while True:
            try:
                bet = int(input('What is your bet? '))
            except:
                print('Bet must be whole number!')
            else:
                if bet > self.account.chips:
                    print(f'Not enough funds! You have only {self.account.chips}.')
                else:
                    self.account.place_bet(bet)
                    print()
                    break

    def __str__(self):
        if len(self.cards) == 0:
            return 'no cards'

        cards_list = [str(card) for card in self.cards]
        return ', '.join(cards_list) + f' - best value: {self.value}'


def ask(question):
    while True:
        answer = input(f'Do you want to {question}? [Y/N] ').upper()

        if answer in ('Y', 'N'):
            print()
            break

    return answer == 'Y'


def eval_cards(cards, values):
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
dealer = Player(0)

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
