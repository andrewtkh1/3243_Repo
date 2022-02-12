from collections import deque
import sys
import copy

# Helper functions to aid in your implementation. Can edit/remove
# Iteration that uses new Dict as marking, Visted dict as been moved out. Only Shallow Copy Path Taken
# Class to contain all data from input file
class InitParams:
    # Class level var
    rows = 0
    cols = 0
    noOfObj = 0
    totalEnemyPiece = 0
    totalOwnPiece = 0
    listOfObjPos = []
    dictOfStepCost = {}
    dictOfEnemyPos = {'King': [], 'Queen':[], 'Bishop': [], 'Rook': [], 'Knight': []}
    dictOfOwnPos = {'King': [], 'Queen':[], 'Bishop': [], 'Rook': [], 'Knight': []}
    dictOfObsOnBoard = {}
    dictOfGoals = {}
    listOfGoals = []
    
class Moves:        
    def markKnightMove(listOfPos):
        for pos in listOfPos:
            (x,y) = chessPosToArr(pos)
            InitParams.dictOfObsOnBoard[pos] = -1
            #Board.board[y][x] = -1
            Moves.markTopRight(x+2, y+1, 1)
            Moves.markTopRight(x+1, y+2, 1)
            Moves.markTopRight(x-2, y+1, 1)
            Moves.markTopRight(x-1, y+2, 1)
            Moves.markTopRight(x-2, y-1, 1)
            Moves.markTopRight(x-1, y-2, 1)
            Moves.markTopRight(x+2, y-1, 1)
            Moves.markTopRight(x+1, y-2, 1)
            
    def markRookMove(listOfPos):
        for pos in listOfPos:
            (x,y) = chessPosToArr(pos)
            InitParams.dictOfObsOnBoard[pos] = -1
            Moves.markUp(x,y+1,-1)
            Moves.markDown(x, y-1, -1)
            Moves.markLeft(x-1, y, -1)
            Moves.markRight(x+1, y, -1)
            #Board.board[y][x] = -1
    
    def markBishopMove(listOfPos):
        for pos in listOfPos:
            InitParams.dictOfObsOnBoard[pos] = -1
            (x,y) = chessPosToArr(pos)
            Moves.markTopRight(x+1, y+1, -1)
            Moves.markTopLeft(x-1, y+1, -1)
            Moves.markBotRight(x+1, y-1, -1)
            Moves.markBotLeft(x-1, y-1, -1)
            #Board.board[y][x] = -1
            
    def markQueenMove(listOfPos):
        for pos in listOfPos:
            (x,y) = chessPosToArr(pos)
            InitParams.dictOfObsOnBoard[pos] = -1
            Moves.markUp(x, y+1, -1)
            Moves.markDown(x, y-1, -1)
            Moves.markLeft(x-1, y, -1)
            Moves.markRight(x+1, y, -1)
            Moves.markTopRight(x+1, y+1, -1)
            Moves.markTopLeft(x-1, y+1, -1)
            Moves.markBotRight(x+1, y-1, -1)
            Moves.markBotLeft(x-1, y-1, -1)
            #Board.board[y][x] = -1
    
    def markKingMove(listOfPos):
        for pos in listOfPos:
            InitParams.dictOfObsOnBoard[pos] = -1
            (x,y) = chessPosToArr(pos)
            Moves.markUp(x, y+1, 1)
            Moves.markDown(x, y-1, 1)
            Moves.markLeft(x-1, y, 1)
            Moves.markRight(x+1, y, 1)
            Moves.markTopRight(x+1, y+1, 1)
            Moves.markTopLeft(x-1, y+1, 1)
            Moves.markBotRight(x+1, y-1, 1)
            Moves.markBotLeft(x-1, y-1, 1)
            #Board.board[y][x] = -1
    
    def markUp(x, y, numOfMoves):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0 or InitParams.dictOfObsOnBoard.get(pos,0) == -1):
            return
        InitParams.dictOfObsOnBoard[pos] = -2
        numOfMoves-=1
        Moves.markUp(x, y+1, numOfMoves)

    def markDown(x, y, numOfMoves):
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (y > maxRow or y < 0 or numOfMoves == 0 or InitParams.dictOfObsOnBoard.get(pos,0) == -1):
            return
        InitParams.dictOfObsOnBoard[pos] = -2
        numOfMoves-=1
        Moves.markDown(x, y-1, numOfMoves)

    def markLeft(x, y, numOfMoves):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0 or InitParams.dictOfObsOnBoard.get(pos,0) == -1):
            return
        InitParams.dictOfObsOnBoard[pos] = -2
        numOfMoves-=1
        Moves.markLeft(x-1, y, numOfMoves)

    def markRight(x, y, numOfMoves):
        maxCol = InitParams.cols - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or x < 0 or numOfMoves == 0 or InitParams.dictOfObsOnBoard.get(pos,0) == -1):
            return
        InitParams.dictOfObsOnBoard[pos] = -2
        numOfMoves-=1
        Moves.markRight(x+1, y, numOfMoves)

    def markTopRight(x, y, numOfMoves):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or InitParams.dictOfObsOnBoard.get(pos,0) == -1):
            return
        InitParams.dictOfObsOnBoard[pos] = -2
        numOfMoves-=1
        Moves.markTopRight(x+1, y+1, numOfMoves)

    def markTopLeft(x, y, numOfMoves):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or InitParams.dictOfObsOnBoard.get(pos,0) == -1):
            return
        InitParams.dictOfObsOnBoard[pos] = -2
        numOfMoves-=1
        Moves.markTopLeft(x-1, y+1, numOfMoves)

    def markBotRight(x, y, numOfMoves):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or InitParams.dictOfObsOnBoard.get(pos,0) == -1):
            return
        InitParams.dictOfObsOnBoard[pos] = -2
        numOfMoves-=1
        Moves.markBotRight(x+1, y-1, numOfMoves)

    def markBotLeft(x, y, numOfMoves):
        maxCol = InitParams.cols - 1
        maxRow = InitParams.rows - 1
        pos = arrToChessPos(x,y)
        if (x > maxCol or y > maxRow or y < 0 or x < 0 or numOfMoves == 0 or InitParams.dictOfObsOnBoard.get(pos,0) == -1):
            return
        InitParams.dictOfObsOnBoard[pos] = -2
        numOfMoves-=1
        Moves.markBotLeft(x-1, y-1, numOfMoves)

