import random
import string
import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__(self, board, position, colour, piecesDict, value):
        self.chessBoard = board
        self.piecesDict = piecesDict
        board.board[position].isPiece = True
        self.position = position    #position = string(col+row)
        self.colour = colour
        self.value = value
        self.col = position[0]
        self.row = int(position[1:])

class Knight(Piece):
    def getMoveList(self):
        moveList = []
        captureList = []
        directionList = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]
        ogCol = ord(self.col)
        ogRow = self.row
        ownColour = self.colour
        for dir in directionList:
            currentCol = ogCol + dir[0]
            currentRow = ogRow + dir[1]
            positionStr = chr(currentCol) + str(currentRow)
            if (self.chessBoard.isAvailableSquare(chr(currentCol), currentRow)):
                moveList.append(positionStr)
            else: #Else if current position is not available
                #If position is within the board
                if self.chessBoard.isWithinBoard(chr(currentCol), currentRow):
                    #If there is a piece on it and piece is not the same colour as that of the current piece
                    if (self.chessBoard.board[positionStr].isPiece and self.piecesDict[positionStr].colour != ownColour):
                        captureList.append(positionStr)

        return moveList, captureList
        
class Rook(Piece):
    def getMoveList(self):
        moveList = []
        captureList = []
        directionList = [(0, -1), (1, 0), (0, 1), (-1, 0)]    #North, East, South, West
        ogCol = ord(self.col)
        ogRow = self.row
        ownColour = self.colour
        for dir in directionList:
            currentCol = ogCol + dir[0]
            currentRow = ogRow + dir[1]
            positionStr = chr(currentCol) + str(currentRow)
            while (self.chessBoard.isAvailableSquare(chr(currentCol), currentRow)):
                moveList.append(chr(currentCol) + str(currentRow))        
                currentCol = currentCol + dir[0]
                currentRow = currentRow + dir[1]

            positionStr = chr(currentCol) + str(currentRow)
            #If position is within the board
            if self.chessBoard.isWithinBoard(chr(currentCol), currentRow):
                #If there is a piece on it and piece is not the same colour as that of the current piece
                if (self.chessBoard.board[positionStr].isPiece and self.piecesDict[positionStr].colour != ownColour):
                    captureList.append(positionStr)

        return moveList, captureList

class Bishop(Piece):
    def getMoveList(self):
        moveList = []
        captureList = []
        directionList = [(1, -1), (1, 1), (-1, 1), (-1, -1)]    #NorthEast, SouthEast, SouthWest, NorthWest
        ogCol = ord(self.col)
        ogRow = self.row
        ownColour = self.colour
        for dir in directionList:
            currentCol = ogCol + dir[0]
            currentRow = ogRow + dir[1]
            while (self.chessBoard.isAvailableSquare(chr(currentCol), currentRow)):
                moveList.append(chr(currentCol) + str(currentRow))        
                currentCol = currentCol + dir[0]
                currentRow = currentRow + dir[1]
            
            positionStr = chr(currentCol) + str(currentRow)
            if self.chessBoard.isWithinBoard(chr(currentCol), currentRow):
                #If there is a piece on it and piece is not the same colour as that of the current piece
                if (self.chessBoard.board[positionStr].isPiece and self.piecesDict[positionStr].colour != ownColour):
                    captureList.append(positionStr)
        
        return moveList, captureList
        
class Queen(Piece):
    def getMoveList(self):
        moveList = []
        captureList = []
        directionList = [(1, -1), (1, 1), (-1, 1), (-1, -1), (0, -1), (1, 0), (0, 1), (-1, 0)] 
        ogCol = ord(self.col)
        ogRow = self.row
        ownColour = self.colour
        for dir in directionList:
            currentCol = ogCol + dir[0]
            currentRow = ogRow + dir[1]
            while (self.chessBoard.isAvailableSquare(chr(currentCol), currentRow)):
                moveList.append(chr(currentCol) + str(currentRow))        
                currentCol = currentCol + dir[0]
                currentRow = currentRow + dir[1]
            
            positionStr = chr(currentCol) + str(currentRow)
            if self.chessBoard.isWithinBoard(chr(currentCol), currentRow):
                #If there is a piece on it and piece is not the same colour as that of the current piece
                if (self.chessBoard.board[positionStr].isPiece and self.piecesDict[positionStr].colour != ownColour):
                    captureList.append(positionStr)
        
        return moveList, captureList
        
