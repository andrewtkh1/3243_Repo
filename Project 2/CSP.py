import copy
import heapq
import heapq
import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

class InitParams:
    # Class level var
    rows = 0
    cols = 0
    noOfObj = 0
    totalOwnPiece = 0
    listOfObjPos = []
    kValue = 10
    dictOfOwnPos = {'King': [], 'Queen':[], 'Bishop': [], 'Rook': [], 'Knight': []}
    dictOfObsOnBoard = {}

class Board:
    samePieceFlag = 0
    samePieceDict = []
    dictOfPriority = {'King': 4, 'Queen':0, 'Bishop': 2, 'Rook': 1, 'Knight': 3}
    maxRows = 0
    maxCols = 0
    totalThreat = 0
    dictOfMaxPiece = {}
    dictOfPieces = {}
    dictOfObs = {}
    dictOfThreat = {} #Format = {'a0': {a1:1 ,a2:1}, ... }, a0 is threatened by a1 & a2. Dict within a dict
    dictOfRemovedPieces = {} #Pieces that have been removed from board.
    #dictOfRemainingPieces = {}
    dictOfNumberOfPiece  = {'King': {}, 'Queen':{}, 'Bishop': {}, 'Rook': {}, 'Knight': {}}
    countDict = {}
    listOfRemainingPieces = []
    isValid = 0

