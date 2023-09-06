"""
Classes and constants needed to run the chessgame itself, technically no gui is needed here as all functionality for the chess mechanics is here
"""

# Constants
EMPTY = 0
PAWN = 1
ROOK = 2 
KNIGHT = 3
BISHOP = 4
QUEEN = 5
KING = 6
WHITE = 10 
BLACK = 20
DRAW = 15
CHOOSE = 95
HOLD = 96
PAUSE = 97

# here we can edit the front row order of pieces, if we want to make variant games for fun 
FRONT_ROW = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]

# Maping chess piece to strings for printing our nice representations of moves and such
STRMAP = {EMPTY: "   ", PAWN: "Pa", ROOK: "Ro",
         KNIGHT: "Kn", BISHOP: "Bi", QUEEN: "Qu", KING: "Ki", WHITE: "w", BLACK: "b"}
# Maping teams to constants for direction calculations
TEAM_SIDE = {BLACK: 1, WHITE: -1}


class ChessPiece:
    '''
    class to represent the chess pieces themselves, this is a parent class with shared methods, classes for each individual piece are below, and hold information on the types of moves they can make
    '''
    def __init__(self, team):
        self._team = team
    
    def get_rank(self):
        return self._rank
    
    def get_team(self):
        return self._team
    
    def get_value(self):
        if self.get_team() == WHITE:
            return self._value
        else: 
            return self._value * (-1)
    
    def is_legal_move(self, board, tile):
        for move in self.moves_no_check(board):
            if tile == move:
                return True
        return False
    
    def same_team(self, piece):
        if self._team == piece._team:
            return True
        return False
    
class Pawn(ChessPiece):
    """
    class representation of the PAWN chesspiece
    """
    def __init__(self, team, is_moved=False):
        ChessPiece.__init__(self, team)
        # this is the only piece with the is_moved flag, since a pawn can move two spaces if it is its first move
        self._is_moved = is_moved
        self._vectors = [(TEAM_SIDE[self._team], 0), (TEAM_SIDE[self._team], 1), (TEAM_SIDE[self._team], -1)]
        if not self._is_moved:
            self._vectors.append((TEAM_SIDE[self._team] * 2, 0))
        self._rank = PAWN
        self._value = 1

    def __str__(self):
        return STRMAP[self._team] + STRMAP[PAWN]

    def clone(self):
        return Pawn(self._team, self._is_moved)

    def moved(self):
        if self._is_moved == False:
            self._is_moved = True
            self._vectors.pop()

    def get_moves(self, board, position):
        p_moves = []
        for direc in self._vectors:
            for tile in traverse_grid(position, direc, 1, board):
                target = board._board[tile[0]][tile[1]]
                if direc[1] == 0:
                    if target == EMPTY:
                        p_moves.append(tile)
                else: 
                    if (target != EMPTY) and (target.get_team() != self.get_team()):
                        p_moves.append(tile)
        return p_moves 

class Knight(ChessPiece):
    """
    class representation of the KNIGHT chesspiece
    """
    def __init__(self, team):
        ChessPiece.__init__(self, team)
        self._vectors = [(2, 1), (2, -1), (-2, 1), (-2, -1), (-1, -2), (1, -2), (-1, 2), (1, 2)]
        self._rank = KNIGHT
        self._value = 3

    def __str__(self):
        return STRMAP[self._team] + STRMAP[KNIGHT]
    
    def clone(self):
        return Knight(self._team)
    
    def get_moves(self, board, position):
        p_moves = []
        for direc in self._vectors:
            for tile in traverse_grid(position, direc, 1, board):
                if (board._board[tile[0]][tile[1]] == EMPTY) or (board._board[tile[0]][tile[1]].get_team() != self.get_team()):
                    p_moves.append(tile)
        return p_moves 

class Bishop(ChessPiece):
    """
    class representation of the BISHOP chesspiece
    """
    def __init__(self, team):
        ChessPiece.__init__(self, team)
        self._vectors = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        self._rank = BISHOP
        self._value = 3

    def __str__(self):
        return STRMAP[self._team] + STRMAP[BISHOP]
    
    def clone(self):
        return Bishop(self._team)
    
    def get_moves(self, board, position):
        p_moves = []
        for direc in self._vectors:
            for tile in traverse_grid(position, direc, 7, board):
                target = board._board[tile[0]][tile[1]]
                if (target == EMPTY) or (target.get_team() != self.get_team()):
                    p_moves.append(tile)
        return p_moves 

