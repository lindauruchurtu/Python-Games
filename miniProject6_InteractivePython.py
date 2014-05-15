#------------------------------------------------------
# Mini-project #6 - Blackjack
#------------------------------------------------------

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
#------------------------------------------------------
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
        #print card_loc
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
#------------------------------------------------------
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        cards_str = "Hand contains"
        for card in self.cards:
            cards_str = cards_str + " " + str(card) 
        return cards_str

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        self.value = 0
        aces = 0
        
        for card in self.cards:
            self.value = self.value + VALUES[card.rank] # A value as 1
            if card.rank == 'A':
                aces = aces + 1
     
        if aces == 0:
            return self.value
        else:
            if self.value + 10 <= 21:
                return self.value + 10
            else:
                return self.value
                # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
                # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        self.pos = pos
        for card in self.cards:
            card.draw(canvas,self.pos)
            # then increment the x-value of the pos for the next card to be drawn
            self.pos[0] = self.pos[0] + 1.2*73
             
# define deck class 
#------------------------------------------------------
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                c = Card(suit, rank)
                self.deck.append(c)
                #self.deck = self.deck.append() 
                # create a Deck object

    def shuffle(self):
        random.shuffle(self.deck) 
        return self.deck

    def deal_card(self):
        card_dealt = random.choice(self.deck)
        self.deck.remove(card_dealt)
        return card_dealt
    # one could create some logic here so if a card
    # has already been handed, then do not give it again
    # or remove this card from the deck.
    
    def __str__(self):
        # return a string representation of the deck
        deck_str = "Deck contains"
        for card in self.deck:
            deck_str = deck_str + " " + str(card) 
        return deck_str

#define event handlers for buttons
#------------------------------------------------------

def deal():
    global outcome, in_play, game_deck, player_hand, dealer_hand, to_do, score
    
    #print "in_play: ", in_play
    
    outcome = ""
    if in_play == True:
        score = score - 1
        outcome = "You Lose"
        #print "You should lose"
        in_play = False
        to_do = "New deal?"
        return
        
    to_do = "Hit or Stand?"
        
    # your code goes here
    game_deck = Deck()
    game_deck.shuffle()
    # Create Player and Dealer Hands
    player_hand = Hand()
    dealer_hand = Hand()
   
    player_hand.add_card(game_deck.deal_card())
    player_hand.add_card(game_deck.deal_card())
    
    dealer_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())
    
    #It is easier to just repeat twice than to write loop
    
    print "The Player's", player_hand
    print "Player's hand value:", player_hand.get_value()
    print "The Dealer's", dealer_hand
    print "Dealer's hand value:", dealer_hand.get_value()
    
    in_play = True
    #print "in_play: ", in_play
    
def hit():
    global player_hand, outcome, in_play, score, to_do 
    
    # if the hand is in play, hit the player 
    if in_play == True:
        player_hand.add_card(game_deck.deal_card())
    
        if player_hand.get_value() <= 21:
            print "The Player's", player_hand
            print "Player's Hand value:", player_hand.get_value()
        else:
        # if busted, assign a message to outcome, update in_play and score
            print "You have busted"
            outcome = "You have busted"
            score = score - 1
            in_play = False
            to_do = "New deal?"
            #print "in_play: ", in_play
       
def stand():
    global player_hand, dealer_hand, outcome, in_play, score, to_do
        
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
    
        if player_hand.get_value() > 21:
            print "You have busted"
            outcome = "You have busted"
            score = score - 1
            to_do = "New deal?"
    
        while dealer_hand.get_value() <= 17:
            dealer_hand.add_card(game_deck.deal_card())
            print "The Dealer's", dealer_hand
            print "Dealer has now a hand value of:", dealer_hand.get_value()
    
    # assign a message to outcome, update in_play and score
   
        if dealer_hand.get_value() > 21:
            print "The Dealer is busted"
            outcome = "You win"
            score = score + 1
            in_play = False
            to_do = "New deal?"
            print "in_play: ", in_play
        elif player_hand.get_value() <= dealer_hand.get_value():
            print "The Dealer has won"
            outcome = "You Lose"
            score = score - 1
            in_play = False
            print "in_play: ", in_play
            to_do = "New deal?"
        else:
            print "You have won"
            outcome = "You win"
            score = score + 1
            in_play = False
            print "in_play: ", in_play
            to_do = "New deal?"
        
# draw handler    
def draw(canvas):
    global player_hand, dealer_hand
    # test to make sure that card.draw works, replace with your code below
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    
    player_hand.draw(canvas, [100, 400])
    dealer_hand.draw(canvas, [100, 150])
    
    # Draw back of the dealer's card when in_play = True
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 150 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
     
    # Title of Game written in Canvas
    canvas.draw_text("BLACKJACK", (180, 70), 45, 'Black')
    # Dealer Title
    canvas.draw_text("Dealer", (100, 120), 25, 'Black')
    # Player Title
    canvas.draw_text("Player", (100, 370), 25, 'Black')
    # Outcome Message
    canvas.draw_text(outcome, (300, 120), 25, 'Red')
    # Print score
    canvas.draw_text("Score: " + str(score), (360, 320), 25, 'Red')
    # Options Message
    canvas.draw_text(to_do, (360, 370), 25, "Blue")
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
#label = frame.add_label("Alive")
frame.set_draw_handler(draw)


# get things rolling
in_play = False
deal()
frame.start()


# remember to review the gradic rubric
