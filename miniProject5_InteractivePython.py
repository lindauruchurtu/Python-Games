# ------------------------------------------
# Mini Project 5 - Memory
# ------------------------------------------

import simplegui
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 100
CARD_WIDTH = 800 // 16


turns = 0

# helper function to initialize globals
def new_game():
    global numbers, state, first_card, second_card, exposed, turns
    first_card = 0
    second_card = 0
    state = 0
    turns = 0
    label.set_text("Turns = " + str(turns))
    numbers = range(8) + range(8)
    random.shuffle(numbers)
    exposed = [False] * 16
   
    
     
# define event handlers
def mouseclick(pos):
    global exposed, state, first_card, second_card, turns

    # determine which card it corresponds and print to console
    i = pos[0] / CARD_WIDTH
    #print i
    # game logic
    if state == 0:
        if exposed[i] == False:
            exposed[i] = True  
        state = 1
        first_card = i
        second_card = 0
    elif state == 1:
        if exposed[i] == False:
            exposed[i] = True 
            state = 2
            second_card = i
            
    elif state == 2:
        turns = turns + 1
        label.set_text("Turns = " + str(turns))
        #print turns
        if (numbers[first_card] == numbers[second_card]):
            exposed[first_card] = True
            exposed[second_card] = True
            first_card = i
            exposed[i] = True
            state = 1
        else:
            exposed[first_card] = False
            exposed[second_card] = False
            exposed[i] = True
            state = 1
            first_card = i
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global numbers, exposed
    x_coord = 0
    for i in range(len(numbers)):
        canvas.draw_text(str(numbers[i]), (10 + x_coord, 0.65 * CANVAS_HEIGHT), 55, 'White')
        x_coord = x_coord + CARD_WIDTH
        if exposed[i] == False:
            #print i
            point = [(i*CARD_WIDTH, 0), (i*CARD_WIDTH, CANVAS_HEIGHT), (i*CARD_WIDTH + CARD_WIDTH, CANVAS_HEIGHT), (i*CARD_WIDTH + CARD_WIDTH, 0) ]
            canvas.draw_polygon(point, 1, "White", "Green")
        else:
            point = [(i*CARD_WIDTH, 0), (i*CARD_WIDTH, CANVAS_HEIGHT), (i*CARD_WIDTH + CARD_WIDTH, CANVAS_HEIGHT), (i*CARD_WIDTH + CARD_WIDTH, 0) ]
            canvas.draw_polygon(point, 1, "White")
                    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


