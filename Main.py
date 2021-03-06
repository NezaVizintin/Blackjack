# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = {"wins": 0, "loses": 0}
dealer_hand = ""
player_hand = ""
deck = ""
last_card = ""
active_text = ""
value_colour_dealer = ""
value_colour_player = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# helper functions
def deal_cards(person, number):
    for add_card in range(number):
        person.add_card(deck.deal_card())

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        s = ""
        for card in self.hand:
            s += str(card) + " "
        return s

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        value = 0
        aces = False
        for card in self.hand:
            value += VALUES[card.get_rank()]
            if card.get_rank() == "A":
                aces = True
         
        if aces and value + 10 <= 21:
            value += 10
        return value   

    def draw(self, canvas, pos):
        for card in self.hand:
            pos = [pos[0] + 5 + CARD_SIZE[0], pos[1]]
            card.draw(canvas, pos)
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        dealt_card = self.deck.pop()
        return dealt_card
        
    def __str__(self):
        s = "Deck: "
        for card in self.deck:
            s += str(card) + " "
        return s


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, last_card, active_text
    active_text = "Hit or stand?"    
    dealer_hand = Hand()
    player_hand = Hand()
    deck = Deck()
    last_card = ""
    
    if in_play:
        score["loses"] += 1
        active_text = "You lose!"
        
    deck.shuffle()
    deal_cards(player_hand, 2)
    deal_cards(dealer_hand, 2)
    
    in_play = True

def hit():
    global in_play, active_text, score
    active_text = "Hit or stand?"
    if in_play:
        card = deck.deal_card()
        player_hand.add_card(card)
        if player_hand.get_value() > 21:
            in_play = False
            active_text = "BUSTED! Sorry, you loose :("
            score["loses"] += 1
    else:
        active_text = "Press DEAL for another game"
       
def stand():
    global in_play, active_text, score
    active_text = "Hit or stand?"
    if in_play:
        while dealer_hand.get_value() < 17:
            deal_cards(dealer_hand, 1)
        if dealer_hand.get_value() > 21:
            in_play = False
            active_text = "Dealer busted! You win!"
            score["wins"] += 1
    else:
        active_text = "Press DEAL for another game"
    
    if in_play:
        if player_hand.get_value() > dealer_hand.get_value():
            active_text = "YAY! You win!"
            score["wins"] += 1
            in_play = False
        else:
            active_text = "Sorry, you loose :("
            score["loses"] += 1
            in_play = False    

# draw handler    
def draw(canvas):
    if player_hand.get_value() <= 21:
        value_colour_player = "Green"
    else:
        value_colour_player = "Red"
        
    if dealer_hand.get_value() <= 21:
        value_colour_dealer = "Green"
    else:
        value_colour_dealer = "Red"
    
    dealer_hand.draw(canvas, [CARD_SIZE[0] * 0.5, CARD_SIZE[1]])
    player_hand.draw(canvas, [CARD_SIZE[0] * 0.5, CARD_SIZE[1] * 2.5])
    canvas.draw_text('BLACKJACK', (200, 60), 40, 'Black')
    canvas.draw_text(active_text, (200, 450), 30, 'Black')
    canvas.draw_text("Score: "  + str(score["wins"]) + "/" + str(score["loses"]), (200, 500), 30, 'Black')
    canvas.draw_circle((51, CARD_SIZE[1] * 3 - 7), 15, 12, 'White', 'White')
    canvas.draw_text(str(player_hand.get_value()), (40, CARD_SIZE[1] * 3), 22, value_colour_player)
    
    if not in_play:
        canvas.draw_circle((51, CARD_SIZE[1] * 1.5 - 7), 15, 12, 'White', 'White')
        canvas.draw_text(str(dealer_hand.get_value()), (40, CARD_SIZE[1] * 1.5), 22, value_colour_dealer)
    
    if in_play:
        canvas.draw_image(card_back, (CARD_SIZE[0]/2, CARD_SIZE[1]/2), (CARD_SIZE[0], CARD_SIZE[1]), [CARD_SIZE[0] * 2.06, CARD_SIZE[1] * 1.5], (CARD_SIZE[0], CARD_SIZE[1]))

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
