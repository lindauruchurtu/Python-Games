# Mini Project 2 - "Guess the number" 
# ------------------------------------
#The first player thinks of a secret number in some known range while the second player attempts 
#to guess the number. After each guess, the first player answers either “Higher”, “Lower” or “Correct!” 
#depending on whether the secret number is higher, lower or equal to the guess.

import math
import random
import simplegui

# initialize global variables used in your code

user_number = 0
low = 0
high = 100
secret_number = 0
no_guesses = 7

# helper function to start and restart the game
def new_game():
    global secret_number, high, low
    print "New game. Range is from 0 to", high
    print ""
    secret_number = random.randrange(low, high)

# define event handlers for control panel

def range100():
    global high, no_guesses
    high = 100
    no_guesses = 7
    new_game()

def range1000():
    global high, no_guesses  
    high = 1000
    no_guesses = 10
    new_game()

def output(no_guesses):
    if (no_guesses>1):
        print "You have", no_guesses, "guesses left"
        print ""
    else:	
        print "You have one guess left"
        print ""
    
    
def input_guess(guess):
    global user_number, no_guesses
    user_number = int(guess)
    
    print "Guess was", guess
    
    if(no_guesses > 1):
        if(user_number > secret_number):
            print "Go lower"
            no_guesses = no_guesses - 1
            output(no_guesses)
        elif(user_number < secret_number):
            print "Go higher"
            no_guesses = no_guesses - 1
            output(no_guesses)
        else:
            print "You guessed right!"
            print "The secret number was", secret_number
            print ""
            new_game()
    else:
        print "You have ran out of guesses"
        print ""
        new_game()
    
# create frame

frame = simplegui.create_frame("Guess the number", 300, 300)

# register event handlers for control elements

frame.add_button("Range [0,100)",range100,200)
frame.add_button("Range [0,1000]",range1000,200)
frame.add_input("Enter guess:", input_guess, 200)

# call new_game and start frame
new_game()
frame.start()

