import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import chessClass as chessgame

GUI_WIDTH = 500
GUI_HEIGHT = GUI_WIDTH
BAR_WIDTH = 5

class ChessGUI:
    """
    GUI class for chess game itself
    """
    
    def __init__(self, size, aifunction=None, depth=None, trials=None):
        # Game board
        self._size = size
        self._bar_spacing = GUI_WIDTH // self._size
        self._pause = False

        # Icons hosted online, much slower to lad them this way
        # self._icons_url = {
        #     "bpa": simplegui.load_image("https://i.ibb.co/tz9VMKw/pawn-black.png"),
        #     "wpa": simplegui.load_image("https://i.ibb.co/CQmP98r/pawn-white.png"),
        #     "bqu": simplegui.load_image("https://i.ibb.co/ZcyFRn8/queen-black.png"),
        #     "wqu": simplegui.load_image("https://i.ibb.co/W2tfsrH/queen-white.png"),
        #     "bki": simplegui.load_image("https://i.ibb.co/nBQfxMw/king-black.png"),
        #     "wki": simplegui.load_image("https://i.ibb.co/YpkprNm/king-white.png"),
        #     "bro": simplegui.load_image("https://i.ibb.co/vw14yd6/rook-black.png"),
        #     "wro": simplegui.load_image("https://i.ibb.co/T825dmc/rook-white.png"),
        #     "bbi": simplegui.load_image("https://i.ibb.co/VSVW3nY/bishop-black.png"),
        #     "wbi": simplegui.load_image("https://i.ibb.co/HzdHxp5/bishop-white.png"),
        #     "bkn": simplegui.load_image("https://i.ibb.co/pz3SSSQ/knight-black.png"),
        #     "wkn": simplegui.load_image("https://i.ibb.co/7KYPh7z/knight-white.png")
        #                }
        # Icons hosted locally, preferable
        self._icons = { 
            chessgame.WHITE: {
                chessgame.PAWN: simplegui._load_local_image("./images/pawn-white.png"),
                chessgame.QUEEN: simplegui._load_local_image("./images/queen-white.png"),
                chessgame.KING: simplegui._load_local_image("./images/king-white.png"),
                chessgame.ROOK: simplegui._load_local_image("./images/rook-white.png"),
                chessgame.BISHOP: simplegui._load_local_image("./images/bishop-white.png"),
                chessgame.KNIGHT: simplegui._load_local_image("./images/knight-white.png")
            },
            chessgame.BLACK: {
                chessgame.PAWN: simplegui._load_local_image("./images/pawn-black.png"),
                chessgame.QUEEN: simplegui._load_local_image("./images/queen-black.png"),
                chessgame.KING: simplegui._load_local_image("./images/king-black.png"),
                chessgame.ROOK: simplegui._load_local_image("./images/rook-black.png"),
                chessgame.BISHOP: simplegui._load_local_image("./images/bishop-black.png"),
                chessgame.KNIGHT: simplegui._load_local_image("./images/knight-black.png")
            }
        }

        # AI setup
        self._aifunction = aifunction
        self._trials = trials
        self._depth = depth
        self._ai_go = False
        
        self.setup_frame()

        # Start new game
        self.newgame()
        
    def setup_frame(self):
        """
        Create GUI frame and add event handlers.
        """
        self._frame = simplegui.create_frame("Chess", GUI_WIDTH, GUI_HEIGHT)
        self._frame.set_canvas_background('White')
        
        # Set handlers
        self._frame.set_draw_handler(self.draw)
        self._frame.set_mouseclick_handler(self.click)
        self._frame.add_button("New Game", self.newgame)
        self._frame.add_button("Print Score", self.score)
        self._label = self._frame.add_label("")

    def start(self):
        """
        Start the GUI.
        """
        self._frame.start()

    def score(self):
        """
        Handler for the print score button, which just prints the current game score
        """
        print(self._board.get_score())

    def newgame(self):
        """
        Start new game.
        """
        self._board = chessgame.ChessBoard()
        self._game = chessgame.GameMaster()
        self._label.set_text("")
        self.picked_up = []
        self._ai_go = False
               
    def draw(self, canvas):
        """
        Continuously updates the chess board GUI.
        """

        # Draw the chess grid
        for bar_start in range(self._bar_spacing, GUI_WIDTH - 1, self._bar_spacing):
            canvas.draw_line((bar_start, 0), (bar_start, GUI_HEIGHT), BAR_WIDTH, 'Black')
            canvas.draw_line((0, bar_start), (GUI_WIDTH, bar_start), BAR_WIDTH, 'Black')

        # Draw each of the chess pieces themselves
        for row in range(self._size):
            for col in range(self._size):
                if self._board.get_square(row, col) != chessgame.EMPTY:
                    coords = self.get_coords_from_grid(row, col)
                    team = self._board.get_square(row, col).get_team()
                    rank = self._board.get_square(row, col).get_rank()
                    canvas.draw_image(self._icons.get(team).get(rank), (34, 34), (68,68), coords, (self._bar_spacing, self._bar_spacing))
        
        # if olding a piece, draw the allowed moves for that piece
        if self._game.get_state() == self._game.HOLD:
            held_piece = self._game.get_picked_up()
            held_piece_position = self._board.get_position(held_piece)
            moves = self._board.get_legal_moves(held_piece_position)
            for move in moves:
                coords = self.get_coords_from_grid(move[0], move[1])
                canvas.draw_polygon([
                    (coords[0] - (self._bar_spacing // 2), coords[1] - (self._bar_spacing // 2) ),
                    (coords[0] + (self._bar_spacing // 2), coords[1] - (self._bar_spacing // 2) ),
                    (coords[0] + (self._bar_spacing // 2), coords[1] + (self._bar_spacing // 2) ),
                    (coords[0] - (self._bar_spacing // 2), coords[1] + (self._bar_spacing // 2) )
                    ], 5, "#65fa9120")

        # if we are in an AI game state, sets an ai flag to True, on the next call, since the flag is True, we will then use the AI to simulate the best move, and then set the AI flag to False, and change the turn back to the player, and set the state back to CHOOSE
        if self._game.get_state() == self._game.AI:
            if self._ai_go:
                print ("Calulating Optimal Move...")
                ai_move = self._aifunction(self._board, self._game.get_turn(), self._depth, self._trials)
                print ("AI Move:")
                print (self._board.apply_move(ai_move[0], ai_move[1]))
                self._game.change_turn()
                self._game.state_choose()
                self._ai_go = False
            else:
                self._ai_go = True

    def click(self, position):
        """
        Click handler for the chessboard, handles all of the actual move functionality for the human player
        """        
        player = self._game.get_turn()
        state = self._game.get_state()
        clicked_tile = self.get_grid_from_coords(position)     

        # if we are in the CHOOSE state, then pick up the chosen piece and find the possible legal moves for that piece
        if state == self._game.CHOOSE:
            piece = self._board.get_square(clicked_tile[0], clicked_tile[1])
            piece_position = self._board.get_position(piece)

            if piece == chessgame.EMPTY:
                print("empty square")
                return
            elif piece.get_team() != player:
                print("not your team!")
                return
            elif piece.get_team() == player:
                self._game.pick_up(piece)
                print (f"Holding: {str(piece)} - {piece_position}")
                print (f"Legal Moves: {str(self._board.get_legal_moves(piece_position))}")
                return
            else:
                print("error, please re-choose")
                return
            
        # if we are in the HOLD state, and holding a piece, then the click corresponds to making an action, or putting down the held piece, execute the action and make the move on the chessboard object
        elif state == self._game.HOLD:
            held_piece = self._game.get_picked_up()
            held_piece_position = self._board.get_position(held_piece)
            held_moves = self._board.get_legal_moves(held_piece_position)

            if clicked_tile == held_piece_position:
                self._game.put_down()
            elif clicked_tile in held_moves:
                print (f"Your Move:")
                print (self._board.apply_move(held_piece_position, clicked_tile))
                self._game.put_down()
                self._game.change_turn()

                # after we make our turn, if we are playing against AI, set the game state to AI
                if self._aifunction:
                    self._game.state_ai()
            else:
                print ("not a legal move")
                return
        
        elif state == self._game.AI:
            print ("AI Still Simulating")
            return
        
        else:
            print ('click "new game" to play!')
            return
        
        # if the made move results in a check, print to the console
        if self._board.is_check(chessgame.other_team(player)):
            print ("check!")
        
        # check if a winning condition has been reached, call the game over function which moves the game state to OVER
        winner = self._board.check_win()
        if winner:
            self.game_over(winner)
        else:
            return   
            
    def game_over(self, winner):
        """
        takes a game winner and congratulates them, and sets the game state to OVER
        """ 
        # Display winner
        if winner == chessgame.WHITE:
            print ("WHITE Wins!")
        elif winner == chessgame.BLACK:
            print ("BLACK Wins!")
        else:
            print ("StaleMate!")

        self._game.state_over()

    def get_coords_from_grid(self, row, col):
        """
        Given a grid square in the form (row, col), returns the coordinates on the canvas of the center of that square.
        """
        return (self._bar_spacing * (col + 1.0/2.0),
                self._bar_spacing * (row + 1.0/2.0))
    
    def get_grid_from_coords(self, position):
        """
        Given coordinates on canvas, gets the corresponding grid square indices.
        """
        posx, posy = position
        return (posy // self._bar_spacing,
                posx // self._bar_spacing)

def run_gui(board_size, ai_function=None, depth=None, trials=None):
    """
    Make a GUI object and run the game!
    """
    gui = ChessGUI(board_size, ai_function, depth, trials)
    gui.start()

# run_gui = ChessGUI(8)
# gui.start()
