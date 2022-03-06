from cmath import pi
import sys
import copy

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
# Iteration that uses new Dict as marking, Visted dict as been moved out. Only Shallow Copy Path Taken
# Class to contain all data from input file

#Flow of search. setup -> populate dict of position that are threatend by others -> Pick piece with most number of threat against him -> Update all pieces on who threat who -> repeat

class Moves:        
    def markKnightMove(listOfPos):
        for pos in listOfPos:
            (x,y) = chessPosToArr(pos)
            Moves.markTopRight(x+2, y+1, 1, pos)
            Moves.markTopRight(x+1, y+2, 1, pos)
            Moves.markTopRight(x-2, y+1, 1, pos)
            Moves.markTopRight(x-1, y+2, 1, pos)
            Moves.markTopRight(x-2, y-1, 1, pos)
            Moves.markTopRight(x-1, y-2, 1, pos)
            Moves.markTopRight(x+2, y-1, 1, pos)
            Moves.markTopRight(x+1, y-2, 1, pos)
            
    def markRookMove(listOfPos):
        for pos in listOfPos:
            (x,y) = chessPosToArr(pos)
            Moves.markUp(x,y+1,-1, pos)
            Moves.markDown(x, y-1, -1, pos)
            Moves.markLeft(x-1, y, -1, pos)
            Moves.markRight(x+1, y, -1, pos)
    
    def markBishopMove(listOfPos):
        for pos in listOfPos:
            (x,y) = chessPosToArr(pos)
            Moves.markTopRight(x+1, y+1, -1, pos)
            Moves.markTopLeft(x-1, y+1, -1, pos)
            Moves.markBotRight(x+1, y-1, -1, pos)
            Moves.markBotLeft(x-1, y-1, -1, pos)
            
    def markQueenMove(listOfPos):
        for pos in listOfPos:
            (x,y) = chessPosToArr(pos)
            Moves.markUp(x, y+1, -1, pos)
            Moves.markDown(x, y-1, -1, pos)
            Moves.markLeft(x-1, y, -1, pos)
            Moves.markRight(x+1, y, -1, pos)
            Moves.markTopRight(x+1, y+1, -1, pos)
            Moves.markTopLeft(x-1, y+1, -1, pos)
            Moves.markBotRight(x+1, y-1, -1, pos)
            Moves.markBotLeft(x-1, y-1, -1, pos)
    
    def markKingMove(listOfPos):
        for pos in listOfPos:
            (x,y) = chessPosToArr(pos)
            Moves.markUp(x, y+1, 1, pos)
            Moves.markDown(x, y-1, 1, pos)
            Moves.markLeft(x-1, y, 1, pos)
            Moves.markRight(x+1, y, 1, pos)
            Moves.markTopRight(x+1, y+1, 1, pos)
            Moves.markTopLeft(x-1, y+1, 1, pos)
            Moves.markBotRight(x+1, y-1, 1, pos)
            Moves.markBotLeft(x-1, y-1, 1, pos)
    
    def markUp(x, y, numOfMoves, originPos):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0 or (pos in Board.dictOfObs)):
            return
        curThreatDict = Board.dictOfThreat.get(pos, -1)
        if (curThreatDict == -1): #Threatend position is new
            newDict = {originPos:{-1}}
            Board.dictOfThreat[pos] = newDict
        else: #position alr has other threats
            curThreatDict[originPos] = -1
            Board.dictOfThreat[pos] = curThreatDict
        numOfMoves-=1
        Moves.markUp(x, y+1, numOfMoves, originPos)

    def markDown(x, y, numOfMoves, originPos):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0 or (pos in Board.dictOfObs)):
            return
        curThreatDict = Board.dictOfThreat.get(pos, -1)
        if (curThreatDict == -1): #Threatend position is new
            newDict = {originPos:{-1}}
            Board.dictOfThreat[pos] = newDict
        else: #position alr has other threats
            curThreatDict[originPos] = -1
            Board.dictOfThreat[pos] = curThreatDict
        numOfMoves-=1
        Moves.markDown(x, y-1, numOfMoves, originPos)

    def markLeft(x, y, numOfMoves, originPos):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0 or (pos in Board.dictOfObs)):
            return
        curThreatDict = Board.dictOfThreat.get(pos, -1)
        if (curThreatDict == -1): #Threatend position is new
            newDict = {originPos:{-1}}
            Board.dictOfThreat[pos] = newDict
        else: #position alr has other threats
            curThreatDict[originPos] = -1
            Board.dictOfThreat[pos] = curThreatDict
        numOfMoves-=1
        Moves.markLeft(x-1, y, numOfMoves, originPos)

    def markRight(x, y, numOfMoves, originPos):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0 or (pos in Board.dictOfObs)):
            return
        curThreatDict = Board.dictOfThreat.get(pos, -1)
        if (curThreatDict == -1): #Threatend position is new
            newDict = {originPos:{-1}}
            Board.dictOfThreat[pos] = newDict
        else: #position alr has other threats
            curThreatDict[originPos] = -1
            Board.dictOfThreat[pos] = curThreatDict
        numOfMoves-=1
        Moves.markRight(x+1, y, numOfMoves, originPos)

    def markTopRight(x, y, numOfMoves, originPos):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or (pos in Board.dictOfObs)):
            return
        curThreatDict = Board.dictOfThreat.get(pos, -1)
        if (curThreatDict == -1): #Threatend position is new
            newDict = {originPos:{-1}}
            Board.dictOfThreat[pos] = newDict
        else: #position alr has other threats
            curThreatDict[originPos] = -1
            Board.dictOfThreat[pos] = curThreatDict
        numOfMoves-=1
        Moves.markTopRight(x+1, y+1, numOfMoves, originPos)

    def markTopLeft(x, y, numOfMoves, originPos):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or (pos in Board.dictOfObs)):
            return
        curThreatDict = Board.dictOfThreat.get(pos, -1)
        if (curThreatDict == -1): #Threatend position is new
            newDict = {originPos:{-1}}
            Board.dictOfThreat[pos] = newDict
        else: #position alr has other threats
            curThreatDict[originPos] = -1
            Board.dictOfThreat[pos] = curThreatDict
        numOfMoves-=1
        Moves.markTopLeft(x-1, y+1, numOfMoves, originPos)

    def markBotRight(x, y, numOfMoves, originPos):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or (pos in Board.dictOfObs)):
            return
        curThreatDict = Board.dictOfThreat.get(pos, -1)
        if (curThreatDict == -1): #Threatend position is new
            newDict = {originPos:{-1}}
            Board.dictOfThreat[pos] = newDict
        else: #position alr has other threats
            curThreatDict[originPos] = -1
            Board.dictOfThreat[pos] = curThreatDict
        numOfMoves-=1
        Moves.markBotRight(x+1, y-1, numOfMoves, originPos)

    def markBotLeft(x, y, numOfMoves, originPos):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or (pos in Board.dictOfObs)):
            return
        curThreatDict = Board.dictOfThreat.get(pos, -1)
        if (curThreatDict == -1): #Threatend position is new
            newDict = {originPos:{-1}}
            Board.dictOfThreat[pos] = newDict
        else: #position alr has other threats
            curThreatDict[originPos] = -1
            Board.dictOfThreat[pos] = curThreatDict
        numOfMoves-=1
        Moves.markBotLeft(x-1, y-1, numOfMoves, originPos)

