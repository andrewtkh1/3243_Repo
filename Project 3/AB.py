import heapq
import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.
### I AM WHITE, ENEMY IS BLACK

class InitParams:
    rows = 5
    cols = 5


class Board:
    dictOfRemovedPieces = {} #Pieces that have been removed from board.
    dictOfCurBoard = {} #example: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
    dictOfWhitePieces = {} #example: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
    dictOfBlackPieces = {}
    pass

# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
class Game:
    enemyPieces = {('e', 4) : ('King', 'Black'), ('d', 4): ('Queen', 'Black'), ('c', 4): ('Bishop', 'Black'), ('b', 4): ('Knight', 'Black'), ('a', 4): ('Rook', 'Black')
    , ('a', 3): ('Pawn', 'Black'), ('b', 3): ('Pawn', 'Black'), ('c', 3): ('Pawn', 'Black'), ('d', 3): ('Pawn', 'Black'), ('e', 3): ('Pawn', 'Black')}

    ownPieces = {('e', 0): ('King', 'White'), ('d', 0): ('Queen', 'White'), ('c', 0): ('Bishop', 'White'), ('b', 0): ('Knight', 'White'), ('a', 0): ('Rook', 'White')
    , ('a', 1): ('Pawn', 'White'), ('b', 1): ('Pawn', 'White'), ('c', 1): ('Pawn', 'White'), ('d', 1): ('Pawn', 'White'), ('e', 1): ('Pawn', 'White')}

    startGameBoard = {**enemyPieces, **ownPieces}
    pass


