import chessClass as chess

class Pawn(ChessPiece):
    self._is_moved = False
    self._vectors = [(TEAM_SIDE[self.team], 0), (TEAM_SIDE[self.team], 1), (TEAM_SIDE[self.team], -1)]
    def get_possible_moves(self, board):
        pass    


class ChessPiece:
    '''
    class to represent the chess peices
    '''
    def __init__(self, team, tile):
        self.team = team
        self.tile = tile
            
    def __str__(self):
        return STRMAP[self.team] + STRMAP[self.rank] + str(self.tile)
    
    def get_possible_moves(self, board, is_clone = False):
        if self.rank == PAWN:
            p_vecs = [(TEAM_SIDE[self.team], 0), (TEAM_SIDE[self.team], 1), (TEAM_SIDE[self.team], -1)]
            p_moves = []
            #string = str(self.team) + "/ white = " + str(board.first_white) + "/ black = " + str(board.first_black)
            # if is_clone:
            #     string += " ::CLONE"
            #print string
            if (board.first_white == True and self.team == WHITE) or (board.first_black == True and self.team == BLACK):
                #print 'fuck this shit'
                p_vecs.append((TEAM_SIDE[self.team] * 2, 0))
                #print p_vecs
            for direc in p_vecs:
                for tile in traverse_grid(self.tile, direc, 1, board):
                    if direc == (TEAM_SIDE[self.team], 0) or direc == (TEAM_SIDE[self.team] * 2, 0):
                        if board._board[tile[0]][tile[1]] == EMPTY:
                            p_moves.append(tile)
#                            print STRMAP[self.team], STRMAP[self.rank], self.tile, p_moves 
                    else: 
                        if board._board[tile[0]][tile[1]] != EMPTY:
                            if board._board[tile[0]][tile[1]].get_team() != self.get_team():
                                p_moves.append(tile)
                        
        elif self.rank == ROOK:
            p_moves = []
            for tile in traverse_grid(self.tile, (0, 1), board.get_dim() - self.tile[1] - 1, board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (0, -1), self.tile[1], board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (1, 0), board.get_dim() - self.tile[0] - 1, board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (0, -1), self.tile[0], board):
                p_moves.append(tile)
                       
        elif self.rank == KNIGHT:
            n_vecs = [(2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2)]
            p_moves = []
            for direc in n_vecs:
                for tile in traverse_grid(self.tile, direc, 1, board):
                    p_moves.append(tile)
                    
        elif self.rank == BISHOP:
            p_moves = []
            for tile in traverse_grid(self.tile, (1, 1), 
                                        min([board.get_dim() - self.tile[0] - 1, 
                                         board.get_dim() - self.tile[1]  - 1]), board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (-1, -1), 
                                        min([self.tile[0], 
                                             self.tile[1]]), board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (1, -1), 
                                        min([board.get_dim() - self.tile[0] - 1, 
                                             self.tile[1]]), board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (-1, 1), 
                                        min([self.tile[0], 
                                            board.get_dim() - self.tile[1]]) - 1, board):
                p_moves.append(tile)
        elif self.rank == QUEEN:
            p_moves = []
            for tile in traverse_grid(self.tile, (0, 1), board.get_dim() - self.tile[1] - 1, board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (0, -1), self.tile[1], board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (1, 0), board.get_dim() - self.tile[0] - 1, board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (-1, 0), self.tile[0], board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (1, 1), 
                                        min([board.get_dim() - self.tile[0] - 1, 
                                         board.get_dim() - self.tile[1] - 1]), board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (-1, -1), 
                                        min([self.tile[0], 
                                             self.tile[1]]), board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (1, -1), 
                                        min([board.get_dim() - self.tile[0] - 1, 
                                             self.tile[1]]), board):
                p_moves.append(tile)
            for tile in traverse_grid(self.tile, (-1, 1), 
                                        min([self.tile[0], 
                                            board.get_dim() - self.tile[1] - 1]), board):
                p_moves.append(tile)
                
        elif self.rank == KING:
            k_vecs = [(-1, 0), (-1, 1), (0, 1), (1, 1), 
                      (1, 0), (1, -1), (0, -1), (-1, -1)]
            p_moves = []       
            for direc in k_vecs:
                for tile in traverse_grid(self.tile, direc, 1, board):
                    p_moves.append(tile)
#            print STRMAP[self.team], STRMAP[self.rank], self.tile, p_moves
        
        for move in list(p_moves):
            if board._board[move[0]][move[1]] != EMPTY:
                if self.same_team(board._board[move[0]][move[1]]):
                    p_moves.remove(move)
        return p_moves
    
    def is_legal_move(self, board, tile):
        for move in self.get_possible_moves(board):
            if tile == move:
                return True
        return False
    
    def is_legal_move2(self, board, tile):
        for move in self.moves_no_check(board):
            if tile == move:
                return True
        return False

    def moves_no_check(self, board):
        moves = self.get_possible_moves(board)
        #print "MNC"
        for move in list(moves):
            cloned = board.clone()
            clone_tile = self.tile
            #print 'shiiiit'
            cloned.apply_move(clone_tile, move, 
                              cloned._board[clone_tile[0]][clone_tile[1]], True)
            #print 'shiiiit'
            if cloned.is_check(self.team, True):
                moves.remove(move)
        self.get_possible_moves(board)
        return moves
    
    def same_team(self, piece):
        if self.team == piece.team:
            return True
        return False
    
    def clone(self):
        return ChessPiece(self.rank, self.team, self.tile)
            
    def move(self, tile):
        self.tile = tile
    
    def get_team(self):
        return self.team
    
    def get_tile(self):
        return self.tile
    
    def get_rank(self):
        return self.rank
    
def traverse_grid(start_cell, direction, num_steps, board):
    """
    Function that iterates through the cells in a grid
    in a linear direction, until another ChessPiece is encountered
    """
    tiles = []
    for step in range(1, num_steps + 1):
        row = start_cell[0] + step * direction[0]
        col = start_cell[1] + step * direction[1]
        if (row < 0) or (row > 7) or (col < 0) or (col > 7):
            break 
        elif board._board[row][col] != EMPTY:
            tiles.append((row, col))
            break
        tiles.append((row, col))
#        print "Processing cell", (row, col), 
#        print "with value", EXAMPLE_GRID[row][col]
    return tiles