class InitParams:
    # Class level var
    rows = 0
    cols = 0
    noOfObj = 0
    totalOwnPiece = 0
    listOfObjPos = []
    kValue = 0
    dictOfOwnPos = {'King': [], 'Queen':[], 'Bishop': [], 'Rook': [], 'Knight': []}
    dictOfObsOnBoard = {}

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    pass

class Board:
    
    dictOfPieces = {}
    dictOfObs = {}
    dictOfThreat = {} #Format = {'a0': {a1:1 ,a2:1}, ... }, a0 is threatened by a1 & a2. Dict within a dict
    dictOfRemovedPieces = {} #Pieces that have been removed from board.
    pass

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
    fileText = open(testfile, 'r')
    read_input(fileText)
    printInit()
    setupThreatenDict()
    printThreat()
    print(numberOfThreat())
    #goalState = search()
    #return goalState #Format to be returned

def search():
    counter = 0
    totalPc = InitParams.totalOwnPiece
    kVal = InitParams.kValue
    
    while(counter >= 0):
        randVal = counter % totalPc+1
        randPc = getPcAtIndex(randVal)
        Board.dictOfRemovedPieces[randPc] = -1
        Board.dictOfPieces.pop(randPc)
        counter+=1
        pass

def getPcAtIndex(index):
    counter = 1
    for pc in Board.dictOfPieces:
        if (index == counter):
            return pc
        counter+=1

