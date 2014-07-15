"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """    
    result = {}
    if len(hand) == 0:
      print "Error"
      return 0

    for elem in hand:
        if elem not in result.keys():
            result[elem] = hand.count(elem)

    keys = result.keys()        

    for num in range(len(keys)):
        result[keys[num]] = keys[num]*result[keys[num]]
    
    return max(result.values())

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    # Generate all possible outcomes
    all_outcomes = gen_all_sequences(range(1,num_die_sides+1,1), num_free_dice)

    #print "My States: ", all_outcomes

    # Score all outcomes and build tuple of score and state
    master_list = []
    for state in all_outcomes:
    # each element is a tuple - build global states
        master_list.append((score(held_dice + state),held_dice + state))

    # Compute probability of each state
    prob = 1.0 / len(all_outcomes)

    # Compute expected value
    exp_value = 0
    for item in master_list:
        exp_value += item[0]*prob

    return exp_value

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    masks = gen_all_sequences([0,1],len(hand))

    all_states = []
    for num in masks:
        temp_item = []
        for index in range(0,len(num)):
            if num[index]==1:
                temp_item.append(hand[index])
        all_states.append(tuple(temp_item))  
    return set(all_states) 

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    # For the given hand, generate all possible holds:
    all_holds = gen_all_holds(hand)

    # Compute the expected value of each hold and save it in a list:
    expected = {}

    for hold in all_holds:
        expected[hold]=expected_value(hold, num_die_sides, len(hand)-len(hold))

    best_value = max(expected.values())
    
    for hold in expected.keys():
        if expected[hold]==best_value:
            return(best_value,hold)

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score = score(hand)
    hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()




