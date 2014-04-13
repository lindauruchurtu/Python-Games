# Rock-paper-scissors-lizard-Spock - Mini project 1
# --------------------------------------------------
#
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors
#
# -----------------------------------------------
# Helper functions
# -----------------------------------------------
# name_to_number(name)
# name_to_number maps the RPSLS input to a number
# -----------------------------------------------

def name_to_number(name):
    #if type(name) != str:
    #    print "Error - input is not a string"
    #    return
    name = name.lower()
    if name == "rock":
        num = 0
    elif name == "spock":
        num = 1
    elif name == "paper":
        num = 2
    elif name == "lizard":
        num = 3
    elif name == "scissors":
        num = 4
    else:
        print "Error: that is not a valid RPSLS input"
    return num	

#Test the function
#print name_to_number("lizard")

# --------------------------------------------------------------
# number_to_name(number)
# number_to_name maps a number between 0 and 4 to a RPSLS string
# --------------------------------------------------------------

def number_to_name(number):
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    else:
        print "Error: the input is a number outside the valid range of 0-4"
    return name	

#Test
#print number_to_name(4)

# -----------------------------------------------
# Main Controller
# -----------------------------------------------
def rpsls(player_choice): 
    # print a blank line to separate consecutive games
    print "\n"
    # print out the message for the player's choice
    print "Player chooses %s" % player_choice
    player_choice = player_choice.lower()
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    import random #import random module
    comp_number = random.randrange(0, 5, 1)
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out the message for computer's choice
    print "Computer chooses %s" % comp_choice
    # compute difference of comp_number and player_number modulo five
    diff = ( player_number - comp_number ) % 5
    # use if/elif/else to determine winner, print winner message
    if diff == 1 or diff == 2:
        print "Player wins!"
    elif diff == 0:
        print "Player and computer tie!"
    else:
        print "Computer wins!"
    
    
# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")


# always remember to check your completed program against the grading rubric