class Rook(ChessPiece):
    """
    class representation of the ROOK chesspiece
    """
    def __init__(self, team):
        ChessPiece.__init__(self, team)
        self._vectors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self._rank = ROOK
        self._value = 5
    
    def __str__(self):
        return STRMAP[self._team] + STRMAP[ROOK]

    def clone(self):
        return Rook(self._team)
    
    def get_moves(self, board, position):
        p_moves = []
        for direc in self._vectors:
            for tile in traverse_grid(position, direc, 7, board):
                if (board._board[tile[0]][tile[1]] == EMPTY) or (board._board[tile[0]][tile[1]].get_team() != self.get_team()):
                    p_moves.append(tile)
        return p_moves 

class Queen(ChessPiece):
    """
    class representation of the QUEEN chesspiece
    """
    def __init__(self, team):
        ChessPiece.__init__(self, team)
        self._vectors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        self._rank = QUEEN
        self._value = 9

    def __str__(self):
        return STRMAP[self._team] + STRMAP[QUEEN]

    def clone(self):
        return Queen(self._team)
      
    def get_moves(self, board, position):
        p_moves = []
        for direc in self._vectors:
            for tile in traverse_grid(position, direc, 7, board):
                if (board._board[tile[0]][tile[1]] == EMPTY) or (board._board[tile[0]][tile[1]].get_team() != self.get_team()):
                    p_moves.append(tile)
        return set(p_moves)

class King(ChessPiece):
    """
    class representation of the KING chesspiece
    """
    def __init__(self, team):
        ChessPiece.__init__(self, team)
        self._vectors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        self._rank = KING
        self._value = 0

    def __str__(self):
        return STRMAP[self._team] + STRMAP[KING]

    def clone(self):
        return King(self._team)
          
    def get_moves(self, board, position):
        p_moves = []
        for direc in self._vectors:
            for tile in traverse_grid(position, direc, 1, board):
                if (board._board[tile[0]][tile[1]] == EMPTY) or (board._board[tile[0]][tile[1]].get_team() != self.get_team()):
                    p_moves.append(tile)
        return p_moves

class Empty(ChessPiece):
    def __init__(self, team, tile):
        ChessPiece.__init__(team, tile)
        self._vectors = []
        self._rank = EMPTY



