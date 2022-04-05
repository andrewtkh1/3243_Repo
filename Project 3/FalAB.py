from math import inf


xAxis = "abcdefghijklmnopqrstuvwxyz"
### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.white_strategy = []
        self.black_strategy = []

    def move(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        copy = type(self)(self.x, self.y, self.color)
        return copy

    def insert_position(self, moves, board, pos):
        if board.is_coordinate_taken(pos):
            if board.is_there_enemy(pos, self.color):
                moves.append(pos)
            return False
        else:
            moves.append(pos)
            return True

class Knight(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.weight = 30
        self.black_strategy = [
            [-5.0, -4.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0,  0.0, -2.0, -4.0],
            [-3.0,  0.0,  2.0,  0.0, -3.0],
            [-4.0, -2.0,  0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -4.0, -5.0], 
        ]
        self.white_strategy = [
            [-5.0, -4.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0,  0.0, -2.0, -4.0],
            [-3.0,  0.0,  2.0,  0.0, -3.0],
            [-4.0, -2.0,  0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -4.0, -5.0], 
        ]

    def __str__(self):
        return "Knight"

    def valid_moves(self, board):
        moves = []
        x_offset = [1,-1,1,-1,2,-2,2,-2]
        y_offset = [2,2,-2,-2,1,1,-1,-1]
        for i in range(len(x_offset)):
            posX = x_offset[i] + self.x
            posY = y_offset[i] + self.y
            pos = (posX, posY)
            if board.is_valid_coordinate(pos, self.color):
                moves.append(pos)
        return moves

        
class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.weight = 50
        self.black_strategy = [
            [  0.0,  0.0,  0.0,  0.0,   0.0],
            [  0.5,  1.0,  1.0,  1.0,   0.5],
            [ -0.5,  0.0,  0.0,  0.0,  -0.5],
            [ -0.5,  0.0,  0.0,  0.0,  -0.5],
            [  0.0,  0.5,  0.5,  0.0,   0.0]
        ]
        self.white_strategy = [
            [  0.0,  0.5,  0.5,  0.0,   0.0],
            [ -0.5,  0.0,  0.0,  0.0,  -0.5],
            [ -0.5,  0.0,  0.0,  0.0,  -0.5],
            [  0.5,  1.0,  1.0,  1.0,   0.5],
            [  0.0,  0.0,  0.0,  0.0,   0.0],
        ]
    def __str__(self):
        return "Rook"

    def valid_moves(self, board):
        moves = []

        # Up, range(self.y+1, self.gridY, 1), if y = 2, then [3,4]
        for y in range(self.y+1, board.gridY, 1):
            pos = (self.x, y)
            if not self.insert_position(moves, board, pos):
                break

        # Down, range(self.y-1, -1, -1), if y = 3, then [2,1,0]
        for y in range(self.y-1, -1, -1):
            pos = (self.x, y)
            if not self.insert_position(moves, board, pos):
                break

        # Left, range(self.x-1, -1, -1), 
        for x in range(self.x-1, -1, -1):
            pos = (x, self.y)
            if not self.insert_position(moves, board, pos):
                break


        # Right
        for x in range(self.x+1, board.gridX, 1):
            pos = (x, self.y)
            if not self.insert_position(moves, board, pos):
                break

        return moves


class Bishop(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.weight = 30
        self.black_strategy = [
            [-2.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0, -1.0],
            [-1.0,  0.5,  1.0,  0.5, -1.0],
            [-1.0,  1.0,  1.0,  1.0, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -2.0]
        ]

        self.white_strategy = [
            [-2.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0,  1.0,  1.0,  1.0, -1.0],
            [-1.0,  0.5,  1.0,  0.5, -1.0],
            [-1.0,  0.0,  0.0,  0.0, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -2.0],
        ]
        
    def __str__(self):
        return "Bishop"

    def valid_moves(self, board):
        moves = []
        # diagonal top right logic
        x = self.x + 1
        y = self.y + 1
        while  0 <= (y) < board.gridY and 0 <= (x) < board.gridX:
            pos = (x, y)
            if not self.insert_position(moves, board, pos):
                break

            x += 1
            y += 1
        
        # diagonal top left logic
        x = self.x - 1
        y = self.y + 1
        while  0 <= (y) < board.gridY and 0 <= (x) < board.gridX:
            pos = (x, y)
            if not self.insert_position(moves, board, pos):
                break

            x -= 1
            y += 1

        # diagonal bottom left logic
        x = self.x - 1
        y = self.y - 1
        while  0 <= (y) < board.gridY and 0 <= (x) < board.gridX:
            pos = (x, y)
            if not self.insert_position(moves, board, pos):
                break

            x -= 1
            y -= 1
        
        # diagonal bottom right logic
        x = self.x + 1
        y = self.y - 1
        while  0 <= (y) < board.gridY and 0 <= (x) < board.gridX:
            pos = (x, y)
            if not self.insert_position(moves, board, pos):
                break

            x += 1
            y -= 1

        return moves

        
class Queen(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.weight = 90
        self.white_strategy = [
            [ -2.0, -1.0, -0.5, -1.0, -2.0],
            [ -1.0,  0.5,  0.5,  0.5, -1.0],
            [ -0.5,  0.5,  0.5,  0.5,  0.0],
            [ -1.0,  0.5,  0.5,  0.5, -1.0],
            [ -2.0, -1.0, -0.5, -1.0, -2.0]
        ]
        self.black_strategy = [
            [ -2.0, -1.0, -0.5, -1.0, -2.0],
            [ -1.0,  0.5,  0.5,  0.5, -1.0],
            [  0.0,  0.5,  0.5,  0.5, -0.5],
            [ -1.0,  0.5,  0.5,  0.5, -1.0],
            [ -2.0, -1.0, -0.5, -1.0, -2.0]
        ]
    def __str__(self):
        return "Queen"

    def valid_moves(self, board):
        # print("Queen valid_moves")
        # Queen's move set is Rook and Bishop combined
        moves = Rook.valid_moves(self, board) + Bishop.valid_moves(self, board)

        # print(f"Queen {moves}")
        return moves

class King(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.weight = 900
        self.white_strategy = [
            [ 2.0,  3.0,  1.0,  0.0,  0.0],
            [ 2.0,  2.0,  0.0,  0.0,  0.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0],
        ]
        self.black_strategy = [
            [-3.0, -4.0, -4.0, -5.0, -5.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0],
            [ 2.0,  2.0,  0.0,  0.0,  0.0],
            [ 2.0,  3.0,  1.0,  0.0,  0.0],
        ]
    def __str__(self):
        return "King"

    def valid_moves(self, board):
        moves = []
        x_offset = [ -1, 0,1,-1,1,-1,0,1 ]
        y_offset = [ -1,-1,-1,0,0,1,1,1 ]

        for i in range(len(x_offset)):
            posX = x_offset[i] + self.x
            posY = y_offset[i] + self.y
            pos = (posX, posY)
            if board.is_valid_coordinate(pos, self.color):
                moves.append(pos)

        return moves


class Pawn(Piece):
    #New Piece to be implemented
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.weight = 10
        self.black_strategy = [
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [5.0, 5.0, 5.0, 5.0, 5.0],
            [0.5, 0.25, 0.5, 1.875, 1.875],
            [0.5, 1.0, 1.0, -2.0, -2.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
        ]

        self.white_strategy = [
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 1.0, 1.0, -2.0, -2.0],
            [0.5, 0.25, 0.5, 1.875, 1.875],
            [5.0, 5.0, 5.0, 5.0, 5.0],
            [0.0, 0.0, 0.0, 0.0, 0.0], 
        ]

    def __str__(self):
        return "Pawn"

    def valid_moves(self, board):
        # print("Pawn valid_moves")
        moves = []
        forwardPos = (self.x, self.y-1)
        diagonalLeft = (self.x-1, self.y-1)
        diagonalRight = (self.x+1, self.y-1)
        if not board.is_black_player_turn:
            # Move forward if empty slot.
            forwardPos = (self.x, self.y+1)
            diagonalLeft = (self.x-1, self.y+1)
            diagonalRight = (self.x+1, self.y+1)

        if board.is_within_grid(forwardPos) and not board.is_coordinate_taken(forwardPos):
            moves.append(forwardPos)
        
        # Attack diagonal left
        if board.is_within_grid(diagonalLeft) and board.is_there_enemy(diagonalLeft, self.color):
            moves.append(diagonalLeft)

        # Attack diagonal right
        if board.is_within_grid(diagonalRight) and board.is_there_enemy(diagonalRight, self.color):
            moves.append(diagonalRight)

        return moves

class State:
    def __init__(self, piece: Piece, x, y):
        self.piece: Piece = piece
        self.x = x
        self.y = y

    def copy(self):
        piece = None
        if self.piece:
            piece = self.piece.copy()
        copy = State(piece, self.x, self.y)
        return copy

class Game:
    def __init__(self, gameboard, version):
        self.gridX = 5
        self.gridY = 5
        self.weights = {'King': 900, 'Queen': 90, 'Rook': 50, 'Bishop': 30, 'Knight': 30, 'Pawn': 10}
        self.xAxis = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4}
        self.grids = []
        self.version = version

        for x in range(self.gridX):
            self.grids.append([])
            for _ in range(self.gridY):
                self.grids[x].append(None)

        self.gameboard = gameboard
        self.black_score = 0
        self.white_score = 0
        self.player = 'White'
        self.turn = 'White'
        self.is_black_player_turn = False
        self.past_moves = []

        self.out_of_moves = False

        for x in range(self.gridX):
            for y in range(self.gridY):
                if self.grids[x][y] is None:
                    self.grids[x][y] = State(None, x, y)

        for posKey in gameboard:
            # ('a', 3) : ('Pawn', 'Black'), 
            # grid[0][0] = ('Pawn', 'Black')
            x = self.xAxis[posKey[0]]
            y = posKey[1]
            data = gameboard[posKey]
            piece = None
            if data[0] == 'King':
                piece =  King(x,y,data[1])
                if data[1] == 'White':
                    self.white_king_pos = (x, y)
                else:
                    self.black_king_pos = (x, y)

            if data[0] == 'Queen':
                piece =  Queen(x,y,data[1])
            if data[0] == 'Rook':
                piece =  Rook(x,y,data[1])
            if data[0] == 'Bishop':
                piece =  Bishop(x,y,data[1])
            if data[0] == 'Knight':
                piece =  Knight(x,y,data[1])
            if data[0] == 'Pawn':
                piece =  Pawn(x,y,data[1])
            
            if data[1] == 'Black':
                self.black_score += self.weights[data[0]] + piece.black_strategy[x][y]
            else:
                self.white_score += self.weights[data[0]] + piece.white_strategy[x][y]

            self.grids[x][y].piece = piece


    def is_valid_coordinate(self, coord, color) -> bool:
        if self.is_within_grid(coord):
            if (not self.is_coordinate_taken(coord) or self.is_there_enemy(coord, color)):
                return True
                
        return False

    def in_check(self, color) -> bool:
        king_coords = self.white_king_pos

        if color == 'Black':
            king_coords = self.black_king_pos
            
        for x in range(self.gridX):
            for y in range(self.gridY):
                if self.is_there_enemy((x, y), color):
                    for move in self.grids[x][y].piece.valid_moves(self):
                        if move[0] == king_coords[0] and move[1] == king_coords[1]:
                            return True

        return False

    def is_checkmate_on_try_pos(self, currPos, targetPos, color) -> bool:
        curr_state = self.grids[currPos[0]][currPos[1]]
        target_state = self.grids[targetPos[0]][targetPos[1]]
        curr_piece = curr_state.piece
        target_piece = target_state.piece

        old_king_pos = None
        if type(curr_piece) is King:
            if color == 'Black':
                old_king_pos = self.black_king_pos
            else:
                old_king_pos = self.white_king_pos

        # Move piece from current pos to target pos
        target_state.piece = curr_piece
        target_state.piece.move(target_state.x, target_state.y)
        curr_state.piece = None

        # Set king coords
        if type(curr_piece) is King:
            if color == 'Black':
                self.black_king_pos = (target_state.piece.x, target_state.piece.y)
            else:
                self.white_king_pos = (target_state.piece.x, target_state.piece.y)

        # toggle between black and white turn
        self.is_black_player_turn = not self.is_black_player_turn

        if self.in_check(color):
            in_check = True
        else:
            in_check = False

        if type(curr_piece) is King:
            if color == 'Black':
                self.black_king_pos = old_king_pos
            else:
                self.white_king_pos = old_king_pos

        # Restore player position
        self.is_black_player_turn = not self.is_black_player_turn

        # Move piece back
        curr_state.piece = curr_piece
        target_state.piece = target_piece
        curr_state.piece.move(curr_state.x, curr_state.y)

        return in_check
     
    # gives you the available move for the current player. 
    def get_move_list(self, version):
        moves = []
        for i in range(self.gridX):
            for j in range(self.gridY):
                currPos = (i, j)
                # if there is a piece and its the current player turn 
                if self.is_coordinate_taken(currPos) and self.grids[i][j].piece.color == self.turn:
                    piece = self.grids[i][j].piece
                    possible_move_list = piece.valid_moves(self)
                    for move in possible_move_list:
                        # make sure not check mate when move piece
                        if not self.is_checkmate_on_try_pos(currPos, move, self.turn):
                            # kill priority
                            if self.is_there_enemy(move, self.turn):
                                # insert front
                                moves.insert(0, (currPos, move, piece, True))
                            else:
                                # insert back
                                moves.append((currPos, move, piece, False))
        if version == 0:
            kill_moves = []
            leftover_moves = []
            for move in moves:
                if move[3] == True:
                    kill_moves.append(move)
                else:
                    leftover_moves.append(move)

            # sort ascending by weight. Tie break the pawn that can kill
            if len(kill_moves) > 1:
                kill_moves = sorted(kill_moves, key=lambda move_data: self.weights[str(move_data[2])], reverse=False)
            if len(leftover_moves) > 1:
                leftover_moves = sorted(leftover_moves, key=lambda move_data: self.weights[str(move_data[2])], reverse=False)

            return (kill_moves + leftover_moves)
        else:
            return moves

    def random_valid_move(self):
        moves = []
        for i in range(self.gridX):
            for j in range(self.gridY):
                currPos = (i, j)
                # if there is a piece and its the current player turn 
                if self.is_coordinate_taken(currPos) and self.grids[i][j].piece.color == self.turn:
                    piece = self.grids[i][j].piece
                    possible_move_list = piece.valid_moves(self)
                    for move in possible_move_list:
                        # kill priority
                        if self.is_there_enemy(move, self.turn):
                            # insert front
                            moves.insert(0, (currPos, move, piece, True))
                        else:
                            # insert back
                            moves.append((currPos, move, piece, False))

        moves = sorted(moves, key=lambda move_data: self.weights[str(move_data[2])], reverse=False)
        return moves[0]

    def is_within_grid(self, coords) -> bool:
        # check if coord is outside of the chess board
        if coords[0] < 0 or coords[0] >= 5 or coords[1] < 0 or coords[1] >= 5:
            # its outside
            return False
            
        # its inside
        return True


    def is_coordinate_taken(self, coords) -> bool:
        # if invalid board position return false
        # if not self.is_within_grid(coords):
        #     return False

        # if piece is None, return false
        if self.grids[coords[0]][coords[1]].piece is None:
            return False

        return True

    def is_there_enemy(self, coords, color) -> bool:
        coord_piece = self.grids[coords[0]][coords[1]].piece
        if self.is_coordinate_taken(coords):
            return coord_piece.color != color

        return False

    def check_no_legal_move(self):
        legal_moves = 0
        for x in range(self.gridX):
            for y in range(self.gridX):
                if self.is_coordinate_taken((x, y)) and self.grids[x][y].piece.color == self.turn:
                    moves = self.grids[x][y].piece.valid_moves(self)  # + self.can_castle(self.tilemap[x][y].piece.color)
                    legal_moves = len(moves)	
                    for move in moves:	
                        if not self.is_checkmate_on_try_pos((x, y), move, self.grids[x][y].piece.color):	
                        #if self.is_within_grid(move):	
                            legal_moves += 1

        if legal_moves == 0:
            self.out_of_moves = True

    def make_move(self, current_pos, target_pos):
        curr_state = self.grids[current_pos[0]][current_pos[1]]
        target_state = self.grids[target_pos[0]][target_pos[1]]

        previous_state = {"black_score": self.black_score,
                          "white_score": self.white_score,
                          "black_king_pos": self.black_king_pos,
                          "white_king_pos": self.white_king_pos,
                          "previousMove": (current_pos, curr_state.copy()),
                          "nextMove": (target_pos, target_state.copy()),
                          "out_of_moves": self.out_of_moves
                          }
        self.past_moves.append(previous_state)

    
        if target_state.piece:
            targetX = target_state.x
            targetY = target_state.y
            if self.turn == 'White':
                self.black_score -= (self.weights[str(target_state.piece)] + target_state.piece.black_strategy[targetX][targetY])
            else:
                self.white_score -= (self.weights[str(target_state.piece)] + target_state.piece.white_strategy[targetX][targetY])

       
        target_state.piece = curr_state.piece
        curr_state.piece.move(target_state.x, target_state.y)

        if type(curr_state.piece) is King:
            if curr_state.piece.color == 'Black':
                self.black_king_pos = target_state.x, target_state.y
            else:
                self.white_king_pos = target_state.x, target_state.y

        # Remove piece from current_pos tile
        curr_state.piece = None
        self.check_no_legal_move()

    def unmake_move(self):
        previous_state = self.past_moves.pop()
        self.black_score = previous_state["black_score"]
        self.white_score = previous_state["white_score"]
        self.black_king_pos = previous_state["black_king_pos"]
        self.white_king_pos = previous_state["white_king_pos"]

        prev_pos = previous_state["previousMove"][0]
        prev_grid_state = previous_state["previousMove"][1]
        prevX = prev_pos[0]
        prevY = prev_pos[1]
        self.grids[prevX][prevY] = prev_grid_state

        next_pos = previous_state["nextMove"][0]
        next_grid_state = previous_state["nextMove"][1]
        nextX = next_pos[0]
        nextY = next_pos[1]
        self.grids[nextX][nextY] = next_grid_state
        self.out_of_moves = previous_state["out_of_moves"]

        if self.turn == 'White':
            self.turn = 'Black'
        else:
            self.turn = 'White'

        self.is_black_player_turn = not self.is_black_player_turn

def evaluate(board: Game, maximizing_color):
    if maximizing_color == 'White':
        return board.white_score - board.black_score
    else:
        return board.black_score - board.white_score

def minimax(board: Game, depth: int, alpha: float, beta: float, maximizing_player: bool, maximizing_color: str, version: int):
    if depth == 0 or board.out_of_moves:
       if version == 2:
           return board.random_valid_move(), evaluate(board, maximizing_color)
       return None, evaluate(board, maximizing_color)

    moves = board.get_move_list(version)
    #print (moves)
    if len(moves) == 0:	
        if version == 2:
           return board.random_valid_move(), evaluate(board, maximizing_color)
        return None, evaluate(board, maximizing_color)
        
    best_move = moves[0] # need to compute best move

    if maximizing_player:
        max_eval = -inf
        for move in moves:
            # prune
            board.make_move(move[0], move[1])
            current_eval = minimax(board, depth - 1, alpha, beta, False, maximizing_color, version)[1]
            # backtrack
            board.unmake_move()
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = inf
        for move in moves:
            board.make_move(move[0], move[1])
            current_eval = minimax(board, depth - 1, alpha, beta, True, maximizing_color, version)[1]
            board.unmake_move()
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_move, min_eval


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    #config = sys.argv[1] #Takes in config.txt Optional
    minimaxMove = minimax(Game(gameboard, 0), 2, -inf, inf, True, 'White', 0)
    movement = minimaxMove[0]
    if movement is None:
        minimaxMove = minimax(Game(gameboard, 1), 2, -inf, inf, True, 'White', 1)
    movement = minimaxMove[0]

    if movement is None:
        minimaxMove = minimax(Game(gameboard, 2), 2, -inf, inf, True, 'White', 2)
    movement = minimaxMove[0]
    aPos = movement[0]
    bPos = movement[1]
    convertMove = ((xAxis[aPos[0]],aPos[1]), (xAxis[bPos[0]],bPos[1]))
    # move = (None, None)
    return convertMove #Format to be returned (('a', 0), ('b', 3))



# def startGame():
#     gameboard = {
#         ('a', 3) : ('Pawn', 'Black'), 
#         ('b', 3) : ('Pawn', 'Black'), 
#         ('c', 3) : ('Pawn', 'Black'),
#         ('d', 3) : ('Pawn', 'Black'),
#         ('e', 3) : ('Pawn', 'Black'),
#         ('a', 4) : ('Rook', 'Black'), 
#         ('b', 4) : ('Knight', 'Black'), 
#         ('c', 4) : ('Bishop', 'Black'),
#         ('d', 4) : ('Queen', 'Black'),
#         ('e', 4) : ('King', 'Black'),
#         ('a', 1) : ('Pawn', 'White'), 
#         ('b', 1) : ('Pawn', 'White'), 
#         ('c', 1) : ('Pawn', 'White'),
#         ('d', 1) : ('Pawn', 'White'),
#         ('e', 1) : ('Pawn', 'White'),
#         ('a', 0) : ('Rook', 'White'), 
#         ('b', 0) : ('Knight', 'White'), 
#         ('c', 0) : ('Bishop', 'White'),
#         ('d', 0) : ('Queen', 'White'),
#         ('e', 0) : ('King', 'White'),
#     }
    
#     move = studentAgent(gameboard)
#     print(move)


# import time
# start = time.time()
# startGame()
# end = time.time()
# print(f"{end - start}s")