class Moves:        
    def markKnightMove(pos, dictOfMoves, color):
        (x,y) = chessPosToArr(pos)
        Moves.markTopRight(x+2, y+1, 1, dictOfMoves, color)
        Moves.markTopRight(x+1, y+2, 1, dictOfMoves, color)
        Moves.markTopRight(x-2, y+1, 1, dictOfMoves, color)
        Moves.markTopRight(x-1, y+2, 1, dictOfMoves, color)
        Moves.markTopRight(x-2, y-1, 1, dictOfMoves, color)
        Moves.markTopRight(x-1, y-2, 1, dictOfMoves, color)
        Moves.markTopRight(x+2, y-1, 1, dictOfMoves, color)
        Moves.markTopRight(x+1, y-2, 1, dictOfMoves, color)
            
    def markRookMove(pos, dictOfMoves, color):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x,y+1,-1, dictOfMoves, color)
        Moves.markDown(x, y-1, -1, dictOfMoves, color)
        Moves.markLeft(x-1, y, -1, dictOfMoves, color)
        Moves.markRight(x+1, y, -1, dictOfMoves, color)
    
    def markBishopMove(pos, dictOfMoves, color):
        (x,y) = chessPosToArr(pos)
        Moves.markTopRight(x+1, y+1, -1, dictOfMoves), color
        Moves.markTopLeft(x-1, y+1, -1, dictOfMoves, color)
        Moves.markBotRight(x+1, y-1, -1, dictOfMoves, color)
        Moves.markBotLeft(x-1, y-1, -1, dictOfMoves, color)
            
    def markQueenMove(pos, dictOfMoves, color):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x, y+1, -1, dictOfMoves, color)
        Moves.markDown(x, y-1, -1, dictOfMoves, color)
        Moves.markLeft(x-1, y, -1, dictOfMoves, color)
        Moves.markRight(x+1, y, -1, dictOfMoves)
        Moves.markTopRight(x+1, y+1, -1, dictOfMoves, color)
        Moves.markTopLeft(x-1, y+1, -1, dictOfMoves, color)
        Moves.markBotRight(x+1, y-1, -1, dictOfMoves, color)
        Moves.markBotLeft(x-1, y-1, -1, dictOfMoves, color)
    
    def markKingMove(pos, dictOfMoves, color):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x, y+1, 1, dictOfMoves, color)
        Moves.markDown(x, y-1, 1, dictOfMoves, color)
        Moves.markLeft(x-1, y, 1, dictOfMoves, color)
        Moves.markRight(x+1, y, 1, dictOfMoves, color)
        Moves.markTopRight(x+1, y+1, 1, dictOfMoves, color)
        Moves.markTopLeft(x-1, y+1, 1, dictOfMoves, color)
        Moves.markBotRight(x+1, y-1, 1, dictOfMoves, color)
        Moves.markBotLeft(x-1, y-1, 1, dictOfMoves, color)

    def markPawnMove(pos, color, dictOfMoves, onlyThreatPos):
        (x,y) = chessPosToArr(pos)
        if (color == "White"): #Moves from top down increasing y val.
            if (not onlyThreatPos):
                Moves.markUp(x, y+1, 1, dictOfMoves, color)
            diagMove = arrToChessPos(x+1, y+1)
            diagMove2 = arrToChessPos(x-1, y+1)
            if (diagMove in Board.dictOfBlackPieces): #There is a piece to eat
                dictOfMoves[diagMove] = 1
            elif (diagMove2 in Board.dictOfBlackPieces):
                dictOfMoves[diagMove2] = 1
        else: #If black piece
            if (not onlyThreatPos):
                Moves.markDown(x, y-1, 1, dictOfMoves, color)
            diagMove = arrToChessPos(x+1, y-1)
            diagMove2 = arrToChessPos(x-1, y-1)
            if (diagMove in Board.dictOfWhitePieces): #There is a piece to eat
                dictOfMoves[diagMove] = 1
            elif (diagMove2 in Board.dictOfWhitePieces):
                dictOfMoves[diagMove2] = 1
        return
    
    def markUp(x, y, numOfMoves, dictOfMoves, color):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #eat another person's peice
            dictOfMoves[pos] = 1
            return
        dictOfMoves[pos] = 1
        numOfMoves-=1
        Moves.markUp(x, y+1, numOfMoves, dictOfMoves, color)

    def markDown(x, y, numOfMoves, dictOfMoves, color):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            dictOfMoves[pos] = 1
            return
        dictOfMoves[pos] = 1
        numOfMoves-=1
        Moves.markDown(x, y-1, numOfMoves, dictOfMoves, color)

    def markLeft(x, y, numOfMoves, dictOfMoves, color):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            dictOfMoves[pos] = 1
            return
        dictOfMoves[pos] = 1
        numOfMoves-=1
        Moves.markLeft(x-1, y, numOfMoves, dictOfMoves, color)

    def markRight(x, y, numOfMoves, dictOfMoves, color):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            dictOfMoves[pos] = 1
            return
        dictOfMoves[pos] = 1
        numOfMoves-=1
        Moves.markRight(x+1, y, numOfMoves, dictOfMoves, color)

    def markTopRight(x, y, numOfMoves, dictOfMoves, color):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            dictOfMoves[pos] = 1
            return
        dictOfMoves[pos] = 1
        numOfMoves-=1
        Moves.markTopRight(x+1, y+1, numOfMoves, dictOfMoves, color)

    def markTopLeft(x, y, numOfMoves, dictOfMoves, color):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            dictOfMoves[pos] = 1
            return
        dictOfMoves[pos] = 1
        numOfMoves-=1
        Moves.markTopLeft(x-1, y+1, numOfMoves, dictOfMoves, color)

    def markBotRight(x, y, numOfMoves, dictOfMoves, color):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            dictOfMoves[pos] = 1
            return
        dictOfMoves[pos] = 1
        numOfMoves-=1
        Moves.markBotRight(x+1, y-1, numOfMoves, dictOfMoves, color)

    def markBotLeft(x, y, numOfMoves, dictOfMoves, color):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            dictOfMoves[pos] = 1
            return
        dictOfMoves[pos] = 1
        numOfMoves-=1
        Moves.markBotLeft(x-1, y-1, numOfMoves, dictOfMoves, color)

'''
Overall algo
Given current game board, Iterate thru till certain depth (LDS) to get Util function, recurse back and find next best move. Perform A-B Prune along the way.'''

'''
Try all possible moves using LDS. Each move has a util function associated. Once reached LDS Depth, find current eval and recurse back up. 

Eval at depth 5:

Possible util functions:
Eat king -> 20
check -> 
Eat Piece & check -> piece cost + check

Eat queen -> 9
Eat rook -> 5
Eat Bishop / Knight -> 3
Eat Pawn -> 1

'''

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
    config = sys.argv[1] #Takes in config.txt Optional

    move = (None, None)
    return move #Format to be returned (('a', 0), ('b', 3))

#Implement your minimax with alpha-beta pruning algorithm here.
def ab():
    pass

