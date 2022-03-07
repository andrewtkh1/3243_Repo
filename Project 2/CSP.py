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
    kValue = 0
    dictOfOwnPos = {'King': [], 'Queen':[], 'Bishop': [], 'Rook': [], 'Knight': []}
    dictOfObsOnBoard = {}

class Board:
    totalThreat = 0
    dictOfPieces = {}
    dictOfObs = {}
    dictOfThreat = {} #Format = {'a0': {a1:1 ,a2:1}, ... }, a0 is threatened by a1 & a2. Dict within a dict
    dictOfRemovedPieces = {} #Pieces that have been removed from board.
    listOfRemainingPieces = []
    pass

def search():
    pass

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
    #goalState = search()
    #return goalState #Format to be returned
    return

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
                InitParams.dictOfObsOnBoard[a] = -1
        elif lineState == 5:
            #Get Number Of each peices on the board
            InitParams.totalOwnPiece = getNumerOfEnemyOrOwn(curLine)
        else:
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
    king = int(listOfvals[0])
    queen = int(listOfvals[1])
    bishop = int(listOfvals[2])
    rook = int(listOfvals[3])
    knight = int(listOfvals[4])
    count = 0
    fillListOfPieces(king, queen, bishop, rook, knight)
    for i in listOfvals:            
        count += int(i)
    return count

def fillListOfPieces(king, queen, bishop, rook, knight):
    for x in range(king):
        Board.listOfRemainingPieces.append("King")
    for x in range(knight):
        Board.listOfRemainingPieces.append("Knight")
    for x in range(rook):
        Board.listOfRemainingPieces.append("Rook")
    for x in range(bishop):
        Board.listOfRemainingPieces.append("Bishop")
    for x in range(queen):
        Board.listOfRemainingPieces.append("Queen")
        
run_CSP()