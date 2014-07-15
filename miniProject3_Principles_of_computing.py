"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 10    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.


def mc_trial(working_board, player):
    """
    Takes a given board state and plays the game to completion 
    with alternating player moves made at random - 
    each call to this function is used to run one trial
    """
    inturn = player
    game_over = 0
 
    while game_over == 0:
        
        # Check if win      
        if working_board.check_win() != None:
            game_over = 1
            #print working_board
            return

        # Check empty cells
        empty_cells = working_board.get_empty_squares()
        
        # Choose position and move
        turn_pos = random.choice(empty_cells)
        
        working_board.move(turn_pos[0],turn_pos[1],inturn)
        
         # Switch player
        inturn = provided.switch_player(inturn)

def mc_update_scores(score, board, player):
    """
    This function takes a grid of scores (a list of lists)
    a board from a completed game, and which player 
    the machine player is and scores the completed board.
    """

    # Set score board
    size = board.get_dim()
    
    # Initialise player_sign
    player_sign = 1
    
    # First check if outcome was a draw or who won:
    if board.check_win() == 4:
        # "It was a draw"
        for row in range(size):
            for col in range(size):
                score[row][col] += 0 
    else:
        if board.check_win() == player:
            player_sign = -1
      
        for row in range(size):
            for col in range(size):
                if board.square(row,col) == 1:
                    score[row][col] += 0
                elif board.square(row,col) == player:
                    score[row][col] -= player_sign*MCMATCH
                else:
                    score[row][col] += player_sign*MCOTHER    
            
    return

def get_best_move(board, scores):
    """
    The function should find all of the empty squares 
    with the maximum score and randomly return one of them 
    as a (row, column) tuple
    """
    values = []
    max_empty_squares = []
    
    # Find empty squares
    #print board
    empty_squares = board.get_empty_squares()
    #print "Empty squares: ", empty_squares
    
    # Extract values:
    for square in empty_squares:
        values.append(scores[square[0]][square[1]])

    # Find maximum, determine if unique
    max_value = max(values)
    
    if values.count(max_value) > 1:
        # there are more than one value so choose random
        for square in empty_squares:
            if scores[square[0]][square[1]] == max_value:
                max_empty_squares.append(square)
        best_move = random.choice(max_empty_squares)
    else:
        for square in empty_squares:
            if scores[square[0]][square[1]] == max_value:
                best_move = square
    return best_move

def mc_move(board, player, trials):
    """
    This function returns a move for the machine player 
    in the form of a (row, column) tuple
    """
    # Define board
    size = board.get_dim()
    
    # Initialise scores grid
    score = [[0 for dummy_row in range(size)] for dummy_col in range(size)] 
    
    # Loop through the various trials
    counter = 0
    
    while counter < trials:
    
        # Perform trial
        #print "Trial No: ", counter+1
        working_board = board.clone()
        mc_trial(working_board, player)

        # Update Score        
        mc_update_scores(score, working_board, player)
        
        # Increase counter
        counter = counter + 1

        # Select a move: check if board has empty squares
        
    if len(board.get_empty_squares()) >= 1:
        #print get_best_move(working_board,score)
        return get_best_move(board, score)
    else: 
        print "Error"
        

#provided.play_game(mc_move, 3, reverse = False)
