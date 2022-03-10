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
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        if (y > maxRow or y < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markUp(x, y+1, numOfMoves, dictOfCurBoard)

    def markDown(x, y, numOfMoves, dictOfCurBoard):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        if (y > maxRow or y < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3) :
            return False
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markDown(x, y-1, numOfMoves, dictOfCurBoard)

    def markLeft(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        if (x > maxCol or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markLeft(x-1, y, numOfMoves, dictOfCurBoard)

    def markRight(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        if (x > maxCol or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markRight(x+1, y, numOfMoves, dictOfCurBoard)

    def markTopRight(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markTopRight(x+1, y+1, numOfMoves, dictOfCurBoard)

    def markTopLeft(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markTopLeft(x-1, y+1, numOfMoves, dictOfCurBoard)

    def markBotRight(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
        dictOfCurBoard[pos] = -2
        numOfMoves-=1
        return Moves.markBotRight(x+1, y-1, numOfMoves, dictOfCurBoard)

    def markBotLeft(x, y, numOfMoves, dictOfCurBoard):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (dictOfCurBoard.get(pos,0) == -1):
            return True
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or dictOfCurBoard.get(pos,0) == -3):
            return False
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
    newSearch(dictOfCurBoard, Board.dictOfPieces, Board.countDict)
    return Board.dictOfPieces

def getNumOfPiece(name, dict):
    counter = 0
    for key in dict:
        val = dict.get(key)
        if (name == val):
            counter+=1
    return counter
    
def newSearch(dictOfCurBoard, dictOfPieces, dictOfNumberOfPiece):
        masterPQ = []
        heapq.heapify(masterPQ)
        if (len(dictOfPieces) == InitParams.totalOwnPiece): #Goal check.
            Board.dictOfPieces = dictOfPieces
            return True
        
        masterPQ = getLeastRemainingValuePos(dictOfCurBoard, dictOfNumberOfPiece)
        if (masterPQ == -1):
            return False #No more piece to put.
        
        curNumOfPc = 0
        
        for nameOfPiece in Board.listOfRemainingPieces: #Calc the current number of pieces on board
            curNumOfPc = curNumOfPc + getNumOfPiece(nameOfPiece,dictOfNumberOfPiece)
        
        while (len(masterPQ) > 0 and len(masterPQ) >= InitParams.totalOwnPiece - curNumOfPc):
            
            datas = heapq.heappop(masterPQ)
            (count, deg, packet) = datas
            (curPos, pqOfPiece) = packet
            #(curPos, pqOfPieces) = datas

            #pqOfPiece = getLeastConstrainValueVar(curPos, dictOfCurBoard, dictOfNumberOfPiece)
            trialBoard = copy.copy(dictOfCurBoard)
            trialDictOfPieces = copy.copy(dictOfPieces)
            trialDictOfNumberOfPieces = copy.copy(dictOfNumberOfPiece)
            while (len(pqOfPiece) > 0):
                #(val,curPc) = heapq.heappop(pqOfPiece)
                #hasFailed = checkAndPlacePiece(curPc, curPos, trialBoard)
                hasFailed = False
                (val,data) = heapq.heappop(pqOfPiece)
                (curPc, trialB) = data
                if (not hasFailed):
                    # Successful place
                    curTuple = (curPos[0], int(curPos[1:]))
                    trialDictOfPieces[curTuple] = curPc
                    trialDictOfNumberOfPieces[curPos] = curPc
                    print(trialDictOfPieces)
                    result = newSearch(trialB, trialDictOfPieces, trialDictOfNumberOfPieces) #change trialB to trial board
                    if (result):
                        return True
                    else:
                        trialBoard = copy.copy(dictOfCurBoard)
                        trialDictOfPieces = copy.copy(dictOfPieces)
                        trialDictOfNumberOfPieces = copy.copy(dictOfNumberOfPiece)
                # All options failed
                trialBoard[curPos] = 5 # 5 to means must be empty
        return #newSearch(trialBoard, dictOfPieces, dictOfNumberOfPiece)

def getLeastConstrainValueVar(pos, dictOfCurBoard, dictOfNumberOfPieces):
    curSpotLeft = 0
    listOfPc = []
    dictOfSumOfPiece = {}
    heapq.heapify(listOfPc)
    trialBoard = copy.copy(dictOfCurBoard)
    
    for nameOfPiece in Board.listOfRemainingPieces: #Calc the current number of pieces on board
        val = getNumOfPiece(nameOfPiece,dictOfNumberOfPieces)
        dictOfSumOfPiece[nameOfPiece] = val
        
    for nameOfPc in Board.listOfRemainingPieces:
        if (dictOfSumOfPiece.get(nameOfPc) >= Board.dictOfMaxPiece.get(nameOfPc)): #Check if num of piece has reached the max count
                continue
        if (not checkAndPlacePiece(nameOfPc, pos, trialBoard)):
            curSpotLeft = len(trialBoard)
            #node = (curSpotLeft, nameOfPc)
            data = (nameOfPc,trialBoard)
            node = (curSpotLeft,data)
            heapq.heappush(listOfPc,node)
        trialBoard = copy.copy(dictOfCurBoard)
    return listOfPc
        
def getLeastRemainingValuePos(dictOfCurBoard, dictOfNumberOfPieces):
    count = 0
    minCount = 99999
    x = 0
    y = 0
    listOfPos = []
    heapq.heapify(listOfPos)
    dictOfSumOfPiece = {}
    for nameOfPiece in Board.listOfRemainingPieces: #Calc the current number of pieces on board
        val = getNumOfPiece(nameOfPiece,dictOfNumberOfPieces)
        dictOfSumOfPiece[nameOfPiece] = val

    while (y <= Board.maxCols):
        pos = arrToChessPos(x, y)
        if (pos in dictOfCurBoard): #if position is blocked/threat (5 means allocated as empty)
            x+=1
            if (x > Board.maxCols):
                x = 0
                y+=1
            continue
            
        #Portion for LCV
        curSpotLeft = 0
        listOfPc = []
        heapq.heapify(listOfPc)

        for nameOfPiece in Board.listOfRemainingPieces:            
            if (dictOfSumOfPiece.get(nameOfPiece) >= Board.dictOfMaxPiece.get(nameOfPiece)): #Check if num of piece has reached the max count
                continue
            trialBoard = copy.copy(dictOfCurBoard)
            isNotValidPlace = checkAndPlacePiece(nameOfPiece, pos, trialBoard)
            if (not isNotValidPlace):
                count+=1
                #Portion for LCV
                curSpotLeft = len(trialBoard)
                data = (nameOfPiece,trialBoard)
                node = (curSpotLeft,data)
                heapq.heappush(listOfPc,node)
        if (count > 0):
            heapq.heappush(listOfPos,(count,(pos,listOfPc))) #count must be min
        # if (count == minCount and count > 0):
        #     listOfPos.append((pos,listOfPc))
        # elif (count < minCount and count > 0):
        #     listOfPos = []
        #     minCount = count
        #     listOfPos.append((pos,listOfPc))
        x+=1
        if (x > Board.maxCols):
            x = 0
            y+=1
        count = 0

    degree = 0
    maxDegree = 0
    finPos = []
    heapq.heapify(finPos)
    
    # Max Degree Heuristic
    for curData in listOfPos:
        (count, cur) = curData
        (curPos, ls) = cur 
        (x,y) = chessPosToArr(curPos)
        if (x + 1 <= Board.maxCols):
            incPos = arrToChessPos(x+1, y)
            val = dictOfCurBoard.get(incPos,0)
            if (not val == -3):
                degree+=1
        if (x + 1 <= Board.maxCols and y + 1 <= Board.maxRows):
            incPos = arrToChessPos(x+1, y+1)
            val = dictOfCurBoard.get(incPos,0)
            if (not val == -3):
                degree+=1
        if (y + 1 <= Board.maxRows):
            incPos = arrToChessPos(x, y+1)
            val = dictOfCurBoard.get(incPos,0)
            if (not val == -3):
                degree+=1
        if (x - 1 >= 0 and y + 1 <= Board.maxRows):
            incPos = arrToChessPos(x-1, y+1)
            val = dictOfCurBoard.get(incPos,0)
            if (not val == -3):
                degree+=1
        if (x - 1 >= 0):
            incPos = arrToChessPos(x-1, y)
            val = dictOfCurBoard.get(incPos,0)
            if (not val == -3):
                degree+=1
        if (x - 1 >= 0 and y - 1 >= 0):
            incPos = arrToChessPos(x-1, y-1)
            val = dictOfCurBoard.get(incPos,0)
            if (not val == -3):
                degree+=1
        if (y - 1 >= 0):
            incPos = arrToChessPos(x, y-1)
            val = dictOfCurBoard.get(incPos,0)
            if (not val == -3):
                degree+=1
        if (x + 1 <= Board.maxCols and y - 1 >= 0):
            incPos = arrToChessPos(x+1, y-1)
            val = dictOfCurBoard.get(incPos,0)
            if (not val == -3):
                degree+=1
        if (degree > 0):
            heapq.heappush(finPos, (count, -degree, (curPos,ls)))
        # if (degree > maxDegree and degree > 0):
        #     maxDegree = degree
        #     finPos = []
        #     finPos.append((curPos,ls))
        # elif (degree == maxDegree and degree != 0):
        #     finPos.append((curPos,ls))
        degree = 0
    
    if (len(finPos) == 0):
        return -1

    return finPos

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
    if (Board.dictOfMaxPiece.get("King") > 0):
        Board.listOfRemainingPieces.append("King")
    if (Board.dictOfMaxPiece.get("Knight") > 0):
        Board.listOfRemainingPieces.append("Knight")
    if (Board.dictOfMaxPiece.get("Rook") > 0):
        Board.listOfRemainingPieces.append("Rook")
    if (Board.dictOfMaxPiece.get("Bishop") > 0):
        Board.listOfRemainingPieces.append("Bishop")
    if (Board.dictOfMaxPiece.get("Queen") > 0):
        Board.listOfRemainingPieces.append("Queen")

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

print(run_CSP())