class Board:
    #For Accesssing board, use [y][x] coord
    board = [[]]
    totalCount = 0
    visited = {} #Dict
    
    def __init__(self) -> None:
        pass

class Node:
    def __init__(self, curPos, nextPos, pathTaken, evalCost, totalCost) -> None:
        self.curPos = curPos #String
        self.pathTaken = pathTaken #List TRY DICT
        self.evalCost = evalCost #int
        self.totalCost = totalCost #Int
        self.nextPos = nextPos #String
        self.costToNextPos = 0 #int
        pass
    
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():
    #arr = [[0 for i in range(cols)] for j in range(rows)] # ONLY Use this method to create 2d array.
    read_input()
    #printInit()
    setupBoard()
    printBoard()
    if (checkEarlyGoal()):
        return [],0
    # You can code in here but you cannot remove this function or change the return type
    moves, nodesExplored = search() #For reference
    #print(moves)
    #print(nodesExplored)
    return moves, nodesExplored #Format to be returned
        
def search():
    frontier = deque()
    startList = getStartActions() # Get start's item
    for i in startList:
        frontier.append(i) #Add all actions from 1st node
    while (len(frontier)  > 0):
        curNode = frontier.popleft()
        curPos = curNode.curPos
        nextPos = curNode.nextPos
        curTuple = (curPos[0], int(curPos[1:]))
        nextTuple = (nextPos[0], int(nextPos[1:]))
        curAction = [curTuple, nextTuple]
        curNode.pathTaken.append(curAction) #Update path taken
        curNode.totalCost += curNode.costToNextPos #Update total cost
        curNode.curPos = nextPos
        Board.totalCount+=1 #Other definiton of Goal
        listOfMoveNodes = getActionsNodes(curNode)
        for i in listOfMoveNodes:
            Board.visited[i.nextPos] = 1
            if (isGoal(i.nextPos)):
                bfsFoundGoal(i)
                Board.totalCount+=1
                return i.pathTaken, Board.totalCount
            frontier.append(i)
        
    return [], Board.totalCount

def checkEarlyGoal():
    for goal in InitParams.listOfGoals:
        x,y = chessPosToArr(goal)
        if (isValidSpot(x,y)):
            return False
    return True

def getStartActions() -> list:
    stPosList = InitParams.dictOfOwnPos.get("King")
    stPos = stPosList[0]
    Board.totalCount+=1
    Board.visited[stPos] = 1
    startNode = Node(stPos,0,[],0,0)
    ls = getActionsNodes(startNode)
    return ls

