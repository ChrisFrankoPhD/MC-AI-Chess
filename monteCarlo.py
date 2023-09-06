"""
Monte Carlo chess module, plays a chess game with random move generation to find "optimal" moves
"""

import random
import chessClass as chessgame
import chessGui as chess_gui

DEPTH = 2
TRIALS = 10

def monte_carlo(board, team, depth, trials):
    """
    given a board state, team, move depth, and number of trials, runs the full monte carlo simulation for that state, and return a tuple representation of the optimal move 
    """
    move_list = board.get_all_moves(team)
    score_tracker = {move: [] for move in move_list}

    # apply all possible current moves for the current team, then call run_sim for the resulting board state of each of those moves. Builds a dictionary with keys of each possible move, and values of the average game score
    for move in score_tracker:
        clone_board = board.clone()
        clone_board.apply_move(move[0], move[1])
        score_tracker[move] = run_sim(clone_board, team, depth, trials)
    
    # return the move with either the minimum or maximum gamescore depending on if the current team is BLACK (min) or WHITE (max)
    if team == chessgame.BLACK:
        return min(score_tracker, key = lambda k: score_tracker[k])
    else:
        return max(score_tracker, key = lambda k: score_tracker[k])

def run_sim(board, team, depth, trials):
    """
    given a board state, team, move depth, and number of trials, runs "trials" number of monte carlo trials and returns an average gamescore as a number
    """
    results = []

    # call the run_trial function "trials" times, randomly simulating a chessgame, and appending the resulting gamescore to the results list
    for dummy_num in range(trials):
        clone_board = board.clone() 
        score = run_trial(clone_board, team, depth)
        results.append(score)

    # return the average result
    return sum(results) / len(results)

def run_trial(board, team, depth):
    """
    Given a board, a team, and a move depth, runs a single random trial to the depth, and returns the resulting game score as a number
    """
    starting_team = team
    team = team

    # make a number of random turns equal to double the depth, to give depth number of rounds, if there is a win during the trial, return a large gamescore
    for dummy_num in range(depth * 2):
        move = random.choice(board.get_all_moves(team))
        board.apply_move(move[0], move[1])
        team = chessgame.other_team(team)
        if board.check_win():
            if starting_team == chessgame.WHITE:
                return 15
            else:
                return -15
            
    # return the boards gamescore
    return board.get_score()

def play_game(depth, trials):
    """
    Play a full chess game with two MC players. Takes a very long time, order of 10 minutes for depth / trials > 3
    """
    # Setup game
    board = chessgame.ChessBoard()
    team = chessgame.WHITE
    winner = False
    
    # Run game until there is a win condition
    while not winner:
        # Move
        move = monte_carlo(board, team, depth, trials)
        board.apply_move(move[0], move[1])

        # Update state
        winner = board.check_win()
        team = chessgame.other_team(team)

        # Display board
        print (board)
        
    # Print winner
    if winner == chessgame.WHITE:
        print ("White wins!")
    elif winner == chessgame.BLACK:
        print ("Black wins!")
    elif winner == chessgame.DRAW:
        print ("StaleMate!")
    else:
        print ("Error: unknown winner")

# play_game(DEPTH, TRIALS)
chess_gui.run_gui(ai_function=monte_carlo, depth=DEPTH, trials=TRIALS)