#Prune if cur iter val <= minAlphaVal
def oppMin(minAlphaVal):
    pass

#Prune if cur iter val >= maxBetaVal
# white Piece
def playerMax(maxBetaVal, board, totalMoves):
    maxVal = -1 #set to -inf
    dictOfBlackThreats = {}
    hasNoMoreMoves = True
    dictOfMoves = {} #{'a0' : ('Queen', listOfPossibleMoves)}
    for whitePos in Board.dictOfWhitePieces:
        (whitePiece, color) = Board.dictOfWhitePieces.get(whitePos) #example: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
        moves = getListOfMoves(pos, whitePiece, "White", False)
        if (len(moves) > 0):
            hasNoMoreMoves = False
        dictOfMoves[pos] = (whitePiece, moves)
    if (hasNoMoreMoves):
        #Out of moves hence tie
        return 0
    
    for pos in Board.dictOfBlackPieces: # Get the current threats for Opponent.
        (piece, color) = Board.dictOfBlackPieces.get(pos)
        threats = getListOfMoves(pos, piece, "Black", True)
        dictOfBlackThreats[pos] = threats # {'a0': list Of position he threatens}
    if (isTerminal(board, "White", dictOfBlackThreats)):
        
        pass
    pass

# Terminal cases: No more moves, checkmate.
# Ways to checkmate: Check if king can move out of the way OR get list of people threatens king & see if can eat any. OR see any local piece can block(Get from list of moves)
# dictOfThreats = {'a0': list Of position he threatens, 'b0' : ....}
def isTerminal(board, color, dictOfThreats):
    #Gets current position of my own King.
    dictOfPosAgainstKing = {}
    dictOfPossibleKingMoves = {}
    if (color == "White"):
        for pos in Board.dictOfWhitePieces:
            (piece, color) = Board.dictOfWhitePieces.get(pos)
            if (piece == "King"):
                kingPos = pos
    else:
        for pos in Board.dictOfBlackPieces:
            (piece, color) = Board.dictOfBlackPieces.get(pos)
            if (piece == "King"):
                kingPos = pos
    
    for originThreatPos in dictOfThreats: #Find who threatens king
        if (kingPos in dictOfThreats.get(originThreatPos)):
            dictOfPosAgainstKing[originThreatPos] = 1
    
    numOfThreats = len(dictOfPosAgainstKing)
    
    if (numOfThreats <= 0): # If true -> no ones threatens king
        return False
    
    if (numOfThreats == 1): #if it's 1 piece, try to eat it. If more than 2, can't eat
        
        pass
        
        
    Moves.markKingMove(kingPos, dictOfPossibleKingMoves, color) #Get possible escapes
    

    pass

# list of moves returned. Moves can either eat or not eat. All are valid.
def getListOfMoves(pos, piece, color, onlyThreatFlag):
    dictOfMoves = {}
    if (piece == "Queen"):
        Moves.markQueenMove(pos, dictOfMoves, color)
    elif (piece == "Rook"):
        Moves.markRookMove(pos,dictOfMoves, color)
    elif (piece == "Bishop"):
        Moves.markBishopMove(pos, dictOfMoves, color)
    elif (piece == "Knight"):
        Moves.markKnightMove(pos, dictOfMoves, color)
    elif( piece == "King"):
        Moves.markKingMove(pos, dictOfMoves, color)
    elif (piece == "Pawn"):
        Moves.markPawnMove(pos, color, dictOfMoves, onlyThreatFlag)
    return dictOfMoves

# Converts chess coordinate to X,Y
def chessPosToArr(pos) -> tuple:
    x = ord(pos[0]) - ord('a')
    y = int(pos[1:])
    return (x,y)

# Converts X,Y to chess coords
def arrToChessPos(x, y):
    ch = chr(x + ord('a'))
    return ch + str(y)

def intToChar(curInt):
    return chr(curInt + ord('a'))

#('d', 10) : ('Knight', 'Black') -> 'd10' : ('Knight', 'Black')
def initializBoard():
    for pos in Game.startGameBoard:
        data = Game.startGameBoard.get(pos)
        (piece, color) = data
        charPos = chr(pos[1] + pos[2])
        Board.dictOfCurBoard[charPos] = data
        if (color == "White"):
            Board.dictOfWhitePieces[charPos] = data
        else:
            Board.dictOfBlackPieces[charPos] = data
        