class King(Piece):
    def getMoveList(self):
        moveList = []
        captureList = []
        ownColour = self.colour
        for i in range(ord(self.col)-1 , ord(self.col) + 2):
            for j in range(self.row-1, self.row+2):
                positionStr = chr(i) + str(j)
                if ((self.chessBoard.isAvailableSquare(chr(i), j)) and ( (chr(i) + str(j)) != self.position) ):
                    moveList.append(positionStr)
                
                if self.chessBoard.isWithinBoard(chr(i), j):
                #If there is a piece on it and piece is not the same colour as that of the current piece
                    if (self.chessBoard.board[positionStr].isPiece and self.piecesDict[positionStr].colour != ownColour):
                        captureList.append(positionStr)
        
        return moveList, captureList
        
class Pawn(Piece):
    #New Piece to be implemented
     def getMoveList(self):
        moveList = []
        captureList = []
        ogCol = ord(self.col)
        ogRow = self.row
        ownColour = self.colour
        if self.colour == "White" :
            #Check if there is a piece in front
            if self.chessBoard.isAvailableSquare(chr(ogCol), ogRow + 1):
                moveList.append(chr(ogCol) + str(ogRow + 1))
            if self.chessBoard.isWithinBoard(chr(ogCol + 1), ogRow + 1) and self.chessBoard.board[chr(ogCol + 1) + str(ogRow + 1)].isPiece and self.piecesDict[chr(ogCol + 1) + str(ogRow + 1)].colour != ownColour:
                captureList.append(chr(ogCol + 1) + str(ogRow + 1))
            if self.chessBoard.isWithinBoard(chr(ogCol - 1), ogRow + 1) and self.chessBoard.board[chr(ogCol - 1) + str(ogRow + 1)].isPiece and self.piecesDict[chr(ogCol - 1) + str(ogRow + 1)].colour != ownColour:
                captureList.append(chr(ogCol - 1) + str(ogRow + 1))
        #if colour is black
        else:
            if self.chessBoard.isAvailableSquare(chr(ogCol), ogRow - 1):
                moveList.append(chr(ogCol) + str(ogRow - 1))
            if self.chessBoard.isWithinBoard(chr(ogCol + 1), ogRow - 1) and self.chessBoard.board[chr(ogCol + 1) + str(ogRow - 1)].isPiece and self.piecesDict[chr(ogCol + 1) + str(ogRow - 1)].colour != ownColour:
                captureList.append(chr(ogCol + 1) + str(ogRow - 1))
            if self.chessBoard.isWithinBoard(chr(ogCol - 1), ogRow - 1) and self.chessBoard.board[chr(ogCol - 1) + str(ogRow - 1)].isPiece and self.piecesDict[chr(ogCol - 1) + str(ogRow - 1)].colour != ownColour:
                captureList.append(chr(ogCol - 1) + str(ogRow - 1))
               
        return moveList, captureList

