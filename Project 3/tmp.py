import AB
import FalAB
import copy
import MarkusAB
import waiKitAB

class Game:
    enemyPieces = {('e', 4) : ('King', 'Black'), ('d', 4): ('Queen', 'Black'), ('c', 4): ('Bishop', 'Black'), ('b', 4): ('Knight', 'Black'), ('a', 4): ('Rook', 'Black')
    , ('a', 3): ('Pawn', 'Black'), ('b', 3): ('Pawn', 'Black'), ('c', 3): ('Pawn', 'Black'), ('d', 3): ('Pawn', 'Black'), ('e', 3): ('Pawn', 'Black')}

    tmpEnemyPiece = {('e', 4) : ('King', 'White'), ('d', 4): ('Queen', 'White'), ('c', 4): ('Bishop', 'White'), ('b', 4): ('Knight', 'White'), ('a', 4): ('Rook', 'White')
    , ('a', 3): ('Pawn', 'White'), ('b', 3): ('Pawn', 'White'), ('c', 3): ('Pawn', 'White'), ('d', 3): ('Pawn', 'White'), ('e', 3): ('Pawn', 'White')}

    tmpOwnPiece = {('e', 0): ('King', 'Black'), ('d', 0): ('Queen', 'Black'), ('c', 0): ('Bishop', 'Black'), ('b', 0): ('Knight', 'Black'), ('a', 0): ('Rook', 'Black')
    , ('a', 1): ('Pawn', 'Black'), ('b', 1): ('Pawn', 'Black'), ('c', 1): ('Pawn', 'Black'), ('d', 1): ('Pawn', 'Black'), ('e', 1): ('Pawn', 'Black')}
 
    ownPieces = {('e', 0): ('King', 'White'), ('d', 0): ('Queen', 'White'), ('c', 0): ('Bishop', 'White'), ('b', 0): ('Knight', 'White'), ('a', 0): ('Rook', 'White')
    , ('a', 1): ('Pawn', 'White'), ('b', 1): ('Pawn', 'White'), ('c', 1): ('Pawn', 'White'), ('d', 1): ('Pawn', 'White'), ('e', 1): ('Pawn', 'White')}    

    startGameBoard = {**enemyPieces, **ownPieces}
    #startGameBoard = {**trial1, **trial2}
    pass


# HOW TO USE:
# Step 1: Drag and drop file into same folder as this code.
# Step 2: Import both players code using the "import <Player's Code file name>"
# Step 3: Decide who to go first by editing which code to call 1st. See below on where to change between plyaer 1 or player 2.

def fight():
    k = 0
    while (k < 50):
        board = {**Game.enemyPieces, **Game.ownPieces}
        tmp = copy.deepcopy(board)
        (src, dest) = AB.studentAgent(tmp) #Player 1
        src = posToStr(src)
        dest = posToStr(dest)
        #print(src)
        print(src, " ", dest, "White")
        print(tmp,"\n")
        move(1, src, dest)
        if (checkWhoWin(2)):
            print("WHITE WIN")
            return
        board = {**Game.tmpEnemyPiece, **Game.tmpOwnPiece}
        tmp = copy.deepcopy(board)
        (src, dest) = waiKitAB.studentAgent(tmp) #Player 2
        src = posToStr(src)
        dest = posToStr(dest)
        print(src, " ", dest, "Black")
        print(tmp,"\n")
        move(2, src, dest)
        if (checkWhoWin(1)):
            print("BLACK WIN")
            return
        k+=1
    print("DRAW")

def checkWhoWin(color):
    if (color == 1):
        for pos in Game.ownPieces:
            piece, color = Game.ownPieces.get(pos)
            if (piece == "King"):
                return 0
        return 1
    else:
        for pos in Game.enemyPieces:
            piece, color = Game.enemyPieces.get(pos)
            if (piece == "King"):
                return 0
        return 1

def strToPos (pos):
    return pos[0] + str(pos[1])

def posToStr (pos):
    return (pos[0], int(pos[1]))

def move(color, src, dest):
    if (color == 1):
        (piece, color) = Game.ownPieces.pop(src)
        (pieceTmp, colorTmp) = Game.tmpOwnPiece.pop(src)
        Game.ownPieces[dest] = (piece, color)
        Game.tmpOwnPiece[dest] = (pieceTmp, colorTmp)
        if (dest in Game.enemyPieces):
            Game.tmpEnemyPiece.pop(dest)
            Game.enemyPieces.pop(dest)
    else:
        (piece, color) = Game.enemyPieces.pop(src)
        (pieceTmp, colorTmp) = Game.tmpEnemyPiece.pop(src)
        Game.enemyPieces[dest] = (piece, color)
        Game.tmpEnemyPiece[dest] = (pieceTmp, colorTmp)
        if (dest in Game.ownPieces):
            Game.tmpOwnPiece.pop(dest)
            Game.ownPieces.pop(dest)


fight()