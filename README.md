# McChess

- Play chess against a Monte Carlo AI opponent, written in Python

## Contents

- [Description](#description)
- [Usage](#using-the-app)
    - [Human Vs Human](#human-vs-human)
    - [Human Vs Computer](#human-vs-computer)
    - [Computer Vs Computer](#computer-vs-computer)
- [Next Steps](#whats-next)
- [Credit](#credit)

## Description 

- This app is written purely in Python, it uses the "SimpleGUICS2Pygame" module to make a basic GUI for the chess game
- The entirety of the chess functionality is dealt with in chessClass.py, while the entirety of the GUI is dealt with in chessGui.py, the game can be played with two human players taking turns with just these two files
- the Monte Carlo AI simulation is dealt with in monteCarlo.py, run this file to start a chess game against the AI player

## Using the App

- there are two main functionalities to the app, playing chess as two human players, and playing chess against the AI, however we can also tell the AI to play a game against itself if we wish

    ### Human Vs Human

    - to play as two human players, simply uncomment the last line in the chessGui.py file (`run_gui = ChessGUI()`), and then run that file from the command line
    - this will use only the chessGui and chessClass files to run a game where you choose the inputs on the GUI for both players
    - game results and moves are logged in the console

    ### Human Vs Computer

    - to play as against the computer, ensure the last line in the chessGui.py file (`run_gui = ChessGUI()`) is commented out, and then run the monteCarlo file from the command line
    - by default this will run a chess game where the Monte Carlo simulation is run to a move depth of 3, with 3 trials each. This should take only a few seconds to decide the computers move
    - you may increase DEPTH, which is the number of turns past the current turn to simulate, or TRIALS, which is the number of simulations to run for each current possible move, by altering the global DEPTH and TRIALS constants at the top of the monteCarlo file. 
        - WARNING, this will very quickly increase the simulation time by the computer, on average at a depth of 5 and number of trials of 10, it takes about 25 seconds to decide the computers move on my laptop
        - I would like to blame this on the large number of possible moves in a chess game, but as always there are likely some inefficiencies to be improved upon

    ### Computer Vs Computer

    - we can also run a AI vs AI simulation that prints the game board in the console as the game progresses, no GUI is needed for this, we simply need to uncomment `play_game(DEPTH, TRIALS)` (second last line) in monteCarlo.py, while making sure to comment out the `chess_gui.run_gui(ai_function=monte_carlo, depth=DEPTH, trials=TRIALS)` (the last line). 
    - this will print the board state after each move into the console

## What's Next?

- In the broad scheme, I would like a similar program that uses PyTorch machine learning to make an AI, I did this as a first experience dealing with program flow and separating the AI/GUI/Chess functionality. (Note: I do not actually play chess at all, but the game is definitely complicated enough to make the project non-trivial) 

## Credit

- I learnt Python from the Fundamentals of Computing Specialization offered by RICE University on Coursera, it was a great course