def getPieceToRemove(curNumofThreat):
    #Non-stochastic implementation
    numOfThreat = curNumofThreat
    pos = ''
    for pieces in Board.dictOfPieces:
        curPc = pieces
        nameOfPc = Board.dictOfPieces.pop(pieces) #Remove a pc from board
        Board.dictOfRemovedPieces[curPc] = -1 # Add to removed dict
        curThreat = numberOfThreat()
        Board.dictOfPieces[curPc] = nameOfPc  # Add back pc to board
        Board.dictOfRemovedPieces.pop(curPc) # Remove from dict
        if (curThreat >= numOfThreat):
            pos = curPc
            numberOfThreat = curThreat
    return pos

def numberOfThreat():
    count = 0
    for pc in Board.dictOfPieces: #Loop thru all pcs on board.
        curThreats = Board.dictOfThreat.get(pc, 0)
        if (curThreats == 0):
            pass
        else:
            for threats in curThreats: #Loop thru all Pcs that are thretening it.
                if (threats in Board.dictOfRemovedPieces):
                    #Board.dictOfThreat.pop(threats) #Remvoes any threats that have been removed.
                    pass
                else:
                    count += 1 #Once found any 1 that threatens him, thats it.
                    break
    return count
        

def read_input(f):
    lineState = 0
    dictOfOwnPos = {'King': [], 'Queen':[], 'Bishop': [], 'Rook': [], 'Knight': []}
    
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
                InitParams.dictOfObsOnBoard[a] = -1
        elif lineState == 5:
            #Get K value (min num of pieces need)
            InitParams.kValue = getRowOrColOrObs(curLine)
        elif lineState == 6:
            #Get Number Of each peices on the board
            InitParams.totalOwnPiece = getNumerOfEnemyOrOwn(curLine)
        elif lineState == 7:
            #Get position of each piece
            if (InitParams.totalOwnPiece == 0 or ':' in curLine):
                pass
            else:
                updateEnemyPosOrOwn(curLine, dictOfOwnPos)
        elif lineState == 8:
            #Get all positions on board
            InitParams.totalOwnPiece = getNumerOfEnemyOrOwn(curLine)
        else:
            pass
        InitParams.dictOfOwnPos = dictOfOwnPos

def setupThreatenDict():
    kingPosList = InitParams.dictOfOwnPos.get("King")
    Moves.markKingMove(kingPosList)
    queenPosList = InitParams.dictOfOwnPos.get("Queen")
    Moves.markQueenMove(queenPosList)
    rookPosList = InitParams.dictOfOwnPos.get("Rook")
    Moves.markRookMove(rookPosList)
    bishopPosList = InitParams.dictOfOwnPos.get("Bishop")
    Moves.markBishopMove(bishopPosList)
    knightPosList = InitParams.dictOfOwnPos.get("Knight")
    Moves.markKnightMove(knightPosList)   
    pass

def addObjToBoard():
    for obs in InitParams.dictOfObsOnBoard:
        Board.dictOfObs[obs] = -1

#Returns row/col/# of obs
def getRowOrColOrObs(string) -> int:
    try:
        idx = string.index(':') + 1
        val = int(string[idx:])
    except Exception:
        print("Error in geting Row/Col/# of obs")
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
    count = 0
    for i in listOfvals:
        count += int(i)
    return count

# Updates dictOfOwnPos with current value of enemy position and add to list.
def updateEnemyPosOrOwn(string, curDict):
    strWithoutBrack = string.replace("[","").strip()
    strWithoutBrack = strWithoutBrack.replace("]","")
    pieceAndPos = tuple(strWithoutBrack.split(","))
    curPos = curDict.get(pieceAndPos[0]) #Get current list of pieices
    if (curPos == None):
        sys.exit("Error at getEnemyPosAndOwn")
    curPos.append(pieceAndPos[1]) #Append position to the list.
    try:
        Board.dictOfPieces[pieceAndPos[1]] = [pieceAndPos[0]]
        curDict[pieceAndPos[0]] = curPos
    except Exception:
        sys.exit("Error at getEnemyPosAndOwn")

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

# Prints all the data from the InitParams Class
def printInit():
    x = InitParams()
    print("rows:", InitParams.rows)
    print("Cols", x.cols)
    print("List of objs",x.listOfObjPos)
    print("Total number of pc: ", x.totalOwnPiece)
    print("Dict of own pos", x.dictOfOwnPos)
    print("Current Board", Board.dictOfPieces)

def printThreat():
    print("Threatend board: ")
    for x in Board.dictOfThreat:
        print(x, Board.dictOfThreat.get(x))

run_local()