def isGoal(pos) -> bool:
    val = InitParams.dictOfGoals.get(pos,-1)
    if (val == 1):
        return True 
    return False
    
def markNodesAsVisited(nodeList):
    """Mark list of nodes next step as visited \n Returns True, Goal Node. If goal is found.\n else False, -"""
    for node in nodeList:
        pos = node.nextPos
        #Board.totalCount+=1 #Definition of nodes tested for Goal.
        if (isGoal(pos)):
            bfsFoundGoal(node)
            return True, node
            pass
        Board.visited[pos] = 1
        
    return False, None
        
def bfsFoundGoal(curNode):
    """Funciton to handle processing of early goal for BFS"""
    curPos = curNode.curPos
    nextPos = curNode.nextPos
    curTuple = (curPos[0], int(curPos[1:]))
    nextTuple = (nextPos[0], int(nextPos[1:]))
    curAction = [curTuple, nextTuple]
    curNode.pathTaken.append(curAction) #Update path taken
    curNode.totalCost += curNode.costToNextPos #Update total cost
    
def getActionsNodes(node) -> list:
    """Returns a list of Nodes that has each nextPos updated to possible next moves.
    \n evalCost can be updated too if needed.
    \n Takes in the Current Node to be processed.
    """ 
    acts = []
    listOfPos = getValidSpots(node.curPos, "king")
    for pos in listOfPos:
        a = copy.deepcopy(node.curPos)
        b = copy.deepcopy(node.nextPos)
        c = copy.deepcopy(node.totalCost)
        d = list(node.pathTaken)
        newNode = Node(a,b,d,0,c)
        #newNode = copy.deepcopy(node)
        newNode.nextPos = pos
        #newNode.costToNextPos = InitParams.dictOfStepCost.get(pos, 1) #Get cost or default value of 1
        #updateEvalCost(newNode)
        acts.append(newNode)
    return acts
    
def updateEvalCost(node):
    """ Implemnet algo to update Node.evalCost here. 
        The cost is used for PQ   """
    stepCost = node.costToNextPos
    node.evalCost = stepCost + node.totalCost
    
# Returns a list of valid pos depedning on piece   
def getValidSpots(pos, piece) -> list:
    (x, y) = chessPosToArr(pos)
    spots = []
    if (piece == "king"):
        if (isValidSpot(x+1,y)): #Right
            spots.append(arrToChessPos(x+1,y))
        if (isValidSpot(x,y+1)): #Up
            spots.append(arrToChessPos(x,y+1))
        if (isValidSpot(x-1,y)): #Left
            spots.append(arrToChessPos(x-1,y))
        if (isValidSpot(x,y-1)): #Down
            spots.append(arrToChessPos(x,y-1))
        if (isValidSpot(x+1,y+1)): #Top right
            spots.append(arrToChessPos(x+1,y+1))
        if (isValidSpot(x-1,y+1)): #Top Left
            spots.append(arrToChessPos(x-1,y+1))
        if (isValidSpot(x-1,y-1)): #Bot left
            spots.append(arrToChessPos(x-1,y-1))
        if (isValidSpot(x+1,y-1)): #Bot right
            spots.append(arrToChessPos(x+1,y-1))    
    return spots
            
                
def isValidSpot(x, y) -> bool:
    """Check if coord given is valid. \n
    valid means within bord, not blocked & not visited."""
    maxCol = InitParams.cols -1
    maxRow = InitParams.rows -1
    if (x > maxCol or y > maxRow or y < 0 or x < 0):
        return False
    chessPos = arrToChessPos(x, y)
    if (InitParams.dictOfObsOnBoard.get(chessPos,1) < 1):
        return False
    if (Board.visited.get(chessPos,-1) != -1): #Not visited = -1.
        return False
    return True   

def printBoard():
    for i in Board.board:
        print(i,"\n")

def setupBoard():
    #Board.board = [[0 for i in range(InitParams.cols)] for j in range(InitParams.rows)] # ONLY Use this method to create 2d array.
    #Board cost to be obtained using-> cost = InitParam.get('a2', someDefaultValue)
    #setupObs()
    setupEnemyPiece()
    
def setupObs():
    curBoard = Board()
    initData = InitParams()
    objList = initData.listOfObjPos
    for x in objList:
        coord = chessPosToArr(x)
        curBoard.board[coord[1]][coord[0]] = -1        
        
