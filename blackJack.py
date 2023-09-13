from random import shuffle

suits = ('spades', 'hearts', 'clubs', 'diamonds')
ranks = ('ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king')
values = {'ace_low':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10, 'jack':10, 'queen':10, 'king':10, 'ace_high':11}

cards_number = 2
chips_init = 100
busted_value = 21


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
		self.value = eval_cards(self.cards, values)
	
	def clear_cards(self):
		self.cards = []
		self.value = 0

	def ask_bet(self):
		while True:
			try:
				bet = int(input(f'What is your bet? '))
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
		else:
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

	for i in range(1, aces+1):
	  vals.append(vals[0] + (i*(values['ace_high']-values['ace_low'])))

	best = vals[0]

	for value in vals:
		  if abs(value - busted_value) < abs(best - busted_value) and value <= busted_value:
		    best = value

	return best


print('Welcome in Black Jack game!')
player = Player(chips_init)
dealer = Player(0)

while True:
	deck = Deck()
	print(f"You're account: {player.account.chips}")
	player.ask_bet()
	
	for i in range(cards_number):
	  player.get_card(deck.deal())
	  dealer.get_card(deck.deal())
	
	print(f'Dealer has {dealer.cards[0]}.')
	
	while True:
	  print(f'You have {player}.')

	  if player.value > busted_value:
	    player.account.lose_chips()
	    print("You're busted!")
	    break
	  elif ask('hit'):
	    player.get_card(deck.deal())
	  else:
	    print("Now it's dealer's turn.")
	    break
	
	while player.value <= busted_value:
	  print(f'Dealer has {dealer}.')

	  if dealer.value > busted_value:
	    player.account.win_chips()
	    print(f'Dealer is busted!')
	    print(f"You've won! Scored {player.value}.")
	    break
	  elif dealer.value > player.value and dealer.value <= busted_value:
	    player.account.lose_chips()
	    print(f'Dealer has won!')
	    break
	  else:
	    dealer.get_card(deck.deal())
	
	print(f"You're account: {player.account.chips}")
	
	if player.account.chips <= 0:
	  print(f'You have no chips! Game over!')
	  break
	elif not ask('play again'):
	  break
	else:
	  player.clear_cards()
	  dealer.clear_cards()

