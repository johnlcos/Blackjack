#NEEDED 
import random 
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit 
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) #create each card and add to deck
                
    def __str__(self): #print the deck
        deck_string = ''
        for card in self.deck:
            deck_string += '\n' + card.__str__()
        return 'Current deck contains:' + deck_string
    
    def shuffle(self):#shuffle deck
        random.shuffle(self.deck) 
        
    def deal(self): #deals one card from top of deck, returns the card
        return self.deck.pop(0)


class Hand:
    def __init__(self):
        self.cards = [] #list containing cards in hand
        self.value = 0 #value of all cards in hand
        self.aces = 0 #track number of aces
        
    def add_card(self,card):
        self.cards.append(card) #add card to hand
        self.value += values[card.rank] #calculate hand value
        if card.rank == 'Ace': #if card is an ace, track
            self.aces += 1
    
    def ace_adjust(self):
        if self.aces != 0 and self.value > 21:
            self.value -= 10 #change value of an ace from 11 to 1
            self.aces -= 1 #use ace


class Player:
    def __init__(self, name, balance=100, bet=0):
        self.name = name
        self.balance = balance
        self.bet = bet
    
    def place_bet(self): #ask for the bet
        while True:
            try:
                self.bet = int(input('How many chips would you like to bet? '))
            except ValueError:
                print('Sorry, a bet must be an integer!')
            else:
                if self.bet > self.balance:
                    print("Sorry, your bet can't exceed",self.balance)
                else:
                    print('Great! You have wagered:',self.bet)
                    break
    
    def bet_win(self): #if bet won add bet
        self.balance += self.bet
        
    def bet_lose(self): #if bet lost subtract bet
        self.balance -= self.bet



def show_some(player_hand, dealer_hand):
    print('\nThe dealer has:')
    print(dealer_hand.cards[0])
    print('<hidden card>')
    print("\nPlayer's Hand:", *player_hand.cards, sep='\n ')


def hit_or_stand():
    move = ''
    while move not in ['H','S']:
        move = input('Would you like to hit or stand? (input H or S)')
        if move not in ['H','S']:
            print('Please input H or S')
    return move


def show_all(player_hand, dealer_hand):
    print("\nDealer's Hand:", *dealer_hand.cards, sep='\n ')
    print("\nPlayer's Hand:", *player_hand.cards, sep='\n ')


print('Welcome to Blackjack')
#create player, player hand and dealer hand
name = input('What is your name?')
balance = int(input('How much money are you playing with?'))
player = Player(name,balance)

while True:
    
    #create and shuffle deck
    deck = Deck()
    deck.shuffle()
    
    print(f'Hi {player.name}! Your current balance is ${player.balance}')
    
    player.place_bet() #prompt player for bet
    
    #deal player and dealer hads
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    #show cards
    show_some(player_hand,dealer_hand)
    
    #start playing
    playing = True
    hitting = True
    
    while playing:
    
        while hitting == True:
            move = hit_or_stand() #prompt to hit or stand
            if move == 'H':
                print('You decided to hit')
                player_hand.add_card(deck.deal())
                player_hand.ace_adjust()
            else:
                hitting = False
                print('You decided to stand')
                
            if player_hand.value > 21:
                show_some(player_hand,dealer_hand)
                print('You Busted! Thats tough...')
                player.bet_lose()
                hitting = False
                playing = False
                break
            show_some(player_hand,dealer_hand)
    
        if player_hand.value <= 21: #if no bust
        
            while dealer_hand.value < 17 or dealer_hand.value < player_hand.value: #if < 17 dealer hits
                dealer_hand.add_card(deck.deal())
                dealer_hand.ace_adjust()

                if dealer_hand.value > 21:
                    show_all(player_hand,dealer_hand)
                    print('Dealer has busted! You Win!')
                    player.bet_win()
                    playing = False
                    break
                
            if playing == True and player_hand.value > dealer_hand.value:
                show_all(player_hand,dealer_hand)
                print(f'Congrats {player.name}! You Win')
                player.bet_win()
                playing = False
                break
            
            elif playing == True and player_hand.value < dealer_hand.value:
                show_all(player_hand,dealer_hand)
                print(f'Sorry {player.name}! You Lose')
                player.bet_lose()
                playing = False
                break
            
            elif playing == True and player_hand.value == dealer_hand.value:
                show_all(player_hand,dealer_hand)
                print(f'Its a draw!')
                playing = False
                break
        
    again = ''
    while again not in ['Y','N']:
        again = input('Would you like to play again? Y or N?')
    if again == 'N':
        print(f'Thanks for playing {player.name}! Your final balance is {player.balance}')
        playing = False
        break
    else:
        pass


