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
    def markKnightMove(pos, dictOfMoves, color, pqOfmoves):
        (x,y) = chessPosToArr(pos)
        Moves.markTopRight(x+2, y+1, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markTopRight(x+1, y+2, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markTopRight(x-2, y+1, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markTopRight(x-1, y+2, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markTopRight(x-2, y-1, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markTopRight(x-1, y-2, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markTopRight(x+2, y-1, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markTopRight(x+1, y-2, 1, dictOfMoves, color, pqOfmoves, pos)
            
    def markRookMove(pos, dictOfMoves, color, pqOfmoves):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x,y+1,-1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markDown(x, y-1, -1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markLeft(x-1, y, -1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markRight(x+1, y, -1, dictOfMoves, color, pqOfmoves, pos)
    
    def markBishopMove(pos, dictOfMoves, color, pqOfmoves):
        (x,y) = chessPosToArr(pos)
        Moves.markTopRight(x+1, y+1, -1, dictOfMoves, color , pqOfmoves, pos)
        Moves.markTopLeft(x-1, y+1, -1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markBotRight(x+1, y-1, -1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markBotLeft(x-1, y-1, -1, dictOfMoves, color, pqOfmoves, pos)
            
    def markQueenMove(pos, dictOfMoves, color, pqOfmoves):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x, y+1, -1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markDown(x, y-1, -1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markLeft(x-1, y, -1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markRight(x+1, y, -1, dictOfMoves, pqOfmoves, pos)
        Moves.markTopRight(x+1, y+1, -1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markTopLeft(x-1, y+1, -1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markBotRight(x+1, y-1, -1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markBotLeft(x-1, y-1, -1, dictOfMoves, color, pqOfmoves, pos)
    
    def markKingMove(pos, dictOfMoves, color, pqOfmoves):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x, y+1, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markDown(x, y-1, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markLeft(x-1, y, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markRight(x+1, y, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markTopRight(x+1, y+1, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markTopLeft(x-1, y+1, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markBotRight(x+1, y-1, 1, dictOfMoves, color, pqOfmoves, pos)
        Moves.markBotLeft(x-1, y-1, 1, dictOfMoves, color, pqOfmoves, pos)

    def markPawnMove(pos, color, dictOfMoves, onlyThreatPos, pqOfmoves):
        (x,y) = chessPosToArr(pos)
        if (color == "White"): #Moves from top down increasing y val.
            if (not onlyThreatPos):
                Moves.markUp(x, y+1, 1, dictOfMoves, color, pqOfmoves, pos)
            diagMove = arrToChessPos(x+1, y+1)
            diagMove2 = arrToChessPos(x-1, y+1)
            if (diagMove in Board.dictOfBlackPieces): #There is a piece to eat
                dictOfMoves[diagMove] = 1
                (pieceName, pieceColor) = Board.dictOfBlackPieces.get(diagMove) #Adds piece to eat as higher priority.
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove))
                heapq.heappush(pqOfmoves, node)
            elif (diagMove2 in Board.dictOfBlackPieces):
                dictOfMoves[diagMove2] = 1
                (pieceName, pieceColor) = Board.dictOfBlackPieces.get(diagMove2) #Adds piece to eat as higher priority.
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove2))
                heapq.heappush(pqOfmoves, node)
        else: #If black piece
            if (not onlyThreatPos):
                Moves.markDown(x, y-1, 1, dictOfMoves, color, pqOfmoves, pos)
            diagMove = arrToChessPos(x+1, y-1)
            diagMove2 = arrToChessPos(x-1, y-1)
            if (diagMove in Board.dictOfWhitePieces): #There is a piece to eat
                dictOfMoves[diagMove] = 1
                (pieceName, pieceColor) = Board.dictOfWhitePieces.get(diagMove) #Adds piece to eat as higher priority.
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove))
                heapq.heappush(pqOfmoves, node)
            elif (diagMove2 in Board.dictOfWhitePieces):
                (pieceName, pieceColor) = Board.dictOfWhitePieces.get(diagMove2) #Adds piece to eat as higher priority.
                dictOfMoves[diagMove2] = 1
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove2))
                heapq.heappush(pqOfmoves, node)
        return
    
    def markUp(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #eat another person's peice
            dictOfMoves[pos] = 1
            if (color == "White"):
                (pieceName, pieceColor) = Board.dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = Board.dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markUp(x, y+1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos)

    def markDown(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = Board.dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = Board.dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markDown(x, y-1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos)

    def markLeft(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = Board.dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = Board.dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markLeft(x-1, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos)

    def markRight(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = Board.dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = Board.dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markRight(x+1, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos)

    def markTopRight(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = Board.dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = Board.dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markTopRight(x+1, y+1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos)

    def markTopLeft(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = Board.dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = Board.dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markTopLeft(x-1, y+1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos)

    def markBotRight(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = Board.dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = Board.dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markBotRight(x+1, y-1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos)

    def markBotLeft(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in Board.dictOfBlackPieces) or (color == "Black" and pos in Board.dictOfWhitePieces)): #Hit a piece
            if (color == "White"):
                (pieceName, pieceColor) = Board.dictOfBlackPieces.get(pos) #Adds piece to eat as higher priority for white's move
            else:
                (pieceName, pieceColor) = Board.dictOfWhitePieces.get(pos) #Adds piece to eat as higher priority for black's move
            dictOfMoves[pos] = 1
            val = -getPieceValue(pieceName)
            node = (val, (originPos, pos))
            heapq.heappush(pqOfmoves, node)
            return
        dictOfMoves[pos] = 1
        node = (-1, (originPos,pos)) # Add move without eating into PQ.
        heapq.heappush(pqOfmoves, node)
        numOfMoves-=1
        Moves.markBotLeft(x-1, y-1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos)

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
    
    initializBoard(gameboard) #Populate dict of white/black and curboard.

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
def playerMax(maxBetaVal, board, totalMoves, dictOfWhiteRemoved, dictOfBlackRemoved):
    maxVal = -1 #set to -inf
    dictOfBlackThreats = {}
    dictOfMoves = {} #{'a0' : ('Queen', listOfPossibleMoves)}
    pqOfMoves = [] #[(-10, ('a3', 'b3', "Queen")] (source, dest, Piece)
    heapq.heapify(pqOfMoves)

    #Get list of moves
    for whitePos in Board.dictOfWhitePieces:
        (whitePiece, color) = Board.dictOfWhitePieces.get(whitePos) #example: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
        moves = getListOfMoves(pos, whitePiece, "White", False, pqOfMoves)
        dictOfMoves[pos] = (whitePiece, moves)

    if (isTerminal(totalMoves, "White")):
        paddingList = [] #can ignore
        if (totalMoves < 5): # Terminated due to a king missing.
            return -10 # I lost my king

        # Reached end of LDS. Need to get Current board value.
        for pos in Board.dictOfBlackPieces: # Get the current threats for Opponent.
            (piece, color) = Board.dictOfBlackPieces.get(pos)
            threats = getListOfMoves(pos, piece, "Black", True, paddingList)
            dictOfBlackThreats[pos] = threats # {'a0': list Of position he threatens}

        pqOfTerminalMoves = []
        heapq.heapify(pqOfTerminalMoves)
        getUtil(board, "White", dictOfBlackThreats, dictOfMoves, pqOfTerminalMoves)
        
    if (len(pqOfMoves == 0)):
        #Out of moves hence tie
        return 0
    
    #iterate thru list of possible moves from best to worst
    while(len(pqOfMoves) > 0):
        (cost, (sourcePos, destPos)) = heapq.heappop(pqOfMoves)
        
    pass

# Ways to checkmate: Check if king can move out of the way OR get list of people threatens king & see if can eat any. OR see any local piece can block(Get from list of moves)
# Possible current util vaues: Checkmate -> capture and check -> Capture -> Check
# dictOfThreats = {'a0': list Of position he threatens, 'b0' : ....}
# Check = 1, Checkmate = 50
def getUtil(board, color, dictOfEnemyThreats, dictOfMyAttacks, pqOfMoves):
    #Gets current position of my own King & enemy king
    dictOfPosAgainstKing = {}
    isCheckmate = False

    if (color == "White"):
        for pos in Board.dictOfWhitePieces:
            (piece, color) = Board.dictOfWhitePieces.get(pos)
            if (piece == "King"):
                kingPos = pos
        
        for pos in Board.dictOfBlackPieces:
            (piece, color) = Board.dictOfBlackPieces.get(pos)
            if (piece == "King"):
                enemyKingPos = pos
    else:
        for pos in Board.dictOfBlackPieces:
            (piece, color) = Board.dictOfBlackPieces.get(pos)
            if (piece == "King"):
                kingPos = pos
        
        for pos in Board.dictOfWhitePieces:
            (piece, color) = Board.dictOfWhitePieces.get(pos)
            if (piece == "King"):
                enemyKingPos = pos
    
    for originThreatPos in dictOfEnemyThreats: #Find who threatens my King
        if (kingPos in dictOfEnemyThreats.get(originThreatPos)):
            dictOfPosAgainstKing[originThreatPos] = 1
    
    numOfThreats = len(dictOfPosAgainstKing)
    
    if (numOfThreats <= 0): # If true -> no checks against king
        return 0

    if (numOfThreats == 1): #if it's 1 piece, try to eat it. If more than 2, can't eat
        (threatSourcePos, x) = dictOfPosAgainstKing.popitem()
        for myPos in dictOfMyAttacks:
            (pieceName, moves) = dictOfMyAttacks.get(myPos)
            if (threatSourcePos in moves): # My position is able to eat the person threatning king
                heapq.heappush(pqOfMoves,(-100, (myPos, threatSourcePos, pieceName)))
                continue        

    for ownPiecePos in dictOfMyAttacks: #Check if I am able to eat the king
        (pieceName, moves) = dictOfMyAttacks.get(ownPiecePos)
        if (enemyKingPos in moves):
            isCheckOpponent = True
            break
        
    nullList = [] #Just to fill up the parameter
    dictOfPossibleKingMoves = {} #Possible moves for my own king
    Moves.markKingMove(kingPos, dictOfPossibleKingMoves, color) #Get possible escapes
    
    for possiblePos in dictOfPossibleKingMoves:
        if (possiblePos not in dictOfPosAgainstKing):
            heapq.heappush(pqOfMoves,(-100, (myPos, threatSourcePos, pieceName)))

    pass

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
def isTerminal(numOfmoves, color):
    if (numOfmoves > 5):
        return True
    
    #Check for kings
    if (color == "Black"):
        for pos in Board.dictOfBlackPieces:
            (pieceName, pieceColor) = Board.dictOfBlackPieces.get(pos)
            if (pieceName == "King"):
                return False
    else:
        for pos in Board.dictOfWhitePieces:
            (pieceName, pieceColor) = Board.dictOfWhitePieces.get(pos)
            if (pieceName == "King"):
                return False
    return True


# list of moves returned. Moves can either eat or not eat. All are valid.
def getListOfMoves(pos, piece, color, onlyThreatFlag, pqOfmoves):   
    dictOfMoves = {}
    if (piece == "Queen"):
        Moves.markQueenMove(pos, dictOfMoves, color, pqOfmoves)
    elif (piece == "Rook"):
        Moves.markRookMove(pos,dictOfMoves, color, pqOfmoves)
    elif (piece == "Bishop"):
        Moves.markBishopMove(pos, dictOfMoves, color, pqOfmoves)
    elif (piece == "Knight"):
        Moves.markKnightMove(pos, dictOfMoves, color, pqOfmoves)
    elif( piece == "King"):
        Moves.markKingMove(pos, dictOfMoves, color, pqOfmoves)
    elif (piece == "Pawn"):
        Moves.markPawnMove(pos, color, dictOfMoves, onlyThreatFlag, pqOfmoves)
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
def initializBoard(startGameBoard):
    for pos in startGameBoard:
        data = startGameBoard.get(pos)
        (piece, color) = data
        charPos = chr(pos[1] + pos[2])
        Board.dictOfCurBoard[charPos] = data
        if (color == "White"):
            Board.dictOfWhitePieces[charPos] = data
        else:
            Board.dictOfBlackPieces[charPos] = data