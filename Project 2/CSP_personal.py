import sys
import random
import heapq
import pygame as p
import time
import os

def isvalid(row, col):
    if row > norows-1 or row < 0 or col > nocols-1 or col < 0:
        return False
    else:
        return True

def convertpos(pos):
    col = ord(pos[0]) - 97
    row = int(pos[1:])
    return (row,col)

def converttuple(pos):
    row = pos[0]
    col = chr(pos[1] + 97)
    return (col,row)

def findgoal(pieces,index,board,screen):
    currentpiece = pieces[index]
    if currentpiece.name == "finish":
        return True
    currentpiece.checkneighours(board.board)
    while len(currentpiece.pq) > 0:
        pos = heapq.heappop(currentpiece.pq)[1]
        currentpiece.placepiece(pos,board.board)

        board.drawboard(screen)
        board.drawpieces(screen)
        p.display.flip()
        time.sleep(0.001)

        if findgoal(pieces,index+1,board,screen) == True:
            return True
    #print("BACKTRACK DETECTED",pieces[index-1].placedpos)
    if pieces[index-1].placedpos == (999,999):
        return False
    board.board[pieces[index-1].placedpos[0]][pieces[index-1].placedpos[1]] = " "
    for pos in pieces[index-1].threatset:
        board.board[pos[0]][pos[1]] = " "
    return False


