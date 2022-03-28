import copy
import heapq
from os import terminal_size
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
    def markKnightMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        (x,y) = chessPosToArr(pos)
        Moves.markTopRight(x+2, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopRight(x+1, y+2, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopRight(x-2, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopRight(x-1, y+2, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopRight(x-2, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopRight(x-1, y-2, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopRight(x+2, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopRight(x+1, y-2, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
            
    def markRookMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x,y+1,-1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, False)
        Moves.markDown(x, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, False)
        Moves.markLeft(x-1, y, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markRight(x+1, y, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
    
    def markBishopMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        (x,y) = chessPosToArr(pos)
        Moves.markTopRight(x+1, y+1, -1, dictOfMoves, color , pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopLeft(x-1, y+1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markBotRight(x+1, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markBotLeft(x-1, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
            
    def markQueenMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x, y+1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, False)
        Moves.markDown(x, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, False)
        Moves.markLeft(x-1, y, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markRight(x+1, y, -1, dictOfMoves, color,pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopRight(x+1, y+1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopLeft(x-1, y+1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markBotRight(x+1, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markBotLeft(x-1, y-1, -1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
    
    def markKingMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        (x,y) = chessPosToArr(pos)
        Moves.markUp(x, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, False)
        Moves.markDown(x, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, False)
        Moves.markLeft(x-1, y, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markRight(x+1, y, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopRight(x+1, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markTopLeft(x-1, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markBotRight(x+1, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        Moves.markBotLeft(x-1, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)

    def markPawnMove(pos, color, dictOfMoves, onlyThreatPos, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        (x,y) = chessPosToArr(pos)
        if (color == "White"): #Moves from top down increasing y val.
            if (not onlyThreatPos):
                Moves.markUp(x, y+1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, True)
            diagMove = arrToChessPos(x+1, y+1)
            diagMove2 = arrToChessPos(x-1, y+1)
            if (diagMove in dictOfWhitePieces):
                dictOfMyCover[diagMove] = 1
            if (diagMove2 in dictOfWhitePieces):
                dictOfMyCover[diagMove2] = 1
            if (diagMove in dictOfBlackPieces): #There is a piece to eat
                dictOfMoves[diagMove] = 1
                (pieceName, pieceColor) = dictOfBlackPieces.get(diagMove) #Adds piece to eat as higher priority.
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove))
                heapq.heappush(pqOfmoves, node)
            if (diagMove2 in dictOfBlackPieces):
                dictOfMoves[diagMove2] = 1
                (pieceName, pieceColor) = dictOfBlackPieces.get(diagMove2) #Adds piece to eat as higher priority.
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove2))
                heapq.heappush(pqOfmoves, node)
        else: #If black piece
            if (not onlyThreatPos):
                Moves.markDown(x, y-1, 1, dictOfMoves, color, pqOfmoves, pos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, True)
            diagMove = arrToChessPos(x+1, y-1)
            diagMove2 = arrToChessPos(x-1, y-1)
            if (diagMove in dictOfBlackPieces): # Check if I can cover myself.
                dictOfMyCover[diagMove] = 1
            if (diagMove2 in dictOfBlackPieces):
                dictOfMyCover[diagMove2] = 1
            if (diagMove in dictOfWhitePieces): #There is a piece to eat
                dictOfMoves[diagMove] = 1
                (pieceName, pieceColor) = dictOfWhitePieces.get(diagMove) #Adds piece to eat as higher priority.
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove))
                heapq.heappush(pqOfmoves, node)
            if (diagMove2 in dictOfWhitePieces):
                (pieceName, pieceColor) = dictOfWhitePieces.get(diagMove2) #Adds piece to eat as higher priority.
                dictOfMoves[diagMove2] = 1
                val = -getPieceValue(pieceName)
                node = (val, (pos, diagMove2))
                heapq.heappush(pqOfmoves, node)
        return
    
    def markUp(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, isPawn):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0):
            return
        if(isPawn):
            if ((pos in dictOfBlackPieces) or (pos in dictOfWhitePieces)): #if is pawn, infront is blocked 
                return
        if ((color == "White" and pos in dictOfWhitePieces) or (color == "Black" and pos in dictOfBlackPieces)): #Check if can cover myself.
            dictOfMyCover[pos] = 1
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
        Moves.markUp(x, y+1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, isPawn)

    def markDown(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, isPawn):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0):
            return
        if(isPawn):
            if ((pos in dictOfBlackPieces) or (pos in dictOfWhitePieces)): #if is pawn, infront is blocked 
                return
        if ((color == "White" and pos in dictOfWhitePieces) or (color == "Black" and pos in dictOfBlackPieces)): #Check if can cover myself.
            dictOfMyCover[pos] = 1
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
        Moves.markDown(x, y-1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover, isPawn)

    def markLeft(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfWhitePieces) or (color == "Black" and pos in dictOfBlackPieces)): #Check if can cover myself.
            dictOfMyCover[pos] = 1
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
        Moves.markLeft(x-1, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)

    def markRight(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfWhitePieces) or (color == "Black" and pos in dictOfBlackPieces)): #Check if can cover myself.
            dictOfMyCover[pos] = 1
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
        Moves.markRight(x+1, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)

    def markTopRight(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfWhitePieces) or (color == "Black" and pos in dictOfBlackPieces)): #Check if can cover myself.
            dictOfMyCover[pos] = 1
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
        Moves.markTopRight(x+1, y+1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)

    def markTopLeft(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfWhitePieces) or (color == "Black" and pos in dictOfBlackPieces)): #Check if can cover myself.
            dictOfMyCover[pos] = 1
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
        Moves.markTopLeft(x-1, y+1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)

    def markBotRight(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfWhitePieces) or (color == "Black" and pos in dictOfBlackPieces)): #Check if can cover myself.
            dictOfMyCover[pos] = 1
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
        Moves.markBotRight(x+1, y-1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        
    def markBotLeft(x, y, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0):
            return
        if ((color == "White" and pos in dictOfWhitePieces) or (color == "Black" and pos in dictOfBlackPieces)): #Check if can cover myself.
            dictOfMyCover[pos] = 1
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
        Moves.markBotLeft(x-1, y-1, numOfMoves, dictOfMoves, color, pqOfmoves, originPos, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)

#Prune if cur iter val <= minAlphaVal
def playerMin(minAlphaVal, maxBetaVal, totalMoves, dictOfWhitePieces, dictOfBlackPieces):
    minVal = 999999 #set to inf
    dictOfWhiteThreats = {}
    dictOfMoves = {} #{'a0' : ('Queen', listOfPossibleMoves)}
    pqOfMoves = [] #[(-10, ('a3', 'b3', "Queen")] (source, dest, Piece)
    heapq.heapify(pqOfMoves)
    dictOfMyCover = {}
    nextMove = (0,0)
    
    #Get list of moves
    for blackPos in dictOfBlackPieces:
        (blackPiece, color) = dictOfBlackPieces.get(blackPos) #example: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
        moves = getListOfMoves(blackPos, blackPiece, "Black", False, pqOfMoves, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        dictOfMoves[blackPos] = (blackPiece, moves)

    if (len(dictOfMoves) == 0):
        # Out of moves. Means draw
        return -1,nextMove
    
    terminalValue = isTerminal(totalMoves, "Black", dictOfWhitePieces, dictOfBlackPieces)
    if (terminalValue > 0): # 1 = No more moves, 2 = No king, 0 = not terminal
        paddingList = [] #can ignore
        dictOfEnemyCover = {}
        if (terminalValue == 2): # Terminated due to a king missing.
            return -1000,nextMove # I lost my king

        # Reached end of LDS. Need to get Current board value.
        for pos in dictOfBlackPieces: # Get the current threats for Opponent.
            (piece, color) = dictOfBlackPieces.get(pos)
            threats = getListOfMoves(pos, piece, "Black", True, paddingList, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover)
            dictOfWhiteThreats[pos] = threats # {'a0': list Of position he threatens}

        return getUtil("White", dictOfWhiteThreats, dictOfMoves, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover),nextMove
    
    #iterate thru list of possible moves from best to worst
    while(len(pqOfMoves) > 0):
        (cost, (sourcePos, destPos)) = heapq.heappop(pqOfMoves)
        tmpDictOfWhitePiece = copy.copy(dictOfWhitePieces)
        tmpDictOfBlackPiece = copy.copy(dictOfBlackPieces)
        transitionModel(sourcePos, destPos, tmpDictOfBlackPiece, tmpDictOfWhitePiece)
        curVal,hisMove = playerMax(minAlphaVal, maxBetaVal, totalMoves-1, tmpDictOfWhitePiece, tmpDictOfBlackPiece)
        
        if (curVal < minVal):
            if (curVal > maxBetaVal): #updates maxBeta Val
                maxBetaVal = curVal
                nextMove = (sourcePos, destPos)
            minVal = curVal
            if (minVal <= minAlphaVal): #Prune
                return (minVal,nextMove)
            
    return minVal,nextMove

#Prune if cur iter val >= maxBetaVal
# white Piece
def playerMax(minAlphaVal, maxBetaVal, totalMoves, dictOfWhitePieces, dictOfBlackPieces):
    maxVal = -999999 #set to -inf
    dictOfBlackThreats = {}
    dictOfMoves = {} #{'a0' : ('Queen', listOfPossibleMoves)}
    pqOfMoves = [] #[(-10, ('a3', 'b3', "Queen")] (source, dest, Piece)
    heapq.heapify(pqOfMoves)
    dictOfMyCover = {}
    nextMove = (0,0)

    #Get list of moves
    for whitePos in dictOfWhitePieces:
        (whitePiece, color) = dictOfWhitePieces.get(whitePos) #example: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
        moves = getListOfMoves(whitePos, whitePiece, "White", False, pqOfMoves, dictOfWhitePieces, dictOfBlackPieces, dictOfMyCover)
        dictOfMoves[whitePos] = (whitePiece, moves)

    if (len(dictOfMoves) == 0):
        # Out of moves. Means draw
        return -1, nextMove
    
    terminalValue = isTerminal(totalMoves, "White", dictOfWhitePieces, dictOfBlackPieces)
    if (terminalValue > 0): # 1 = No more moves, 2 = No king, 0 = not terminal
        paddingList = [] #can ignore
        dictOfEnemyCover = {}
        if (terminalValue == 2): # Terminated due to a king missing.
            return -1000, nextMove # I lost my king

        # Reached end of LDS. Need to get Current board value.
        for pos in dictOfBlackPieces: # Get the current threats for Opponent.
            (piece, color) = dictOfBlackPieces.get(pos)
            threats = getListOfMoves(pos, piece, "Black", True, paddingList, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover)
            dictOfBlackThreats[pos] = threats # {'a0': list Of position he threatens}

        return getUtil("White", dictOfBlackThreats, dictOfMoves, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover), nextMove
    
    #iterate thru list of possible moves from best to worst
    while(len(pqOfMoves) > 0):
        (cost, (sourcePos, destPos)) = heapq.heappop(pqOfMoves)
        tmpDictOfWhitePiece = copy.copy(dictOfWhitePieces)
        tmpDictOfBlackPiece = copy.copy(dictOfBlackPieces)
        transitionModel(sourcePos, destPos, tmpDictOfWhitePiece, tmpDictOfBlackPiece)
        curVal, hisMove = playerMin(minAlphaVal, maxBetaVal, totalMoves-1, tmpDictOfWhitePiece, tmpDictOfBlackPiece)
        #curVal = -curVal
        
        if (curVal > maxVal):
            if (curVal < minAlphaVal): #updates minAlpha Val
                minAlphaVal = curVal
                nextMove = (sourcePos, destPos)
            maxVal = curVal
            if (maxVal >= maxBetaVal): #Prune
                return maxVal, nextMove
            
    return maxVal, nextMove

# Ways to checkmate: Check if king can move out of the way OR get list of people threatens king & see if can eat any. OR see any local piece can block(Get from list of moves)
# Possible current util vaues: Checkmate -> capture and check -> Capture -> Check
# dictOfThreats = {'a0': list Of position he threatens, 'b0' : ....}
# Check = -6, Checkmate = -100
# dictOfPiece: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
# dict of my atk: {'a0': ('Queen', dict of position it threatens)}
def getUtil(color, dictOfEnemyThreats, dictOfMyAttacks, dictOfMyPiece, dictOfEnemyPiece, dictOfEnemyCover):
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
    
    if (numOfThreats > 0): # If true -> no checks against king
        isCheck = True

    # Get total value of people that was ate.
    if (color == "White"):
        numOfPiecesAte = len(Board.initialDictOfWhitePieces) - len(dictOfEnemyPiece)
        if (numOfPiecesAte > 0):
            hasEatPiece = True
            valueOfEatenPiece = getValueOfPiecesEatened(Board.initialDictOfWhitePieces, dictOfMyPiece)
    else:
        numOfPiecesAte = len(Board.initialDictOfBlackPieces) - len(dictOfEnemyPiece)
        if (numOfPiecesAte > 0):
            hasEatPiece = True
            valueOfEatenPiece = getValueOfPiecesEatened(Board.initialDictOfBlackPieces, dictOfMyPiece)

    # Checkmate -> capture and check -> Capture -> Check
    if (not hasEatPiece and not isCheck): # No eats or no checks
        return 0
    elif (not isCheck and hasEatPiece): # Only Ate
        return -(valueOfEatenPiece)
    
    # Try to escape first!
    nullList = [] #Just to fill up the parameter
    nullDict = {}
    dictOfPossibleKingMoves = {} #Possible moves for my own king
    if (color == "White"):
        Moves.markKingMove(kingPos, dictOfPossibleKingMoves, color, nullList, dictOfMyPiece, dictOfEnemyPiece, nullDict) #Get possible escapes
    else:
        Moves.markKingMove(kingPos, dictOfPossibleKingMoves, color, nullList, dictOfEnemyPiece, dictOfMyPiece, nullDict) #Get possible escapes
    canEscape = False
    
    for possibeEscape in list(dictOfPossibleKingMoves):
        isThreat = False
        for oppPos in dictOfEnemyThreats:
            enemyMoves = dictOfEnemyThreats.get(oppPos)
            if (possibeEscape in enemyMoves): #Enemy threatens one of my escape position, try next escape position.
                isThreat = True
                break
        if (isThreat == False): #no enemy threatens this escape position. Means can escape.
            canEscape = True
            isCheckmate = False
            break
        
    if (canEscape and hasEatPiece): # Can escape means no checkmate.
        return -(valueOfEatenPiece + 6)
    elif (canEscape and not hasEatPiece): # Can escape but never ate any means only check
        return -6
    
    #Unable to move out of the way, Try to eat it.
    if (numOfThreats == 1): # IF only 1 threat against King, can consider eating it to escape.
        isCheckmate = True
        (enemySourceAtk, ignoreVal) = dictOfPosAgainstKing.popitem()
        for ownPiecePos in dictOfMyAttacks: #Check if I am able to eat the king
            (pieceName, moves) = dictOfMyAttacks.get(ownPiecePos)
            if (enemySourceAtk in moves):
                if ((pieceName == "King") and (enemySourceAtk in dictOfEnemyCover)): #If I try to eat enemy using my king but it is guarded by 3rd piece somewhere else.
                    continue
                else : # I'm using piece other than my king to eat. Need to check if will still remian in check after eating.
                    tmpDictOfMyPiece = copy.copy(dictOfMyPiece)
                    tmpDictOfEnemyPiece = copy.copy(dictOfEnemyPiece)
                    transitionModel(ownPiecePos, enemySourceAtk, tmpDictOfMyPiece, tmpDictOfEnemyPiece) #Try out the moves
                    newDictOfThreats = {}
                    padLs = []
                    if (color == "White"):
                        for pos in tmpDictOfEnemyPiece: # Get the current threats for Opponent.
                            (piece, color) = tmpDictOfEnemyPiece.get(pos)
                            threats = getListOfMoves(pos, piece, "Black", True, padLs, dictOfEnemyPiece, dictOfMyPiece, dictOfEnemyCover)
                            newDictOfThreats[pos] = threats # {'a0': dict Of position he threatens}
                    else:
                        for pos in tmpDictOfEnemyPiece: # Get the current threats for Opponent.
                            (piece, color) = tmpDictOfEnemyPiece.get(pos)
                            threats = getListOfMoves(pos, piece, "White", True, padLs, dictOfMyPiece, dictOfEnemyPiece, dictOfEnemyCover)
                            newDictOfThreats[pos] = threats # {'a0': dict Of position he threatens}
                    
                    for updatedPos in newDictOfThreats:
                        newThreats = newDictOfThreats.get(updatedPos)
                        if (kingPos in newThreats): #King is still being threatened
                            isCheckmate = True
                            break
                        isCheckmate = False #still yet to find a threat against king
                        
                    if (isCheckmate == False):
                        break
                    
        if (not isCheckmate and isCheck and hasEatPiece ):
            return -(valueOfEatenPiece + 6)
        if (not isCheckmate and isCheck and not hasEatPiece):
            return -6
    
    return -100 #unable to eat, hence checkmate.
        
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

# dictOfPiece: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
def transitionModel(originPos, destPos, dictOfMyPieces, dictOfEnemyPieces):
    
    (myPieceName, myColor) = dictOfMyPieces.pop(originPos) #Moves my piece to next desired position.
    dictOfMyPieces[destPos] = (myPieceName, myColor)
    
    if (destPos in dictOfEnemyPieces): #Remove enemy Piece that i ate.
        dictOfEnemyPieces.pop(destPos)

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
    #Check for kings
    if (color == "Black"):
        for pos in dictOfBlackPieces:
            (pieceName, pieceColor) = dictOfBlackPieces.get(pos)
            if (pieceName == "King"):
                if (numOfmoves <= 0):
                    return 1 # Has king but no moves left
                else: # Has king and Has moves left.
                    return 0
        return 2 # No king left.
    else:
        for pos in dictOfWhitePieces:
            (pieceName, pieceColor) = dictOfWhitePieces.get(pos)
            if (pieceName == "King"):
                if (numOfmoves <= 0):
                    return 1 # Has king but no moves left
                else: # Has king and Has moves left.
                    return 0
        return 2 # No king left.

# list of moves returned. Moves can either eat or not eat. All are valid.
def getListOfMoves(pos, piece, color, onlyThreatFlag, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover):   
    dictOfMoves = {}
    if (piece == "Queen"):
        Moves.markQueenMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover)
    elif (piece == "Rook"):
        Moves.markRookMove(pos,dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover)
    elif (piece == "Bishop"):
        Moves.markBishopMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover)
    elif (piece == "Knight"):
        Moves.markKnightMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover)
    elif( piece == "King"):
        Moves.markKingMove(pos, dictOfMoves, color, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover)
    elif (piece == "Pawn"):
        Moves.markPawnMove(pos, color, dictOfMoves, onlyThreatFlag, pqOfmoves, dictOfWhitePieces, dictOfBlackPieces, dictOfEnemyCover)
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
        charPos = pos[0] + str(pos[1])
        if (color == "White"):
            dictOfWhitePieces[charPos] = data
            Board.initialDictOfWhitePieces[charPos] = data
        else:
            dictOfBlackPieces[charPos] = data
            Board.initialDictOfBlackPieces[charPos] = data
            
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

    dictOfWhitePieces = {} #example: {'a0' : ('Queen', 'White'), 'd0' : ('Knight', 'Black'), 'g25' : ('Rook', 'White')}
    dictOfBlackPieces = {}
    move = (None,None)

    initializBoard(gameboard, dictOfWhitePieces, dictOfBlackPieces) #Populate dict of white/black and curboard.
    (cost,move) = playerMax(1000000,-1000000,40,dictOfWhitePieces,dictOfBlackPieces)

    return move #Format to be returned (('a', 0), ('b', 3))

#print(studentAgent(Game.startGameBoard))