from random import shuffle

suits = ('spades', 'hearts', 'clubs', 'diamonds')
ranks = ('ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king')
values = {'ace_low':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10, 'jack':10, 'queen':10, 'king':10, 'ace_high':11}

cards_number = 2
money_init = 100


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
		self.cards = []
		self.value = 0
	
	def get_card(self, card):
		self.cards.append(card)
		self.value = eval_cards(self.cards)
	
	def bet(self, money):
		self.money -= money
		return money
	
	def add_money(self, money):
		self.money += money
	
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
			  if bet > self.money:
			    print(f'Not enough funds! You have only {self.money}.')
			  else:
			    break
	
		self.bet(bet)
		print()
		return bet
	
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
	    break

	print()
	return answer == 'Y'


def eval_cards(cards):
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
		  if abs(value - 21) < abs(best - 21) and value <= 21:
		    best = value

	return best


print('Welcome in Black Jack game!')
player = Player(money_init)
dealer = Player(0)

while True:
	deck = Deck()
	print(f"You're account: {player.money}")
	bet = player.ask_bet()
	
	for i in range(cards_number):
	  player.get_card(deck.deal())
	  dealer.get_card(deck.deal())
	
	print(f'Dealer has {dealer.cards[0]}.')
	
	while True:
	  print(f'You have {str(player)}.')

	  if player.value > 21:
	    print("You're busted!")
	    break
	  else:
	    if ask('hit'):
	      player.get_card(deck.deal())
	    else:
	      print("Now it's dealer's turn.")
	      break
	
	while player.value <= 21:
	  print(f'Dealer has {str(dealer)}.')

	  if dealer.value > 21:
	    print(f'Dealer is busted!')
	    print(f"You've won! Scored {player.value}.")
	    player.add_money(bet*2)
	    break
	  elif dealer.value > player.value and dealer.value <= 21:
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

