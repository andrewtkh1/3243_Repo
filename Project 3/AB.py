import copy
import heapq
import sys
import weakref

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.
### I AM WHITE, ENEMY IS BLACK

class InitParams:
    rows = 5
    cols = 5


class Board:
    dictOfRemovedPieces = {} #Pieces that have been removed from board.
    initialDictOfWhitePieces = {}
    initialDictOfBlackPieces = {}
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
    def markKnightMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces):
        (x,y) = chessPosToArr(pos)
        Moves.markTopRight(x+2, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopRight(x+1, y+2, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopRight(x-2, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopRight(x-1, y+2, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopRight(x-2, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopRight(x-1, y-2, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopRight(x+2, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopRight(x+1, y-2, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
            
    def markRookMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x,y+1,-1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markDown(x, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markLeft(x-1, y, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markRight(x+1, y, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
    
    def markBishopMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces):
        (x,y) = chessPosToArr(pos)
        Moves.markTopRight(x+1, y+1, -1, dictOfMoves, color , pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopLeft(x-1, y+1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markBotRight(x+1, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markBotLeft(x-1, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
            
    def markQueenMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x, y+1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markDown(x, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markLeft(x-1, y, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markRight(x+1, y, -1, dictOfMoves, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopRight(x+1, y+1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopLeft(x-1, y+1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markBotRight(x+1, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markBotLeft(x-1, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
    
    def markKingMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markDown(x, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markLeft(x-1, y, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markRight(x+1, y, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopRight(x+1, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markTopLeft(x-1, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markBotRight(x+1, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
        Moves.markBotLeft(x-1, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)

    def markPawnMove(pos, color, dictOfMoves, onlyThreatPos, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces):
        (x,y) = chessPosToArr(pos)
        if (color == "White"): #Moves from top down increasing y val.
            if (not onlyThreatPos):
                Moves.markUp(x, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
            diagMove = arrToChessPos(x+1, y+1)
            diagMove2 = arrToChessPos(x-1, y+1)
            if (diagMove in dictOfBlackPieces): #There is a piece to eat
                dictOfMoves[diagMove] = 1
                (pieceName, pieceColor) = dictOfBlackPieces.get(diagMove) #Adds piece to eat as higher priority.
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove))
                heapq.heappush(pqOfmoves, node)
            elif (diagMove2 in dictOfBlackPieces):
                dictOfMoves[diagMove2] = 1
                (pieceName, pieceColor) = dictOfBlackPieces.get(diagMove2) #Adds piece to eat as higher priority.
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove2))
                heapq.heappush(pqOfmoves, node)
        else: #If black piece
            if (not onlyThreatPos):
                Moves.markDown(x, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces)
            diagMove = arrToChessPos(x+1, y-1)
            diagMove2 = arrToChessPos(x-1, y-1)
            if (diagMove in dictOfWhitePieces): #There is a piece to eat
                dictOfMoves[diagMove] = 1
                (pieceName, pieceColor) = dictOfWhitePieces.get(diagMove) #Adds piece to eat as higher priority.
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove))
                heapq.heappush(pqOfmoves, node)
            elif (diagMove2 in dictOfWhitePieces):
                (pieceName, pieceColor) = dictOfWhitePieces.get(diagMove2) #Adds piece to eat as higher priority.
                dictOfMoves[diagMove2] = 1
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove2))
                heapq.heappush(pqOfmoves, node)
        return
    
    def markUp(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfBlackPieces) or (color == "Black" and pos in dictOfWhitePieces)): #eat another person's peice
            dictOfMoves[pos] = 1
            if (color == "White"):
                (pieceName, pieceColor) = dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markUp(x, y+1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces)

    def markDown(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfBlackPieces) or (color == "Black" and pos in dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markDown(x, y-1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces)

    def markLeft(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfBlackPieces) or (color == "Black" and pos in dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markLeft(x-1, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces)

    def markRight(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfBlackPieces) or (color == "Black" and pos in dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markRight(x+1, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces)

    def markTopRight(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfBlackPieces) or (color == "Black" and pos in dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markTopRight(x+1, y+1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces)

    def markTopLeft(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfBlackPieces) or (color == "Black" and pos in dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markTopLeft(x-1, y+1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces)

    def markBotRight(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfBlackPieces) or (color == "Black" and pos in dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markBotRight(x+1, y-1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces)

    def markBotLeft(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfBlackPieces) or (color == "Black" and pos in dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markBotLeft(x-1, y-1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces)

'''
Overall algo
Given current game board, Iterate thru till certain depth (LDS) to get Util function, recurse back and find next best move. Perform A-B Prune along the way.'''
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

    dictOfWhitePieces = {} #example: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
    dictOfBlackPieces = {}

    initializBoard(gameboard, dictOfWhitePieces, dictOfBlackPieces) #Populate dict of white/black and curboard.


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
def playerMax(maxBetaVal, board, totalMoves, dictOfWhitePieces, dictOfBlackPieces):
    maxVal = -1 #set to -inf
    dictOfBlackThreats = {}
    dictOfMoves = {} #{'a0' : ('Queen', listOfPossibleMoves)}
    pqOfMoves = [] #[(-10, ('a3', 'b3', "Queen")] (source, dest, Piece)
    heapq.heapify(pqOfMoves)

    #Get list of moves
    for whitePos in dictOfWhitePieces:
        (whitePiece, color) = dictOfWhitePieces.get(whitePos) #example: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
        moves = getListOfMoves(pos, whitePiece, "White", False, pqOfMoves, dictOfWhitePieces, dictOfBlackPieces)
        dictOfMoves[pos] = (whitePiece, moves)

    if (len(dictOfMoves) == 0):
        # Out of moves.
        return 1

    if (isTerminal(totalMoves, "White", dictOfWhitePieces, dictOfBlackPieces)):
        paddingList = [] #can ignore
        if (totalMoves < 5): # Terminated due to a king missing.
            return -10 # I lost my king

        # Reached end of LDS. Need to get Current board value.
        for pos in dictOfBlackPieces: # Get the current threats for Opponent.
            (piece, color) = dictOfBlackPieces.get(pos)
            threats = getListOfMoves(pos, piece, "Black", True, paddingList, dictOfWhitePieces, dictOfBlackPieces)
            dictOfBlackThreats[pos] = threats # {'a0': list Of position he threatens}

        return getUtil(board, "White", dictOfBlackThreats, dictOfMoves, dictOfWhitePieces, dictOfBlackPieces)
    
    #iterate thru list of possible moves from best to worst
    while(len(pqOfMoves) > 0):
        # Want to add avoiding moving into self-check
        (cost, (sourcePos, destPos)) = heapq.heappop(pqOfMoves)
        
    pass

# Ways to checkmate: Check if king can move out of the way OR get list of people threatens king & see if can eat any. OR see any local piece can block(Get from list of moves)
# Possible current util vaues: Checkmate -> capture and check -> Capture -> Check

# dictOfThreats = {'a0': list Of position he threatens, 'b0' : ....}
# Check = 6, Checkmate = -100
# dictOfPiece: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
# dict of my atk: {'a0': ('Queen', dict of position it threatens)}
def getUtil(board, color, dictOfEnemyThreats, dictOfMyAttacks, dictOfMyPiece, dictOfEnemyPiece):
    #Gets current position of my own King & enemy king
    dictOfPosAgainstKing = {}
    numOfPiecesAte = 0
    isCheckmate = False
    hasEatPiece = False
    isCheck = False

    #Get position of my king and enemy king
    for pos in dictOfMyPiece:
        (piece, color) = dictOfMyPiece.get(pos)
        if (piece == "King"):
            kingPos = pos
        
    for pos in dictOfEnemyPiece:
        (piece, color) = dictOfEnemyPiece.get(pos)
        if (piece == "King"):
            enemyKingPos = pos
    
    for originThreatPos in dictOfEnemyThreats: #Find who threatens my King
        if (kingPos in dictOfEnemyThreats.get(originThreatPos)):
            dictOfPosAgainstKing[originThreatPos] = 1
    
    numOfThreats = len(dictOfPosAgainstKing)
    
    if (numOfThreats <= 0): # If true -> no checks against king
        isCheck = True

    # Get total value of people that was ate.
    if (color == "White"):
        numOfPiecesAte = len(Board.initialDictOfBlackPieces) - len(dictOfEnemyPiece)
        if (numOfPiecesAte > 0):
            valueOfEatenPiece = getValueOfPiecesEatened(Board.initialDictOfBlackPieces, dictOfEnemyPiece)
    else:
        numOfPiecesAte = len(Board.initialDictOfWhitePieces) - len(dictOfEnemyPiece)
        if (numOfPiecesAte > 0):
            valueOfEatenPiece = getValueOfPiecesEatened(Board.initialDictOfWhitePieces, dictOfEnemyPiece)

    if (numOfPiecesAte > 0):
        hasEatPiece = True

    # Checkmate -> capture and check -> Capture -> Check
    if (not hasEatPiece and not isCheck): # No eats or no checks
        return 0
    elif (not isCheck and hasEatPiece): # Only Ate
        return valueOfEatenPiece

    canEatOppKing = False
    if (numOfThreats == 1): # IF only 1 threat against King, can consider eating it to escape.
        #Check if checkmate
        for ownPiecePos in dictOfMyAttacks: #Check if I am able to eat the king
            (pieceName, moves) = dictOfMyAttacks.get(ownPiecePos)
            if (enemyKingPos in moves):
                isCheckmate = False
                break
            isCheckmate = True
        
        if (isCheckmate):
            return -100
        if (isCheck and hasEatPiece):
            return -(valueOfEatenPiece + 6)
        if (isCheck):
            return 6
        
    # Has more than 2 pieces against my king
    nullList = [] #Just to fill up the parameter
    dictOfPossibleKingMoves = {} #Possible moves for my own king
    Moves.markKingMove(kingPos, dictOfPossibleKingMoves, color, dictOfMyPiece, dictOfEnemyPiece) #Get possible escapes
    canEscape = False
    
    for possibeEscape in list(dictOfPossibleKingMoves):
        isThreat = False
        for oppPos in dictOfEnemyThreats:
            enemyMoves = dictOfEnemyThreats.get(oppPos)
            if (possibeEscape in enemyMoves):
                isThreat = True
                break
        if (isThreat == False):
            canEscape = True
            break
    
    if (not canEscape): # Means no escape hence checkmate
        return -100
    
    if (canEscape and hasEatPiece): # Check and ate
        return -(valueOfEatenPiece + 6)
    
    return 6 #Only check.
        
#Find the total value of missing pieces
#example: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
def getValueOfPiecesEatened(dictOfInitialPieces, dictOfRemainingPieces):
    numOfPawn = 0
    numOfKnight = 0
    numOfBishop = 0
    numOfRook = 0
    numOfQueen = 0
    # No King as it is taken care by terminal state.
    
    #Find initial pieces
    for pos in dictOfInitialPieces:
        (piece, color) = dictOfInitialPieces.get(pos)
        if (piece == "Pawn"):
            numOfPawn+=1
        elif (piece == "Knight"):
            numOfKnight+=1
        elif (piece == "Bishop"):
            numOfBishop+=1
        elif (piece == "Rook"):
            numOfRook+=1
        elif (piece == "Queen"):
            numOfQueen+=1

    #Minus current pieces
    for curPos in dictOfRemainingPieces:
        (curPiece, color) = dictOfRemainingPieces.get(curPos)
        if (curPiece == "Pawn"):
            numOfPawn-=1
        elif (curPiece == "Knight"):
            numOfKnight-=1
        elif (curPiece == "Bishop"):
            numOfBishop-=1
        elif (curPiece == "Rook"):
            numOfRook-=1
        elif (curPiece == "Queen"):
            numOfQueen-=1

    return numOfPawn*getPieceValue("Pawn") + numOfBishop*getPieceValue("Bishop") + numOfKnight*getPieceValue("Knight") + numOfRook*getPieceValue("Rook") + numOfQueen*getPieceValue("Queen")

def getPieceValue(pieceName):
    if (pieceName == "King"):
        return 11
    if (pieceName == "Queen"):
        return 10
    if (pieceName == "Rook"):
        return 9
    if (pieceName == "Bishop"):
        return 9
    if (pieceName == "Knight"):
        return 8
    if (pieceName == "Pawn"):
        return 7
    
# Terminal cases. King is gone.
def isTerminal(numOfmoves, color, dictOfWhitePieces, dictOfBlackPieces):
    if (numOfmoves > 5):
        return True
    
    #Check for kings
    if (color == "Black"):
        for pos in dictOfBlackPieces:
            (pieceName, pieceColor) = dictOfBlackPieces.get(pos)
            if (pieceName == "King"):
                return False
    else:
        for pos in dictOfWhitePieces:
            (pieceName, pieceColor) = dictOfWhitePieces.get(pos)
            if (pieceName == "King"):
                return False
    return True


# list of moves returned. Moves can either eat or not eat. All are valid.
def getListOfMoves(pos, piece, color, onlyThreatFlag, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces):   
    dictOfMoves = {}
    if (piece == "Queen"):
        Moves.markQueenMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces)
    elif (piece == "Rook"):
        Moves.markRookMove(pos,dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces)
    elif (piece == "Bishop"):
        Moves.markBishopMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces)
    elif (piece == "Knight"):
        Moves.markKnightMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces)
    elif( piece == "King"):
        Moves.markKingMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces)
    elif (piece == "Pawn"):
        Moves.markPawnMove(pos, color, dictOfMoves, onlyThreatFlag, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces)
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
def initializBoard(startGameBoard, dictOfWhitePieces, dictOfBlackPieces):
    for pos in startGameBoard:
        data = startGameBoard.get(pos)
        (piece, color) = data
        charPos = chr(pos[1] + pos[2])
        if (color == "White"):
            dictOfWhitePieces[charPos] = data
            Board.initialDictOfWhitePieces[charPos] = data
        else:
            dictOfBlackPieces[charPos] = data
            Board.initialDictOfBlackPieces[charPos] = data