class Moves:        
    def markKnightMove(pos, dictOfCurBoard):
        (x,y) = chessPosToArr(pos)
        dictOfCurBoard[pos] = -1
        if (Moves.markTopRight(x+2, y+1, 1, dictOfCurBoard) or Moves.markTopRight(x+1, y+2, 1, dictOfCurBoard) or Moves.markTopRight(x-2, y+1, 1, dictOfCurBoard)
            or Moves.markTopRight(x-1, y+2, 1, dictOfCurBoard) or Moves.markTopRight(x-2, y-1, 1, dictOfCurBoard) or Moves.markTopRight(x-1, y-2, 1, dictOfCurBoard)
            or Moves.markTopRight(x+2, y-1, 1, dictOfCurBoard) or Moves.markTopRight(x+1, y-2, 1, dictOfCurBoard)):
            return True        
            
    def markRookMove(pos, dictOfCurBoard):
        (x,y) = chessPosToArr(pos)
        dictOfCurBoard[pos] = -1
        if (Moves.markUp(x,y+1,-1, dictOfCurBoard) or Moves.markDown(x, y-1, -1, dictOfCurBoard) or Moves.markLeft(x-1, y, -1, dictOfCurBoard)
            or Moves.markRight(x+1, y, -1, dictOfCurBoard)):
            return True
    
    def markBishopMove(pos, dictOfCurBoard):
        dictOfCurBoard[pos] = -1
        (x,y) = chessPosToArr(pos)
        if (Moves.markTopRight(x+1, y+1, -1, dictOfCurBoard) or Moves.markTopLeft(x-1, y+1, -1, dictOfCurBoard)
            or Moves.markBotRight(x+1, y-1, -1, dictOfCurBoard) or Moves.markBotLeft(x-1, y-1, -1, dictOfCurBoard)):
            return True      
            
    def markQueenMove(pos, dictOfCurBoard):
        (x,y) = chessPosToArr(pos)
        dictOfCurBoard[pos] = -1
        if (Moves.markUp(x, y+1, -1, dictOfCurBoard) or Moves.markDown(x, y-1, -1, dictOfCurBoard) or Moves.markLeft(x-1, y, -1, dictOfCurBoard)
            or Moves.markRight(x+1, y, -1, dictOfCurBoard) or Moves.markTopRight(x+1, y+1, -1, dictOfCurBoard) or Moves.markTopLeft(x-1, y+1, -1, dictOfCurBoard)
            or Moves.markBotRight(x+1, y-1, -1, dictOfCurBoard) or Moves.markBotLeft(x-1, y-1, -1, dictOfCurBoard)):
            return True

    def markKingMove(pos, dictOfCurBoard):
        dictOfCurBoard[pos] = -1
        (x,y) = chessPosToArr(pos)
        if (Moves.markUp(x, y+1, 1, dictOfCurBoard) or Moves.markDown(x, y-1, 1, dictOfCurBoard) or Moves.markLeft(x-1, y, 1, dictOfCurBoard)
            or Moves.markRight(x+1, y, 1, dictOfCurBoard) or Moves.markTopRight(x+1, y+1, 1, dictOfCurBoard) or Moves.markTopLeft(x-1, y+1, 1, dictOfCurBoard)
            or Moves.markBotRight(x+1, y-1, 1, dictOfCurBoard) or Moves.markBotLeft(x-1, y-1, 1, dictOfCurBoard)):
            return True
            
    def markUp(x, y, numOfMoves, dictOfCurBoard):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        while not (y > maxRow or y < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            pos = arrToChessPos(x,y)
            if (dictOfCurBoard.get(pos,0) == -1):
                return True
            dictOfCurBoard[pos] = -2
            numOfMoves-=1
            y+=1
        return False
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3): #-3 is obstacles
            return False
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markUp(x, y+1, numOfMoves, dictOfCurBoard)

    def markDown(x, y, numOfMoves, dictOfCurBoard):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        while(not(y > maxRow or y < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3)):
            pos = arrToChessPos(x,y)
            if (dictOfCurBoard.get(pos,0) == -1):
                return True
            dictOfCurBoard[pos] = -2
            numOfMoves-=1
            y-=1
        return False
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3) :
            return False
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markDown(x, y-1, numOfMoves, dictOfCurBoard)

    def markLeft(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        while not (x > maxCol or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            pos = arrToChessPos(x,y)
            if (dictOfCurBoard.get(pos,0) == -1):
                return True
            dictOfCurBoard[pos] = -2
            numOfMoves-=1
            x-=1
        return False
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markLeft(x-1, y, numOfMoves, dictOfCurBoard)

    def markRight(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        while not (x > maxCol or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            pos = arrToChessPos(x,y)
            if (dictOfCurBoard.get(pos,0) == -1):
                return True
            dictOfCurBoard[pos] = -2
            numOfMoves-=1
            x+=1
        return False
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markRight(x+1, y, numOfMoves, dictOfCurBoard)

    def markTopRight(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        while not (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            pos = arrToChessPos(x,y)
            if (dictOfCurBoard.get(pos,0) == -1):
                return True
            dictOfCurBoard[pos] = -2
            numOfMoves-=1
            x+=1
            y+=1
        return False
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markTopRight(x+1, y+1, numOfMoves, dictOfCurBoard)

    def markTopLeft(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        while not  (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            pos = arrToChessPos(x,y)
            if (dictOfCurBoard.get(pos,0) == -1):
                return True
            dictOfCurBoard[pos] = -2
            numOfMoves-=1
            x-=1
            y+=1
        return False
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markTopLeft(x-1, y+1, numOfMoves, dictOfCurBoard)

    def markBotRight(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        while not (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            pos = arrToChessPos(x,y)
            if (dictOfCurBoard.get(pos,0) == -1):
                return True
            dictOfCurBoard[pos] = -2
            numOfMoves-=1
            x+=1
            y-=1
        return False
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markBotRight(x+1, y-1, numOfMoves, dictOfCurBoard)

    def markBotLeft(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        while not (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            pos = arrToChessPos(x,y)
            if (dictOfCurBoard.get(pos,0) == -1):
                return True
            dictOfCurBoard[pos] = -2
            numOfMoves-=1
            x-=1
            y-=1
        return False
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markBotLeft(x-1, y-1, numOfMoves, dictOfCurBoard)

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
    fileText = open(testfile, 'r')
    read_input(fileText)
    Board.maxCols = InitParams.cols - 1
    Board.maxRows = InitParams.rows - 1
    dictOfCurBoard = InitParams.dictOfObsOnBoard
    search(dictOfCurBoard, Board.dictOfPieces, Board.countDict)
    return Board.dictOfPieces

def getNumOfPiece(name, dict):
    counter = 0
    for key in dict:
        val = dict.get(key)
        if (name == val):
            counter+=1
    return counter
    
def search(dictOfCurBoard, dictOfPieces, dictOfNumberOfPiece):
    
    if (len(dictOfPieces) == InitParams.totalOwnPiece): #Goal check.
        Board.dictOfPieces = dictOfPieces
        return True
    
    numOfRemainPc = InitParams.totalOwnPiece - len(dictOfPieces)
    totalPos = InitParams.rows * InitParams.cols
    remainPos = totalPos - len(dictOfCurBoard)
    
    if (numOfRemainPc > remainPos): # Number of piece left is more than remaining spots
        return False
    
    lsOfSpots = []
    heapq.heapify(lsOfSpots)
        
    pieceList = getLeastRemainingValuePos(dictOfCurBoard, dictOfNumberOfPiece, dictOfPieces)
    if (pieceList == -1): #No valid assignment of piece
        return False
    (noOfPosValid, priority, data) = pieceList
    (nameOfPiece, lsOfSpots) = data
    
    trialDictOfPieces = copy.copy(dictOfPieces)
    trialDictOfNumberOfPieces = copy.copy(dictOfNumberOfPiece)
    
    #lsOfSpots = getLeastConstrainValueVar(nameOfPiece, dictOfCurBoard) #This line is to get Least Const value. Not necessary as alr done in leastRemainingValuePos function.
    #print(lsOfSpots)
    while (len(lsOfSpots) > 0):
        vertex = heapq.heappop(lsOfSpots)
        (numOfPosBlocked, node) = vertex
        (pos, preDoneBoard) = node
        curTuple = (pos[0], int(pos[1:]))
        trialDictOfPieces[curTuple] = nameOfPiece #Dict to print
        trialDictOfNumberOfPieces[pos] = nameOfPiece #Dict to keep track of what pieces are on the board.        
        #print(trialDictOfPieces)
        result = search(preDoneBoard, trialDictOfPieces, trialDictOfNumberOfPieces) #change trialB to trial board
        if (result):
            return True
        Board.samePieceDict.append(trialDictOfPieces)
        trialDictOfPieces = copy.copy(dictOfPieces)
        trialDictOfNumberOfPieces = copy.copy(dictOfNumberOfPiece)
        
    return False

# Changed to piece. For each piece, calc how many spots on the board is valid for it. Get piece with the min.
# Return (numOfPositionsValid, Board.dictOfPriority.get(uniquePiece), (uniquePiece, listOfSpots))
# lsOfSpots is =  node = (numOfPosBlocked,data), data = (pos,trialBoard)
def getLeastRemainingValuePos(dictOfCurBoard, dictOfNumberOfPieces, dictOfPieces):
    numOfPositionsValid = 0
    listOfPcs = []
    heapq.heapify(listOfPcs)
    dictOfSumOfPiece = {}
    dictOfDistinctPiece = {}
    
    minNumOfPos = (InitParams.cols * InitParams.rows) + 1
    bestPiece = -1
    bestPiecePosLs = -1
    
    for nameOfPiece in Board.listOfRemainingPieces: #Calc the current number of pieces on board
        val = getNumOfPiece(nameOfPiece,dictOfNumberOfPieces)
        if (dictOfDistinctPiece.get(nameOfPiece,"0") == "0"): # Add each unique piece.
            dictOfDistinctPiece[nameOfPiece] = -1
        dictOfSumOfPiece[nameOfPiece] = val
        
    ls = ["Queen", "Bishop", "Rook", "Knight", "King"]
    for uniquePiece in dictOfSumOfPiece:
        x = 0
        y = 0
        
        if (dictOfSumOfPiece.get(uniquePiece,0) >= Board.dictOfMaxPiece.get(uniquePiece,0)): #Check if num of piece has reached the max count
            continue
        
        listOfSpots = []
        heapq.heapify(listOfSpots)
        while (y <= Board.maxCols):
            pos = arrToChessPos(x, y)                
            if (pos in dictOfCurBoard): #if position is blocked/threat
                x+=1
                if (x > Board.maxCols):
                    x = 0
                    y+=1
                continue
            
            if (Board.samePieceFlag):#(len(dictOfPieces) == InitParams.totalOwnPiece - 1):
                flag = 0
                curTuple = (pos[0], int(pos[1:]))
                dictOfPieces[curTuple] = nameOfPiece #Dict to print
                for i in range(len(Board.samePieceDict)):
                    if (dictOfPieces == Board.samePieceDict[i]):
                        flag = 1
                        break
                dictOfPieces.pop(curTuple)
                if (flag == 1):
                    x+=1
                    if (x > Board.maxCols):
                        x = 0
                        y+=1
                    continue
            
            #Portion for LCV
            trialBoard = copy.copy(dictOfCurBoard)
            isNotValidPlace = checkAndPlacePiece(uniquePiece, pos, trialBoard)
            if (not isNotValidPlace):
                numOfPositionsValid+=1
                #Portion for LCV
                numOfPosBlocked = len(trialBoard)
                data = (pos,trialBoard)
                node = (numOfPosBlocked,data) # We want the least number of spots taken
                if (Board.samePieceFlag): # Do not re-try the same spots.
                    #Board.samePieceDict[pos] = -1
                    pass
                heapq.heappush(listOfSpots,node)
            x+=1
            if (x > Board.maxCols):
                x = 0
                y+=1
        if (numOfPositionsValid == 0):
            return -1        
        if (numOfPositionsValid > 0 and numOfPositionsValid <= minNumOfPos):
                # Priority is for max degree Heuristic.
                if (numOfPositionsValid < minNumOfPos):
                    (bestPiece, bestPiecePosLs) = uniquePiece, listOfSpots
                elif (Board.dictOfPriority.get(bestPiece) > Board.dictOfPriority.get(uniquePiece)):
                    (bestPiece, bestPiecePosLs) = uniquePiece, listOfSpots
                #heapq.heappush(listOfPcs,(numOfPositionsValid,Board.dictOfPriority.get(uniquePiece),(uniquePiece,listOfSpots))) #count must be min        
        numOfPositionsValid = 0
    if (bestPiece == -1):
        return -1
    # if (len(listOfPcs) == 0):
    #      return -1
    return (0,0,(bestPiece, bestPiecePosLs))
    return heapq.heappop(listOfPcs)

def checkAndPlacePiece(piece, pos, dictOfCurBoard):
    status = False #True means is not valid place.
    if (piece == "King"):
        status = Moves.markKingMove(pos, dictOfCurBoard)
    elif (piece == "Knight"):
        status = Moves.markKnightMove(pos,dictOfCurBoard)
    elif (piece == "Rook"):
        status = Moves.markRookMove(pos, dictOfCurBoard)
    elif (piece == "Bishop"):
        status = Moves.markBishopMove(pos,dictOfCurBoard)
    elif (piece == "Queen"):
        status = Moves.markQueenMove(pos, dictOfCurBoard)
    return status

def read_input(f):
    lineState = 0
    for curLine in f:
        if ':' in curLine:
            lineState += 1
        if lineState == 1:
            InitParams.rows = getRowOrColOrObs(curLine)
        elif lineState == 2:
            InitParams.cols = getRowOrColOrObs(curLine)
        elif lineState == 3:
            InitParams.noOfObj = getRowOrColOrObs(curLine)
        elif lineState == 4:
            #Get position of obs in list
            InitParams.listOfObjPos = getObjPos(curLine)
            for a in InitParams.listOfObjPos:
                InitParams.dictOfObsOnBoard[a] = -3
        elif lineState == 5:
            #Get Number Of each peices on the board
            InitParams.totalOwnPiece = getNumerOfEnemyOrOwn(curLine)
        else:
            pass

def addObjToBoard():
    for obs in InitParams.dictOfObsOnBoard:
        Board.dictOfObs[obs] = -3

#Returns row/col/# of obs
def getRowOrColOrObs(string) -> int:
    try:
        idx = string.index(':') + 1
        val = int(string[idx:])
    except Exception:
        #print("Error in geting Row/Col/# of obs")
        sys.exit()
    return val

#Returns list of Obj Pos in a list
def getObjPos(string) -> list:
    if (InitParams.noOfObj == 0):
        return []
    idx = string.index(':') + 1
    valOnlyStr = string[idx:]
    valOnlyStr = valOnlyStr.strip()
    listOfVal = list(valOnlyStr.split(" "))
    return listOfVal

#Get total number of Enemy pieces
def getNumerOfEnemyOrOwn(string) -> int:
    idx = string.index(':') + 1
    valOnlyStr = string[idx:].strip()
    listOfvals = list(valOnlyStr.split(" "))
    Board.dictOfMaxPiece["King"] = int(listOfvals[0])
    Board.dictOfMaxPiece["Queen"] = int(listOfvals[1])
    Board.dictOfMaxPiece["Bishop"] = int(listOfvals[2])
    Board.dictOfMaxPiece["Rook"] = int(listOfvals[3])
    Board.dictOfMaxPiece["Knight"] = int(listOfvals[4])
    count = 0
    fillListOfPieces()
    for i in listOfvals:            
        count += int(i)
    return count

def fillListOfPieces():
    noOfDistinctPc = 0
    if (Board.dictOfMaxPiece.get("King") > 0):
        noOfDistinctPc+=1
        Board.listOfRemainingPieces.append("King")
    if (Board.dictOfMaxPiece.get("Knight") > 0):
        noOfDistinctPc+=1
        Board.listOfRemainingPieces.append("Knight")
    if (Board.dictOfMaxPiece.get("Rook") > 0):
        noOfDistinctPc+=1
        Board.listOfRemainingPieces.append("Rook")
    if (Board.dictOfMaxPiece.get("Bishop") > 0):
        noOfDistinctPc+=1
        Board.listOfRemainingPieces.append("Bishop")
    if (Board.dictOfMaxPiece.get("Queen") > 0):
        noOfDistinctPc+=1
        Board.listOfRemainingPieces.append("Queen")
    if (noOfDistinctPc == 1): # Indicate that there is onyl 1 type of piece in the board.
        Board.samePieceFlag = 1

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

#print(run_CSP())