class Board:
    def __init__(self, numRows, numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.board = {}
        for i in range(0, numCols):
            colChar = string.ascii_lowercase[i]
            for j in range(0, numRows):
                positionStr = colChar + str(j)
                positionTuple = (colChar, j)
                self.board[positionStr] = Square(positionStr, False, False)

    def isWithinBoard(self, col, row):
        if (ord(col) < ord('a') or ord(col) >= ord('a') + self.numCols):
            return False
        if (row < 0 or row >= self.numRows):
            return False
        return True
    
    #Check if its an obstacle(not available)
    def isAvailableSquare(self, col, row):
        if (ord(col) < ord('a') or ord(col) >= ord('a') + self.numCols):
            return False
        if (row < 0 or row >= self.numRows):
            return False
        return not self.board[col+str(row)].isPiece

class Square:
    def __init__(self, position, isThreatened, isPiece):
        self.position = position
        self.isThreatened = isThreatened
        self.isPiece = isPiece

class Game:
    pass

class State:
    def __init__(self, piecesDict, chessBoard):
        self.piecesDict = piecesDict
        self.chessBoard = chessBoard
        self.piecesMoveDict = {}
        self.whitePiecesMoveDict = {}
        self.blackPiecesMoveDict = {}
        for item in self.piecesDict.items():
            positionStr = item[0]
            piece = item[1]
            self.piecesMoveDict[positionStr] = self.piecesDict[positionStr].getMoveList()
            if piece.colour == "White":
                self.whitePiecesMoveDict[positionStr] = self.piecesMoveDict[positionStr]
            elif piece.colour == "Black": 
                self.blackPiecesMoveDict[positionStr] = self.piecesMoveDict[positionStr]
    
    def getColourPiecesMoveDict(self, colour):
        if colour == "White": 
            return self.whitePiecesMoveDict
        return self.blackPiecesMoveDict

    def getKingPosition(self, colour):
        for key, value in self.piecesDict.items():
            if isinstance(value, King):
                if value.colour == colour:
                    return key          
        return False
    
    def isCheck(self, colour):
        positionsThreateningKing = []
        #Check if White King is checked
        if colour == "White":
            whiteKingPos = self.getKingPosition("White")
            for position, moves in self.blackPiecesMoveDict.items():
                captureMoves = moves[1]
                if whiteKingPos in captureMoves:
                    positionsThreateningKing.append(position)
        #Check if Black King is checked
        elif colour == "Black":
            blackKingPos = self.getKingPosition("Black")
            for position, moves in self.whitePiecesMoveDict.items():
                captureMoves = moves[1]
                if blackKingPos in captureMoves:
                    positionsThreateningKing.append(position)
        
        if len(positionsThreateningKing)!= 0:
            return True, positionsThreateningKing

        return False, positionsThreateningKing

    def getAllMoves(self, colour):
        allMovesList = []
        for position, piece in self.piecesDict.items():
            if piece.colour == colour: 
                pieceMoveList, pieceCaptureList = self.piecesMoveDict[position]
                for capture in pieceCaptureList:
                    score = 2
                    captureMoveTuple = (position, capture, score)
                    allMovesList.append(captureMoveTuple)
                for move in pieceMoveList:
                    score = 1
                    normalMoveTuple = (position, move, score)
                    allMovesList.append(normalMoveTuple)
        
        return sorted(allMovesList, key = lambda x: x[2], reverse=True)

    def getEvaluationFunction(self):
        whiteMaterialSum = 0
        blackMaterialSum = 0
        for position, piece in self.piecesDict.items():
            if piece.colour == "White":
                whiteMaterialSum += piece.value
            elif piece.colour == "Black":
                blackMaterialSum += piece.value

        evaluationFunction = whiteMaterialSum - blackMaterialSum
        return evaluationFunction

def isCheckMate(state, colour):
        #if unable to get coloured king's position -> coloured king has been eaten -> Gameover
        kingPosition = state.getKingPosition(colour)
        if not kingPosition:
            return True 
        return False

def copyPiecesDict(piecesDict):
    newPiecesDict = {}
    newChessBoard = Board(5,5)
    for position, piece in piecesDict.items():
        pieceType = piece.__class__.__name__
        colour = piece.colour
        newPiecesDict[position] = initialisePiece(pieceType, colour, position, newChessBoard, newPiecesDict)
    
    return newPiecesDict, newChessBoard

def movePiece(state, initialPos, destinationPos):
    
    #Get a copy of the current state piecesDict
    newStatePiecesDict = state.piecesDict.copy()
    
    #Pop the piece that is going to be moved
    poppedPiece = newStatePiecesDict.pop(initialPos)
    
    #Re-initialise all the pieces for the new state
    newStatePiecesDict, newStateChessBoard = copyPiecesDict(newStatePiecesDict)

    #Get the details of the piece that is going to be moved
    pieceType = poppedPiece.__class__.__name__
    colour = poppedPiece.colour
    position = destinationPos

    #Move the piece to its destinated position
    newStatePiecesDict[destinationPos] = initialisePiece(pieceType, colour, position, newStateChessBoard, newStatePiecesDict)

    #Initialise a new state
    newState = State(newStatePiecesDict, newStateChessBoard)

    return newState

def capturePiece(state, initialPos, destinationPos):

    #Get a copy of the current state piecesDict
    newStatePiecesDict = state.piecesDict.copy()
    
    #Pop the piece that is capturing
    capturingPiece = newStatePiecesDict.pop(initialPos)

    #Pop the piece that is going to be captured
    capturedPiece = newStatePiecesDict.pop(destinationPos)
    
    #Re-initialise all the pieces for the new state
    newStatePiecesDict, newStateChessBoard = copyPiecesDict(newStatePiecesDict)

    #Get the details of the piece that is going to be moved
    pieceType = capturingPiece.__class__.__name__
    colour = capturingPiece.colour
    position = destinationPos

    #Move the piece to its destinated position
    newStatePiecesDict[destinationPos] = initialisePiece(pieceType, colour, position, newStateChessBoard, newStatePiecesDict)

    #Initialise a new state
    newState = State(newStatePiecesDict, newStateChessBoard)

    return newState

def generateNextStates(state, colour):
    nextStatesList = []
    nextMoves = state.getAllMoves(colour)
    
    for move in nextMoves:
        initialPos = move[0]
        destinationPos = move[1]
        score = move[2]
        if score == 2:
            nextState = capturePiece(state, initialPos, destinationPos)
        elif score == 1:
            nextState = movePiece(state, initialPos, destinationPos)
    
    nextStatesList.append(nextState)
    return nextStatesList

#Implement your minimax with alpha-beta pruning algorithm here.
def ab(state, depth, alpha, beta, isMax):
    if depth == 0 or isCheckMate(state, "White") or isCheckMate(state, "Black"):
        return None, state.getEvaluationFunction()

    colour = ""
    if isMax:
        colour = "White"
    else:
        colour = "Black"

    nextMoves = state.getAllMoves(colour)
    bestMove = random.choice(nextMoves)

    if isMax:
        maxUtility = -float('inf')
        for move in nextMoves:
            initialPos = move[0]
            destinationPos = move[1]
            score = move[2]
            if score == 2:
                nextState = capturePiece(state, initialPos, destinationPos)
            elif score == 1:
                nextState = movePiece(state, initialPos, destinationPos)

            currUtility = ab(nextState, depth - 1, alpha, beta, False)[1]

            if (currUtility > maxUtility):
                maxUtility = currUtility
                bestMove = move

            alpha = max(alpha, currUtility)
            if alpha >= beta:
                break

        return bestMove, maxUtility

    else: 
        minUtility = float('inf')
        for move in nextMoves:
            initialPos = move[0]
            destinationPos = move[1]
            score = move[2]
            if score == 2:
                nextState = capturePiece(state, initialPos, destinationPos)
            elif score == 1:
                nextState = movePiece(state, initialPos, destinationPos)

            currUtility = ab(nextState, depth -1, alpha, beta, True)[1]

            if (currUtility < minUtility):
                minUtility = currUtility
                bestMove = move

            beta = min(beta, currUtility)
            if alpha >= beta:
                break
        return bestMove, minUtility

def parseGameboard(gameboard):
    piecesDict = {}
    chessBoard = Board(5,5)
    for key in gameboard.keys():
        positionStr = key[0] + str(key[1])
        piecesDict[positionStr] = initialisePiece(gameboard[key][0], gameboard[key][1], positionStr, chessBoard, piecesDict)
    
    return piecesDict, chessBoard

def initialisePiece(pieceType, colour, position, chessBoard, piecesDict):
    if pieceType == "King":
        return King(chessBoard, position, colour, piecesDict, 200000)
    elif pieceType == "Queen":
        return Queen(chessBoard, position, colour, piecesDict, 900)
    elif pieceType == "Bishop":
        return Bishop(chessBoard, position, colour, piecesDict, 330)
    elif pieceType == "Rook":
        return Rook(chessBoard, position, colour, piecesDict, 500)
    elif pieceType == "Knight":
        return Knight(chessBoard, position, colour, piecesDict, 320)
    elif pieceType == "Pawn":
        return Pawn(chessBoard, position, colour, piecesDict, 100)

def formatMove(move):
    initialPos = move[0]
    destinationPos = move[1]

    return ((initialPos[0], int(initialPos[1:])), (destinationPos[0], int(destinationPos[1:])))


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

    piecesDict, chessBoard = parseGameboard(gameboard)
    currentState = State(piecesDict, chessBoard)
    depth = 3

    bestState, utility = ab(currentState, depth, -float('inf'), float('inf'), True)

    move = formatMove(bestState)
    return move #Format to be returned (('a', 0), ('b', 3))

initialBoard = {('a', 0) : ('Rook', 'White'), ('b', 0) : ('Knight', 'White'), ('c', 0) : ('Bishop', 'White'), ('d', 0) : ('Queen', 'White'), ('e', 0) : ('King', 'White'),
('a', 1) : ('Pawn', 'White'), ('b', 1) : ('Pawn', 'White'), ('c', 1) : ('Pawn', 'White'), ('d', 1) : ('Pawn', 'White'), ('e', 1) : ('Pawn', 'White'),
('a', 3) : ('Pawn', 'Black'), ('b', 3) : ('Pawn', 'Black'), ('c', 3) : ('Pawn', 'Black'), ('d', 3) : ('Pawn', 'Black'), ('e', 3) : ('Pawn', 'Black'),
('a', 4) : ('Rook', 'Black'), ('b', 4) : ('Knight', 'Black'), ('c', 4) : ('Bishop', 'Black'), ('d', 4) : ('Queen', 'Black'), ('e', 4) : ('King', 'Black')}

startingState = {('e', 0): ('King', 'White'),
                     ('c', 0): ('Queen', 'White'),
                     ('d', 2): ('Pawn', 'White'),

                     ('c', 3): ('Pawn', 'Black'),
                     ('d', 4): ('King', 'Black')
                     }

print(studentAgent(startingState))