class Board:
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.board = []
        self.width = 64
        self.height = 64

        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[i].append(" ")

    def makefailure(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = "T"

    def drawboard(self,screen):
        colors = [p.Color("white"),p.Color("gray")]
        for row in range(self.rows):
            for col in range(self.cols):
                color = colors[((row+col) % 2)]
                p.draw.rect(screen,color,p.Rect(col*self.width,row*self.height,self.width,self.height))

    def drawpieces(self,screen):
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                if piece != " ":
                    screen.blit(images[piece],p.Rect(col*self.width,row*self.height,self.width,self.height))

    def placeObstacles(self,obstacle):
        row = int(obstacle[0])
        col = int(obstacle[1])
        self.board[row][col] = "X"

class Piece:
    def __init__(self,name):
        self.name = name
        self.pq = []
        self.threatset = set()
        self.placedpos = (999,999)

    def placepiece(self,pos,board):
        row = pos[0]
        col = pos[1]
        self.threatset = set()
        if self.name == "King":
            board[row][col] = "K"
            self.placedpos = (row,col)
            for i in range(3):
                if isvalid(row-1,col-1+i) == True and board[row-1][col-1+i] == " ":
                    board[row-1][col-1+i] = "T"
                    self.threatset.add((row-1,col-1+i))
            for i in range(3):
                if isvalid(row+1,col-1+i) == True and board[row+1][col-1+i] == " ":
                    board[row+1][col-1+i] = "T"
                    self.threatset.add((row+1,col-1+i))
            if isvalid(row, col - 1) == True and board[row][col - 1] == " ":
                board[row][col - 1] = "T"
                self.threatset.add((row, col - 1))
            if isvalid(row, col + 1) == True and board[row][col + 1] == " ":
                board[row][col + 1] = "T"
                self.threatset.add((row, col + 1))

        if self.name == "Rook":
            for i in range(1,nocols):
                if isvalid(row, col+i) == True and board[row][col+i] == " ":
                    board[row][col+i] = "T"
                    self.threatset.add((row, col+i))
                elif isvalid(row, col+i) == True and board[row][col+i] == "T":
                    pass
                else:
                    break
            for i in range(1,nocols):
                if isvalid(row, col-i) == True and board[row][col-i] == " ":
                    board[row][col-i] = "T"
                    self.threatset.add((row, col-i))
                elif isvalid(row, col-i) == True and board[row][col-i] == "T":
                    pass
                else:
                    break
            for i in range(1,norows):
                if isvalid(row+i, col) == True and board[row+i][col] == " ":
                    board[row+i][col] = "T"
                    self.threatset.add((row+i, col))
                elif isvalid(row+i, col) == True and board[row+i][col] == "T":
                    pass
                else:
                    break
            for i in range(1,norows):
                if isvalid(row-i, col) == True and board[row-i][col] == " ":
                    board[row-i][col] = "T"
                    self.threatset.add((row-i, col))
                elif isvalid(row-i, col) == True and board[row-i][col] == "T":
                    pass
                else:
                    break
            self.placedpos = (row, col)
            board[row][col] = "R"

        if self.name == "Bishop":
            for i in range(1,max(norows,nocols)):
                if isvalid(row+i,col+i) == True and board[row+i][col+i] == " ":
                    board[row+i][col+i] = "T"
                    self.threatset.add((row+i,col+i))
                elif isvalid(row+i,col+i) == True and board[row+i][col+i] == "T":
                    pass
                else:
                    break
            for i in range(1,max(norows,nocols)):
                if isvalid(row-i,col-i) == True and board[row-i][col-i] == " ":
                    board[row-i][col-i] = "T"
                    self.threatset.add((row-i,col-i))
                elif isvalid(row-i,col-i) == True and board[row-i][col-i] == "T":
                    pass
                else:
                    break
            for i in range(1,max(norows,nocols)):
                if isvalid(row+i,col-i) == True and board[row+i][col-i] == " ":
                    board[row+i][col-i] = "T"
                    self.threatset.add((row+i,col-i))
                elif isvalid(row+i,col-i) == True and board[row+i][col-i] == "T":
                    pass
                else:
                    break
            for i in range(1,max(norows,nocols)):
                if isvalid(row-i,col+i) == True and board[row-i][col+i] == " ":
                    board[row-i][col+i] = "T"
                    self.threatset.add((row-i,col+i))
                elif isvalid(row-i,col+i) == True and board[row-i][col+i] == "T":
                    pass
                else:
                    break
            self.placedpos = (row, col)
            board[row][col] = "B"

        if self.name == "Queen":
            for i in range(1,nocols):
                if isvalid(row, col+i) == True and board[row][col+i] == " ":
                    board[row][col+i] = "T"
                    self.threatset.add((row, col+i))
                elif isvalid(row, col+i) == True and board[row][col+i] == "T":
                    pass
                else:
                    break
            for i in range(1,nocols):
                if isvalid(row, col-i) == True and board[row][col-i] == " ":
                    board[row][col-i] = "T"
                    self.threatset.add((row, col-i))
                elif isvalid(row, col-i) == True and board[row][col-i] == "T":
                    pass
                else:
                    break
            for i in range(1,norows):
                if isvalid(row+i, col) == True and board[row+i][col] == " ":
                    board[row+i][col] = "T"
                    self.threatset.add((row+i, col))
                elif isvalid(row+i, col) == True and board[row+i][col] == "T":
                    pass
                else:
                    break
            for i in range(1,norows):
                if isvalid(row-i, col) == True and board[row-i][col] == " ":
                    board[row-i][col] = "T"
                    self.threatset.add((row-i, col))
                elif isvalid(row-i, col) == True and board[row-i][col] == "T":
                    pass
                else:
                    break
            for i in range(1,max(norows,nocols)):
                if isvalid(row+i,col+i) == True and board[row+i][col+i] == " ":
                    board[row+i][col+i] = "T"
                    self.threatset.add((row+i,col+i))
                elif isvalid(row+i,col+i) == True and board[row+i][col+i] == "T":
                    pass
                else:
                    break
            for i in range(1,max(norows,nocols)):
                if isvalid(row-i,col-i) == True and board[row-i][col-i] == " ":
                    board[row-i][col-i] = "T"
                    self.threatset.add((row-i,col-i))
                elif isvalid(row-i,col-i) == True and board[row-i][col-i] == "T":
                    pass
                else:
                    break
            for i in range(1,max(norows,nocols)):
                if isvalid(row+i,col-i) == True and board[row+i][col-i] == " ":
                    board[row+i][col-i] = "T"
                    self.threatset.add((row+i,col-i))
                elif isvalid(row+i,col-i) == True and board[row+i][col-i] == "T":
                    pass
                else:
                    break
            for i in range(1,max(norows,nocols)):
                if isvalid(row-i,col+i) == True and board[row-i][col+i] == " ":
                    board[row-i][col+i] = "T"
                    self.threatset.add((row-i,col+i))
                elif isvalid(row-i,col+i) == True and board[row-i][col+i] == "T":
                    pass
                else:
                    break
            self.placedpos = (row, col)
            board[row][col] = "Q"

        if self.name == "Knight":
            board[row][col] = "k"
            self.placedpos = (row, col)
            if isvalid(row+2, col+1) == True and board[row+2][col+1] == " ":
                board[row+2][col+1] = "T"
                self.threatset.add((row+2, col+1))
            if isvalid(row+1, col+2) == True and board[row+1][col+2] == " ":
                board[row+1][col+2] = "T"
                self.threatset.add((row+1, col+2))
            if isvalid(row-2, col-1) == True and board[row-2][col-1] == " ":
                board[row-2][col-1] = "T"
                self.threatset.add((row-2, col-1))
            if isvalid(row-1, col-2) == True and board[row-1][col-2] == " ":
                board[row-1][col-2] = "T"
                self.threatset.add((row-1, col-2))
            if isvalid(row-2, col+1) == True and board[row-2][col+1] == " ":
                board[row-2][col+1] = "T"
                self.threatset.add((row-2, col+1))
            if isvalid(row-1, col+2) == True and board[row-1][col+2] == " ":
                board[row-1][col+2] = "T"
                self.threatset.add((row-1, col+2))
            if isvalid(row+2, col-1) == True and board[row+2][col-1] == " ":
                board[row+2][col-1] = "T"
                self.threatset.add((row+2, col-1))
            if isvalid(row+1, col-2) == True and board[row+1][col-2] == " ":
                board[row+1][col-2] = "T"
                self.threatset.add((row+1, col-2))

    def inspectpiece(self,pos,board):
        row = pos[0]
        col = pos[1]
        threats = 0
        if self.name == "King":
            for i in range(3):
                if isvalid(row-1,col-1+i) == True:
                    if board[row-1][col-1+i] == " ":
                        threats += 1
                    elif board[row-1][col-1+i] in pieceset:
                        return -1

            for i in range(3):
                if isvalid(row + 1, col - 1 + i) == True:
                    if board[row + 1][col - 1 + i] == " ":
                        threats += 1
                    elif board[row + 1][col - 1 + i] in pieceset:
                        return -1

            if isvalid(row, col - 1) == True:
                if board[row][col - 1] == " ":
                    threats += 1
                elif board[row][col - 1] in pieceset:
                    return -1

            if isvalid(row, col + 1) == True:
                if board[row][col + 1] == " ":
                    threats += 1
                elif board[row][col + 1] in pieceset:
                    return -1

        if self.name == "Rook":
            for i in range(1,nocols):
                if isvalid(row, col+i) == True:
                    if board[row][col+i] == " ":
                        threats += 1
                    elif board[row][col+i] == "X":
                        break
                    elif board[row][col+i] in pieceset:
                        return -1
            for i in range(1,nocols):
                if isvalid(row, col - i) == True:
                    if board[row][col - i] == " ":
                        threats += 1
                    elif board[row][col - i] == "X":
                        break
                    elif board[row][col - i] in pieceset:
                        return -1
            for i in range(1,norows):
                if isvalid(row + i, col) == True:
                    if board[row + i][col] == " ":
                        threats += 1
                    elif board[row + i][col] == "X":
                        break
                    elif board[row + i][col] in pieceset:
                        return -1
            for i in range(1,norows):
                if isvalid(row - i, col) == True:
                    if board[row - i][col] == " ":
                        threats += 1
                    elif board[row - i][col] == "X":
                        break
                    elif board[row - i][col] in pieceset:
                        return -1

        if self.name == "Bishop":
            for i in range(1,max(norows,nocols)):
                if isvalid(row+i,col+i) == True:
                    if board[row+i][col+i] == " ":
                        threats += 1
                    elif board[row+i][col+i] == "X":
                        break
                    elif board[row+i][col+i] in pieceset:
                        return -1
            for i in range(1,max(norows,nocols)):
                if isvalid(row - i, col - i) == True:
                    if board[row - i][col - i] == " ":
                        threats += 1
                    elif board[row - i][col - i] == "X":
                        break
                    elif board[row - i][col - i] in pieceset:
                        return -1
            for i in range(1,max(norows,nocols)):
                if isvalid(row + i, col - i) == True:
                    if board[row + i][col - i] == " ":
                        threats += 1
                    elif board[row + i][col - i] == "X":
                        break
                    elif board[row + i][col - i] in pieceset:
                        return -1
            for i in range(1,max(norows,nocols)):
                if isvalid(row - i, col + i) == True:
                    if board[row - i][col + i] == " ":
                        threats += 1
                    elif board[row - i][col + i] == "X":
                        break
                    elif board[row - i][col + i] in pieceset:
                        return -1

        if self.name == "Queen":
            for i in range(1,nocols):
                if isvalid(row, col+i) == True:
                    if board[row][col+i] == " ":
                        threats += 1
                    elif board[row][col+i] == "X":
                        break
                    elif board[row][col+i] in pieceset:
                        return -1
            for i in range(1,nocols):
                if isvalid(row, col - i) == True:
                    if board[row][col - i] == " ":
                        threats += 1
                    elif board[row][col - i] == "X":
                        break
                    elif board[row][col - i] in pieceset:
                        return -1
            for i in range(1,norows):
                if isvalid(row + i, col) == True:
                    if board[row + i][col] == " ":
                        threats += 1
                    elif board[row + i][col] == "X":
                        break
                    elif board[row + i][col] in pieceset:
                        return -1
            for i in range(1,norows):
                if isvalid(row - i, col) == True:
                    if board[row - i][col] == " ":
                        threats += 1
                    elif board[row - i][col] == "X":
                        break
                    elif board[row - i][col] in pieceset:
                        return -1
            for i in range(1,max(norows,nocols)):
                if isvalid(row+i,col+i) == True:
                    if board[row+i][col+i] == " ":
                        threats += 1
                    elif board[row+i][col+i] == "X":
                        break
                    elif board[row+i][col+i] in pieceset:
                        return -1
            for i in range(1,max(norows,nocols)):
                if isvalid(row - i, col - i) == True:
                    if board[row - i][col - i] == " ":
                        threats += 1
                    elif board[row - i][col - i] == "X":
                        break
                    elif board[row - i][col - i] in pieceset:
                        return -1
            for i in range(1,max(norows,nocols)):
                if isvalid(row + i, col - i) == True:
                    if board[row + i][col - i] == " ":
                        threats += 1
                    elif board[row + i][col - i] == "X":
                        break
                    elif board[row + i][col - i] in pieceset:
                        return -1
            for i in range(1,max(norows,nocols)):
                if isvalid(row - i, col + i) == True:
                    if board[row - i][col + i] == " ":
                        threats += 1
                    elif board[row - i][col + i] == "X":
                        break
                    elif board[row - i][col + i] in pieceset:
                        return -1

        if self.name == "Knight":
            if isvalid(row+2, col+1) == True:
                if board[row+2][col+1] == " ":
                    threats += 1
                elif board[row+2][col+1] in pieceset:
                    return -1
            if isvalid(row+1, col+2) == True:
                if board[row+1][col+2] == " ":
                    threats += 1
                elif board[row+1][col+2] in pieceset:
                    return -1
            if isvalid(row-2, col-1) == True:
                if board[row-2][col-1] == " ":
                    threats += 1
                elif board[row-2][col-1] in pieceset:
                    return -1
            if isvalid(row-1, col-2) == True:
                if board[row-1][col-2] == " ":
                    threats += 1
                elif board[row-1][col-2] in pieceset:
                    return -1
            if isvalid(row-2, col+1) == True:
                if board[row-2][col+1] == " ":
                    threats += 1
                elif board[row-2][col+1] in pieceset:
                    return -1
            if isvalid(row-1, col+2) == True:
                if board[row-1][col+2] == " ":
                    threats += 1
                elif board[row-1][col+2] in pieceset:
                    return -1
            if isvalid(row+2, col-1) == True:
                if board[row+2][col-1] == " ":
                    threats += 1
                elif board[row+2][col-1] in pieceset:
                    return -1
            if isvalid(row+1, col-2) == True:
                if board[row+1][col-2] == " ":
                    threats += 1
                elif board[row+1][col-2] in pieceset:
                    return -1
        return threats

    def checkneighours(self,board):
        backtrack = False
        for row in range(norows):
            for col in range(nocols):
                if board[row][col] == " ":
                    value = self.inspectpiece((row,col),board)
                    if value >= 0:
                        heapq.heappush(self.pq,(value,(row,col)))
        #if len(self.pq) > 0:
            #self.placepiece(heapq.heappop(self.pq)[1], board)
        #else:
            #backtrack = True
        #return backtrack

#def loadimages():
    #images["K"] = p.image.load("images/bK.png")
    #images["Q"] = p.image.load("images/bQ.png")
    #images["B"] = p.image.load("images/bB.png")
   # images["R"] = p.image.load("images/bR.png")
    #images["k"] = p.image.load("images/bN.png")
  #  images["X"] = p.image.load("images/obstacle.png")
  #  images["T"] = p.image.load("images/threaten.png")
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    file = open(sys.argv[1], "r") #Do not remove. This is your input testfile.
    lines = file.readlines()
    file.close()  #Close text file
    global norows
    global nocols
    global pieceset
    pieceset = set(["K","Q","B","R","k"])
    norows = int(lines[0][5:])
    nocols = int(lines[1][5:])

    gameboard = Board(norows,nocols)
    noobstacles = int(lines[2][20:])
    if noobstacles != 0:
        obstaclelist = lines[3][38:].split()
        for index,pos in enumerate(obstaclelist):
            obstaclelist[index] = convertpos(pos)
            gameboard.placeObstacles(obstaclelist[index])
    Kqbrk = [int(i) for i in lines[4][60:].split()] #end of parsing

    width = 64 * nocols
    height = 64 * norows
    screen = p.display.set_mode((width,height))
    screen.fill(p.Color("white"))

    queuepieces = [] #needed
    for i in range(Kqbrk[1]):
        queuepieces.append("Queen")
    for i in range(Kqbrk[3]):
        queuepieces.append("Rook")
    for i in range(Kqbrk[2]):
        queuepieces.append("Bishop")
    for i in range(Kqbrk[4]):
        queuepieces.append("Knight")
    for i in range(Kqbrk[0]):
        queuepieces.append("King")
    queuepieces.append("finish")
    objectpieces = []
    for piece in queuepieces:
        objectpieces.append(Piece(piece))

    running = True
    runonce = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        if runonce == False:
            finished = findgoal(objectpieces, 0, gameboard,screen)
            if finished == False:
                gameboard.makefailure()
            runonce = True
        gameboard.drawboard(screen)
        gameboard.drawpieces(screen)
        clock.tick(15)
        p.display.flip()

p.init()
clock = p.time.Clock()
images = {}
#loadimages()
run_CSP()