import sys
import copy

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
# Iteration that uses new Dict as marking, Visted dict as been moved out. Only Shallow Copy Path Taken
# Class to contain all data from input file
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
    pass

class State:
    pass

def search():
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
    #goalState = search()
    #return goalState #Format to be returned

def read_input(f):
    
    lineState = 0
    dictOfOwnPos = {'King': [], 'Queen':[], 'Bishop': [], 'Rook': [], 'Knight': []}

    for curLine in f:
        if ':' in curLine:
            lineState += 1
            print(lineState)
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

# Updates dictOfEnemyPos with current value of enemy position and add to list.
def updateEnemyPosOrOwn(string, curDict):
    strWithoutBrack = string.replace("[","").strip()
    strWithoutBrack = strWithoutBrack.replace("]","")
    pieceAndPos = tuple(strWithoutBrack.split(","))
    curPos = curDict.get(pieceAndPos[0])
    if (curPos == None):
        sys.exit("Error at getEnemyPosAndOwn")
    curPos.append(pieceAndPos[1])
    try:
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
    print("Dict of own pos", x.dictOfOwnPos)

run_local()