class ChessBoard:
    """
    Class to represent a Chess board, the chessboard deals with all the interactions between pieces, and the location of the pieces themselves. The only place where a piece location is stored is on the board itself, so that there is a single source of truth.
    """

    def __init__(self, board = None, dead_pieces = None):
        """
        Initialize the chessboard object with the given dimension and 
        whether or not the game should be reversed.
        """
        self._dim = 8
        self.dead_pieces = []
        self.team_black = []
        self.team_white = []
        self._score = 0

        if board == None:
            # Create empty board
            self._board = [[EMPTY for dummycol in range(self._dim)] 
                           for dummyrow in range(self._dim)]
            #fill board with pawns piece
            for col in range(self._dim):
                # add pawn to tile, then append piece to team list, once for black then for white
                self._board[1][col] = Pawn(BLACK)
                self.team_black.append(self._board[1][col])
                
                self._board[self._dim - 2][col] = Pawn(WHITE)
                self.team_white.append(self._board[self._dim - 2][col])

            for col in range(self._dim):
                if FRONT_ROW[col] == ROOK:
                    # add rook to tile, then append piece to team list, once for black then for white
                    self._board[0][col] = Rook(BLACK)
                    self.team_black.append(self._board[0][col])

                    self._board[self._dim - 1][col] = Rook(WHITE)
                    self.team_white.append(self._board[self._dim - 1][col])

                if FRONT_ROW[col] == BISHOP:
                    # add bishop to tile, then append piece to team list, once for black then for white
                    self._board[0][col] = Bishop(BLACK)
                    self.team_black.append(self._board[0][col])

                    self._board[self._dim - 1][col] = Bishop(WHITE)
                    self.team_white.append(self._board[self._dim - 1][col])

                if FRONT_ROW[col] == KNIGHT:
                    # add knight to tile, then append piece to team list, once for black then for white
                    self._board[0][col] = Knight(BLACK)
                    self.team_black.append(self._board[0][col])

                    self._board[self._dim - 1][col] = Knight(WHITE)
                    self.team_white.append(self._board[self._dim - 1][col])

                if FRONT_ROW[col] == KING:
                    # add king to tile, then append piece to team list, once for black then for white
                    self._board[0][col] = King(BLACK)
                    self.team_black.append(self._board[0][col])

                    self._board[self._dim - 1][col] = King(WHITE)
                    self.team_white.append(self._board[self._dim - 1][col])

                if FRONT_ROW[col] == QUEEN:
                    # add queen to tile, then append piece to team list, once for black then for white
                    self._board[0][col] = Queen(BLACK)
                    self.team_black.append(self._board[0][col])

                    self._board[self._dim - 1][col] = Queen(WHITE)
                    self.team_white.append(self._board[self._dim - 1][col])


        else:
            # if we are given a chessboard to make a clone of, then we fill our new board with cloned chess pieces int he appropriate locations
            self._board = [[EMPTY for row in range(len(board))] for col in range(len(board))]
            for row in range(len(board)):
                for col in range(len(board)):
                    if board[row][col] != EMPTY:
                        piece = board[row][col].clone()
                        self._board[row][col] = piece
                        if piece.get_team() == WHITE:
                            self.team_white.append(piece)
                        else:
                            self.team_black.append(piece)

            self.dead_pieces = [dead_pieces[idx] for idx in range(len(dead_pieces))]
           
    def __str__(self):
        """
        Build a string representation of the chessboard.
        """
        rep = ""
        for row in range(self._dim):
            for col in range(self._dim):
                piece = self._board[row][col]
                if piece == EMPTY:
                    rep += STRMAP[piece]
                else:
                    rep += str(piece)
                if col == self._dim - 1:
                    rep += "\n"
                else:
                    rep += " | "
            if row != self._dim - 1:
                rep += "-" * (6 * self._dim - 3)
                rep += "\n"
        return rep

    def get_dead_str(self):
        """
        string representation of the dead pieces list.
        """
        dead_str = "dead: "
        for piece in self.dead_pieces:
            dead_str += str(piece) + ", "
        return dead_str
    
    def get_white_str(self):
        """
        string representation of the white pieces list.
        """
        white_str = "white: "
        for piece in self.team_white:
            white_str += str(piece) + ", "
        return white_str

    def get_black_str(self):
        """
        string representation of the black pieces list.
        """
        black_str = "black: "
        for piece in self.team_black:
            black_str += str(piece) + ", "
        return black_str
    
    def get_team_list(self, team):
        """
        return a teams given team list.
        """
        if team == WHITE:
            return self.team_white
        else:
            return self.team_black
        
    def get_square(self, row, col):
        """
        Returns either EMPTY, or a ChessPiece object at position (row, col) of the board.
        """
        if (0 <= row < self._dim) or (0 <= col < self._dim):
            return self._board[row][col]
        else:
            print("index out of board dimensions")
            return
        
    def get_position(self, piece):
        """
        Given a chess piece object, return the position of that object on the board.
        """
        row = None
        col = None
        for idx, value in enumerate(self._board):
            if piece in value:
                row = idx
                col = value.index(piece)
                break
        return (row, col)         

    def get_dim(self):
        """
        Return the dimension of the board.
        """
        return self._dim

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """
        empty = []
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] == EMPTY:
                    empty.append((row, col))
        return empty
    
    def get_score(self):
        """
        Return the current game score of the board
        """
        score = 0 
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] != EMPTY:
                    score += self._board[row][col].get_value()
        return score


    def get_legal_moves(self, org_tile):
        """
        Return a list all legal moves for a piece at a given tile
        """
        held_piece = self._board[org_tile[0]][org_tile[1]]
        legal_moves = held_piece.get_moves(self, self.get_position(held_piece))
        for move in list(legal_moves):
            clone_board = self.clone()
            clone_board.apply_move(org_tile, move)
            if clone_board.is_check(held_piece.get_team()):
                legal_moves.remove(move)
        return set(legal_moves)

    def remove_piece(self, piece):
        """
        Given a piece, remove that piece from its team list
        """
        team = piece.get_team()
        if team == WHITE:
            self.team_white.remove(piece)
        else:
            self.team_black.remove(piece)

    def apply_move(self, org_tile, end_tile):
        """
        Given a coordinate for a piece, and a target coordinate, do all action needed to move the piece from the initial to target coordinate on the board. 
        """
        held_piece = self._board[org_tile[0]][org_tile[1]]
        string = (f"MOVE: {STRMAP[held_piece.get_team()]}{STRMAP[held_piece.get_rank()]} {str(org_tile)} --> {str(end_tile)}")

        # if the target square holds an enemy piece, "kill" that piece   
        if self._board[end_tile[0]][end_tile[1]] != EMPTY:
            self.dead_pieces.append(self._board[end_tile[0]][end_tile[1]])
            self.remove_piece(self._board[end_tile[0]][end_tile[1]])

        self._board[end_tile[0]][end_tile[1]] = held_piece
        self._board[org_tile[0]][org_tile[1]] = EMPTY
        
        # if the moved piece was a pawn, set the moved flag to True
        if held_piece.get_rank() == PAWN:
            held_piece.moved()

        return string
    
    def is_check(self, team):
        """
        check if the given team is in check, returning either True or False
        """
        if team == WHITE:
            for piece in self.team_black:
                for move in piece.get_moves(self, self.get_position(piece)):
                    if self._board[move[0]][move[1]] != EMPTY:
                        if self._board[move[0]][move[1]].get_rank() == KING:
                            return True
        if team == BLACK:
            for piece in self.team_white:
                for move in piece.get_moves(self, self.get_position(piece)):
                    if self._board[move[0]][move[1]] != EMPTY:
                        if self._board[move[0]][move[1]].get_rank() == KING:
                            return True
        return False
    
    def is_stale(self, team):
        """
        check if the given team is stale, meaning if they can make no moves without putting themselves in check, returning either True or False
        """
        roster = self.get_team_list(team)
        for piece in roster:
            position = self.get_position(piece)
            for move in self.get_legal_moves(position):
                clone_board = self.clone()
                clone_board.apply_move(position, move)
                if clone_board.is_check(piece.get_team()) == False:
                    return False
        return True
    
    def check_win(self, mc = False):
        """
        check the current win state of the board, 
            returns False if game is undecided, 
            returns WHITE if white team has won,
            returns BLACK if black team has won,
            returns DRAW if there is a stalemate
        """
        
        if self.is_stale(WHITE):
            if self.is_check(WHITE):
                return BLACK
            else:
                return DRAW
        elif self.is_stale(BLACK):
            if self.is_check(BLACK):
                return WHITE
            else:
                return DRAW
        else:
            return False
    
    def get_all_moves(self, team):
        """
        given a team, returns all possible moves that team could make
        """
        if team == WHITE:
            team_list = self.team_white
        else:
            team_list = self.team_black
        moves = []
        moves_str = ""
        for piece in team_list:
            position = self.get_position(piece)
            for move in self.get_legal_moves(position):
                moves.append((position, move))
                moves_str += f"{str(piece)}{str(position)} --> {str(move)}, "
        return moves
        
    def clone(self):
        """
        Return a copy of the board.
        """
        return ChessBoard(self._board, self.dead_pieces)

class GameMaster:
    """
    Class for the game master, which deals with setting the state of the game, this could also be in the GUI, but I like the separation, and I believe it allows for more reusability of the GUI code
    """
    def __init__(self, turn=WHITE):
        """
        initialize the object, and the constants for the possible states
        """
        self._turn = turn
        self._state = CHOOSE
        self._picked_up = None

        self.CHOOSE = 95
        self.HOLD = 96
        self.PAUSE = 97
        self.OVER = 98
        self.AI = 99
    
    def get_turn(self):
        """
        return who's turn it currently is
        """
        return self._turn
    
    def get_state(self):
        """
        return the current state
        """
        return self._state

    def get_picked_up(self):
        """
        return the piece is currently "picked up", which a move is being chosen for
        """
        return self._picked_up
        
    def pick_up(self, piece):
        """
        pickup a specified piece, and set the game state to HOLD
        """
        self._picked_up = piece
        self._state = self.HOLD 

    def put_down(self):
        """
        put down whatever piece is being held, and set the game state to CHOOSE
        """
        self._picked_up = None
        self._state = self.CHOOSE 

    def change_turn(self):
        """
        change the turn state between players
        """
        if self._turn == WHITE:
            self._turn = BLACK
        else: 
            self._turn = WHITE

    def state_choose(self):
        """
        change the game state to CHOOSE
        """
        self._state = self.CHOOSE 
    def state_hold(self):
        """
        change the game state to HOLD
        """
        self._state = self.HOLD 
    def state_pause(self):
        """
        change the game state to PAUSE
        """
        self._state = self.PAUSE
    def state_ai(self):
        """
        change the game state to AI
        """
        self._state = self.AI
    def state_over(self):
        """
        change the game state to OVER
        """
        self._state = self.OVER


def traverse_grid(start_cell, direction, num_steps, board):
    """
    Iterates through the cells in a grid in a given linear direction (2D vector), until another ChessPiece is encountered, returns list all traversed tiles
    """
    tiles = []
    for step in range(1, num_steps + 1):
        row = start_cell[0] + step * direction[0]
        col = start_cell[1] + step * direction[1]
        if (row < 0) or (row > 7) or (col < 0) or (col > 7):
            return tiles 
        elif board._board[row][col] != EMPTY:
            tiles.append((row, col))
            return tiles
        tiles.append((row, col))
    return tiles
                       
def other_team(team):
    """
    given a team, returns the other team
    """
    if team == WHITE:
        return BLACK
    else:
        return WHITE

