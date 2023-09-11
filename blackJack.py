from random import shuffle

suits = ('spades', 'hearts', 'clubs', 'diamonds')
ranks = ('ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king')
values = {'ace_low':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10, 'jack':10, 'queen':10, 'king':10, 'ace_high':11}

cards_number = 2
money_init = 100
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


class Player:
	def __init__(self, money):
		self.money = money
		self.bet = 0
		self.cards = []
		self.value = 0
	
	def get_card(self, card):
		self.cards.append(card)
		self.value = eval_cards(self.cards)
	
	def lose_money(self):
		self.money -= self.bet
	
	def add_money(self, money):
		self.money += money
	
	def clear_cards(self):
		self.cards = []
		self.value = 0

	def ask_bet(self):
		while True:
			try:
				self.bet = int(input(f'What is your bet? '))
			except:
				print('Bet must be whole number!')
			else:
			  if self.bet > self.money:
			    print(f'Not enough funds! You have only {self.money}.')
			  else:
			    print()
			    break
	
	def __str__(self):
		if len(self.cards) == 0:
		  return 'no cards'
		else:
		  cards_list = []

		  for card in self.cards:
		    cards_list.append(str(card))

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
player = Player(money_init)
dealer = Player(0)

while True:
	deck = Deck()
	print(f"You're account: {player.money}")
	player.ask_bet()
	
	for i in range(cards_number):
	  player.get_card(deck.deal())
	  dealer.get_card(deck.deal())
	
	print(f'Dealer has {dealer.cards[0]}.')
	
	while True:
	  print(f'You have {str(player)}.')

	  if player.value > busted_value:
	    player.lose_money()
	    print("You're busted!")
	    break
	  else:
	    if ask('hit'):
	      player.get_card(deck.deal())
	    else:
	      print("Now it's dealer's turn.")
	      break
	
	while player.value <= busted_value:
	  print(f'Dealer has {str(dealer)}.')

	  if dealer.value > busted_value:
	    player.add_money(player.bet)
	    print(f'Dealer is busted!')
	    print(f"You've won! Scored {player.value}.")
	    break
	  elif dealer.value > player.value and dealer.value <= busted_value:
	    player.lose_money()
	    print(f'Dealer has won!')
	    break
	  else:
	    dealer.get_card(deck.deal())
	
	print(f"You're account: {player.money}")
	
	if player.money <= 0:
	  print(f'You have no money! Game over!')
	  break
	else:
	  if not ask('play again'):
	    break
	  else:
	    player.clear_cards()
	    dealer.clear_cards()