def setupEnemyPiece():
    if (InitParams.totalEnemyPiece == 0):
        return
    kingPosList = InitParams.dictOfEnemyPos.get("King")
    Moves.markKingMove(kingPosList)
    queenPosList = InitParams.dictOfEnemyPos.get("Queen")
    Moves.markQueenMove(queenPosList)
    rookPosList = InitParams.dictOfEnemyPos.get("Rook")
    Moves.markRookMove(rookPosList)
    bishopPosList = InitParams.dictOfEnemyPos.get("Bishop")
    Moves.markBishopMove(bishopPosList)
    knightPosList = InitParams.dictOfEnemyPos.get("Knight")
    Moves.markKnightMove(knightPosList)    

# Set up the InitParams class to have all the data from the Txt file.
# Order of input
# Rows > Cols > #Of Obs > Position of Obs: > step cost: > (Multiple new lines) > 
# # of Enemy pieces: > Position of Enemy Pieces: > (Multiple new lines) > Number of Own Pieces: > Starting Pos of Pieces: > (Multiple new lines) > Goal positions:
def read_input():
    if len(sys.argv) != 2:
        pass
        #print("ERROR IN ARGUMENTS")
        #sys.exit()
    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")
    
    lineState = 0
    dictOfStepCost = {}
    dictOfEnemyPos = {'King': [], 'Queen':[], 'Bishop': [], 'Rook': [], 'Knight': []}
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
            #Get Step Cost in tuple.
            if ':' not in curLine:
                #Skips starting line
                stepCost = getStepCost(curLine)
                #Add to dict
                dictOfStepCost[stepCost[0]] = int(stepCost[1])
        elif lineState == 6:
            #number of enemy
            InitParams.totalEnemyPiece = getNumerOfEnemyOrOwn(curLine)
        elif lineState == 7:
            #View dictOfEnemyPos for dictonary order.
            if (InitParams.totalEnemyPiece == 0 or ':' in curLine):
                pass
            else:
                updateEnemyPosOrOwn(curLine, dictOfEnemyPos)
        elif lineState == 8:
            InitParams.totalOwnPiece = getNumerOfEnemyOrOwn(curLine)
        elif lineState == 9:
            #updates own pos pieces
            if (InitParams.totalOwnPiece == 0 or ':' in curLine):
                pass
            else:
                updateEnemyPosOrOwn(curLine,dictOfOwnPos)
        elif lineState == 10:
            tmpLs = getObjPos(curLine)
            InitParams.listOfGoals = tmpLs
            for p in tmpLs:
                InitParams.dictOfGoals[p] = 1
        else:
            pass
            #sys.exit("Error in Line State")
    InitParams.dictOfEnemyPos = dictOfEnemyPos
    InitParams.dictOfOwnPos = dictOfOwnPos
    InitParams.dictOfStepCost = dictOfStepCost

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

#Get total number of Enemy pieces
def getNumerOfEnemyOrOwn(string) -> int:
    idx = string.index(':') + 1
    valOnlyStr = string[idx:].strip()
    listOfvals = list(valOnlyStr.split(" "))
    count = 0
    for i in listOfvals:
        count += int(i)
    return count

#Returns a tuple (Pos, cost) for step cost.
def getStepCost(string) -> tuple:
    strWithoutBrack = string.replace("[","")
    strWithoutBrack = strWithoutBrack.replace("]","")
    posAndCost = tuple(strWithoutBrack.split(","))
    return posAndCost

#Returns list of Obj Pos in a list
def getObjPos(string) -> list:
    idx = string.index(':') + 1
    valOnlyStr = string[idx:]
    valOnlyStr = valOnlyStr.strip()
    listOfVal = list(valOnlyStr.split(" "))
    return listOfVal
    
#Returns row/col/# of obs
def getRowOrColOrObs(string) -> int:
    try:
        idx = string.index(':') + 1
        val = int(string[idx:])
    except Exception:
        print("Error in geting Row/Col/# of obs")
        sys.exit()    
    return val

# Prints all the data from the InitParams Class
def printInit():
    x = InitParams()
    print("rows:", InitParams.rows)
    print("Cols", x.cols)
    print("dict of steps", x.dictOfStepCost)
    print("List of objs",x.listOfObjPos)
    print("Dict of enemy pos", x.dictOfEnemyPos)
    print("Dict of own pos", x.dictOfOwnPos)
    print("List of goals", x.listOfGoals)
    
#if __name__ == "__main__":
    #run_BFS()
#print(run_BFS())
#run_BFS()