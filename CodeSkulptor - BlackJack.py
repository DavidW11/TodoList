# Mini-project #6 - Blackjack


import simplegui
import random


# Global variables
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    


in_play = False
outcome = ""
score = 0


SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


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

        
class Hand: 
    def __init__(self):
        card_list = []
        self.card_list = card_list

    def __str__(self):
        list_string = ""
        for cards in range(len(self.card_list)):
            list_string += " " + str(self.card_list[cards])
        return list_string            

    def add_card(self, card):
        self.card_list.append(card)

    def get_value(self):
        value = 0
        for cards in self.card_list:
            value += VALUES[cards.rank  ] 
        for cards in self.card_list:
            if cards.rank == 'A' and value + 10 <= 21:
                value += 10
        return value

    def draw(self, canvas, pos):
        x = pos[0]
        for cards in self.card_list:
            cards.draw(canvas, (x,pos[1]))
            x += 102
            
        
class Deck:
    def __init__(self):
        deck = []
        for x in SUITS:
            for y in RANKS:
                card = Card(x, y)
                deck.append(card)
        self.deck = deck

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
            
    def __str__(self):
        deck_string = ""
        for cards in range(len(self.deck)):
            deck_string += " " + str(self.deck[cards])
        return deck_string


# Event handlers
def deal():
    global outcome, in_play, score
    global my_deck, my_hand, dealer_hand
    
    if in_play == True:
        outcome = "Dealer wins"
        score -= 1
    
    my_deck = Deck()
    my_hand = Hand()
    dealer_hand = Hand()
    my_deck.shuffle()
    
    dealer_hand.add_card(my_deck.deal_card())
    my_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    my_hand.add_card(my_deck.deal_card())
    
    in_play = True
    outcome = "Hit or Stand"

def hit():
    global outcome, in_play, score
    player_value = my_hand.get_value()
    if in_play == True:
        my_hand.add_card(my_deck.deal_card())
        player_value = my_hand.get_value()
        if player_value > 21:
            outcome = "You Busted and the Dealer Wins"
            in_play = False
            score -= 1
    else:
        outcome = "You Busted and the Dealer Wins, Game Over"

def stand():
    global outcome, in_play, score
    player_value = my_hand.get_value()
    if in_play == True:
        dealer_value = dealer_hand.get_value()
        while dealer_value <= 17:
            dealer_hand.add_card(my_deck.deal_card())
            dealer_value = dealer_hand.get_value()
        if dealer_value > 21:
            outcome = "The Dealer Busted, You Won"
            in_play = False
            score += 1
        elif player_value <= dealer_value:
            outcome = "The Dealer Wins"
            in_play = False
            score -= 1
        else:
            outcome = "You Won"
            in_play = False
            score += 1
    else:
        outcome = "You Busted and the Dealer Wins, Game Over"
        

# Draw handler    
def draw(canvas):
    global outcome, score
    global in_play, my_hand, dealer_hand
    canvas.draw_text(str(outcome), (400, 150), 21, 'Red')
    canvas.draw_text(str(score), (450, 50), 21, 'White')
    canvas.draw_text("Blackjack", (100,100), 33, 'Red')
    my_hand.draw(canvas, (50, 400))
    dealer_hand.draw(canvas, (50, 200))
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0],200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

                     
# Initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")


# Buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


#Start
deal()
frame.start()

