import operator
import sys
import copy
import random

class chessBoard():
    obs_Dict = {}   #Holds Obstacles
    current_Index = 0   #Index of the list
    test_File_List = []     #holds the testFile
    enemy_Pieces_List = []  #0 = King, #1 = Queen, #2 = Bishop, #3 = Rook, #4 = Knight
    enemy_Coordinates_Dict = {}
    friendly_Pieces_List = []
    friendly_Coordintes_Dict = {}
    column_length = 5
    row_length = 5
    cols_Coordinate_LettersToNum = {'a':0, 'b':1,'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10,
     'l':11, 'm':12, 'n':13, 'o':14, 'p':15, 'q':16, 'r':17,'s':18, 't':19, 'u':20, 'v':21,'w':22, 
     'x':23, 'y':24, 'z':25}
    cols_Coordinate_NumToLetters = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', 8:'i',
     9:'j', 10:'k', 11:'l', 12:'m', 13:'n', 14:'o', 15:'p', 16:'q', 17:'r', 18:'s', 
     19:'t', 20:'u', 21:'v', 22:'w', 23:'x', 24:'y', 25:'z'}

    def initNumOfPieces():
        temp_Dict = {}
        temp = chessBoard.test_File_List[chessBoard.current_Index].split(":")[1].rstrip("\n")
        temp = temp.split(" ")
        for i in range(len(temp)):
            if(i == 0):
                temp_Dict["King"] = int(temp[i])
            elif(i == 1):
                temp_Dict["Queen"] = int(temp[i])
            elif(i == 2):
                temp_Dict["Bishop"] = int(temp[i])
            elif(i == 3):
                temp_Dict["Rook"] = int(temp[i])
            elif(i == 4):
                temp_Dict["Knight"] = int(temp[i])
            else:
                temp_Dict["Pawn"] = int(temp[i])
        return temp_Dict
    
    def initEnemyCoordinatesDict():
        pawn_Counter = 0
        for i in range(10):
            content_Holder = chessBoard.test_File_List[chessBoard.current_Index].rstrip("\n")
            name_Of_Piece = content_Holder.split(",")[0].replace("[", "")
            coordinate = content_Holder.split(",")[1].replace("]", "")
            if(name_Of_Piece == "Pawn"):
                chessBoard.enemy_Coordinates_Dict["B_" + name_Of_Piece + "," + str(pawn_Counter)] = coordinate
                pawn_Counter += 1
                chessBoard.current_Index +=1
            else:
                chessBoard.enemy_Coordinates_Dict["B_" + name_Of_Piece] = coordinate
                chessBoard.current_Index +=1
    
    def initFriendlyCoordinatesDict():
        pawn_Counter = 0
        for i in range(10):
            content_Holder = chessBoard.test_File_List[chessBoard.current_Index].rstrip("\n")
            name_Of_Piece = content_Holder.split(",")[0].replace("[", "")
            coordinate = content_Holder.split(",")[1].replace("]", "")
            if(name_Of_Piece == "Pawn"):
                chessBoard.friendly_Coordintes_Dict["W_" + name_Of_Piece + "," + str(pawn_Counter)] = coordinate
                pawn_Counter += 1
                chessBoard.current_Index +=1
            else:
                chessBoard.friendly_Coordintes_Dict["W_" + name_Of_Piece] = coordinate
                chessBoard.current_Index +=1

    # gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}        
    def initGameBoard(coordinates_Dict):
        gameboard = {}
        for piece in coordinates_Dict:
            coordinate = coordinates_Dict.get(piece)
            temp = list(coordinate)
            key_Tuple = (temp[0], int(temp[1]))
            if "W" in piece:
                chesspiece = piece.split("_")[1]
                if "," in chesspiece:
                    pawn_Name = chesspiece.split(",")[0]
                    gameboard[key_Tuple] =  (pawn_Name, "White")
                else:
                    gameboard[key_Tuple] =  (chesspiece, "White")
            else:
                chesspiece = piece.split("_")[1]
                if "," in chesspiece:
                    pawn_Name = chesspiece.split(",")[0]
                    gameboard[key_Tuple] =  (pawn_Name, "Black")
                else:
                    gameboard[key_Tuple] =  (chesspiece, "Black")
        return gameboard


def initTestCase():
    with open(F'{sys.argv[1]}') as f:
        testfile = f.readlines()
    chessBoard.test_File_List = testfile
    chessBoard.row_length = int(chessBoard.test_File_List[chessBoard.current_Index].split(":")[1])
    chessBoard.current_Index += 1
    chessBoard.column_length = int(chessBoard.test_File_List[chessBoard.current_Index].split(":")[1])
    chessBoard.current_Index += 1
    chessBoard.enemy_Pieces_List = chessBoard.initNumOfPieces()
    chessBoard.current_Index += 2
    chessBoard.initEnemyCoordinatesDict()
    chessBoard.friendly_Pieces_List = chessBoard.initNumOfPieces()
    chessBoard.current_Index += 2
    chessBoard.initFriendlyCoordinatesDict()
    Game.dict_Of_all_ChessPieces_Coordinates = {**chessBoard.enemy_Coordinates_Dict, **chessBoard.friendly_Coordintes_Dict}
    gameboard = chessBoard.initGameBoard(Game.dict_Of_all_ChessPieces_Coordinates)
    return gameboard 

class Piece:
    def __init__(self, name, team, coordinates, move_Set):
        self.name = name
        self.team = team
        self.coordinates = coordinates
        self.move_Set = move_Set

    def convertCoordinatesToXY(coordinates):
        content_Holder = []
        x_Axis = 0
        y_Axis = ""
        content_Holder = list(coordinates)
        if(len(content_Holder) > 2):
            x_Axis = chessBoard.cols_Coordinate_LettersToNum.get(content_Holder[0])
            content_Holder.pop(0)
            for i in range(len(content_Holder)):
                y_Axis = y_Axis + content_Holder[i]
            y_Axis = int(y_Axis)
        else:
            x_Axis = chessBoard.cols_Coordinate_LettersToNum.get(content_Holder[0])
            y_Axis = int(content_Holder[1])
        return x_Axis, y_Axis

class Knight(Piece):

    def __init__(self, name, team, coordinates, move_Set):
        super().__init__(name, team, coordinates, move_Set)
        self.utility = 30
    
    def knightMoves(name,x_axis, y_axis, position_Of_Opposing_Pieces, position_Of_Teammates, original_Coord, team):
        dict_Of_Moves = {}
        y_Axis_Movement = [2, 2, 1, -1, -2, -2, -1, 1]
        x_Axis_Movenemt = [-1, 1, 2, 2, 1, -1, -2, -2]
        for i in range(len(y_Axis_Movement)):
            Y = y_Axis_Movement[i] + y_axis
            X = x_Axis_Movenemt[i] + x_axis
            if (chessBoard.column_length > (X) >= 0) and (chessBoard.row_length > (Y) >= 0):
                newY_axis = y_Axis_Movement[i] + y_axis
                newX_axis = x_Axis_Movenemt[i] + x_axis
                coordinate = chessBoard.cols_Coordinate_NumToLetters.get(newX_axis) + str(newY_axis)
                if(coordinate in position_Of_Opposing_Pieces.values()): 
                    temp_Tuple = ("Threat",name, team, original_Coord, coordinate)
                    dict_Of_Moves[coordinate , name] = temp_Tuple
                    continue
                if(coordinate not in position_Of_Teammates.values()):
                    temp_Tuple = ("Movement",name, team, original_Coord, coordinate)
                    dict_Of_Moves[coordinate , name] = temp_Tuple
                    continue
        return dict_Of_Moves
        
class Rook(Piece):

    def __init__(self, name, team, coordinates, move_Set):
        super().__init__(name, team, coordinates, move_Set)
        self.utility = 50

    def rookMoves(name, x_axis, y_axis, position_Of_Opposing_Pieces, position_Of_Teammates, original_Coord, team):
        dict_Of_Moves = {}
        new_Y_axis = y_axis
        new_X_axis = x_axis
        
        while(chessBoard.row_length > new_Y_axis+1 >= 0): #Upwards movement
            new_Y_axis = new_Y_axis + 1
            coordinate = chessBoard.cols_Coordinate_NumToLetters.get(x_axis) + str(new_Y_axis)
            if(coordinate in position_Of_Opposing_Pieces.values()):
                temp_Tuple = ("Threat",name, team, original_Coord, coordinate) 
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            if(coordinate not in position_Of_Teammates.values()):
                temp_Tuple = ("Movement",name, team, original_Coord, coordinate)
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            else:
                break
        new_Y_axis = y_axis
        new_X_axis = x_axis

        while(chessBoard.row_length > new_Y_axis-1 >= 0): #Downward movement
            new_Y_axis = new_Y_axis - 1
            coordinate = chessBoard.cols_Coordinate_NumToLetters.get(x_axis) + str(new_Y_axis)
            if(coordinate in position_Of_Opposing_Pieces.values()):
                temp_Tuple = ("Threat",name, team, original_Coord, coordinate) 
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            if(coordinate not in position_Of_Teammates.values()):
                temp_Tuple = ("Movement",name, team, original_Coord, coordinate)
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            else:
                break
        new_Y_axis = y_axis
        new_X_axis = x_axis

        while(chessBoard.column_length > new_X_axis-1 >= 0): #left movement
            new_X_axis = new_X_axis - 1
            coordinate = chessBoard.cols_Coordinate_NumToLetters.get(new_X_axis) + str(y_axis)
            if(coordinate in position_Of_Opposing_Pieces.values()):
                temp_Tuple = ("Threat",name, team, original_Coord, coordinate) 
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            if(coordinate not in position_Of_Teammates.values()):
                temp_Tuple = ("Movement",name, team, original_Coord, coordinate)
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            else:
                break
        new_Y_axis = y_axis
        new_X_axis = x_axis
        
        while(chessBoard.column_length > new_X_axis+1 >= 0): #right movement
            new_X_axis = new_X_axis + 1
            coordinate = chessBoard.cols_Coordinate_NumToLetters.get(new_X_axis) + str(y_axis)
            if(coordinate in position_Of_Opposing_Pieces.values()):
                temp_Tuple = ("Threat",name, team, original_Coord, coordinate) 
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            if(coordinate not in position_Of_Teammates.values()):
                temp_Tuple = ("Movement",name, team, original_Coord, coordinate)
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            else:
                break
        
        return dict_Of_Moves

class Bishop(Piece):

    def __init__(self, name, team, coordinates, move_Set):
        super().__init__(name, team, coordinates, move_Set)
        self.utility = 50

    def bishopMoves(name,x_axis, y_axis, position_Of_Opposing_Pieces, position_Of_Teammates, original_Coord, team):
        dict_Of_Moves = {}
        new_Y_axis = y_axis
        new_X_axis = x_axis
        while(chessBoard.row_length > new_Y_axis+1 >= 0) and (chessBoard.column_length > new_X_axis+1 >= 0): #Diagonal Top Right movement
            new_Y_axis = new_Y_axis + 1
            new_X_axis = new_X_axis + 1
            coordinate = chessBoard.cols_Coordinate_NumToLetters.get(new_X_axis) + str(new_Y_axis)
            if(coordinate in position_Of_Opposing_Pieces.values()):
                temp_Tuple = ("Threat",name, team, original_Coord, coordinate) 
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            if(coordinate not in position_Of_Teammates.values()):
                temp_Tuple = ("Movement",name, team, original_Coord, coordinate)
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            else:
                break
        new_Y_axis = y_axis
        new_X_axis = x_axis

        while(chessBoard.row_length > new_Y_axis-1 >= 0) and (chessBoard.column_length > new_X_axis+1 >= 0): #Diagonal Bottom Right movement
            new_Y_axis = new_Y_axis - 1
            new_X_axis = new_X_axis + 1
            coordinate = chessBoard.cols_Coordinate_NumToLetters.get(new_X_axis) + str(new_Y_axis)
            if(coordinate in position_Of_Opposing_Pieces.values()):
                temp_Tuple = ("Threat",name, team, original_Coord, coordinate) 
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            if(coordinate not in position_Of_Teammates.values()):
                temp_Tuple = ("Movement",name, team, original_Coord, coordinate)
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            else:
                break
        new_Y_axis = y_axis
        new_X_axis = x_axis

        while(chessBoard.row_length > new_Y_axis+1 >= 0) and (chessBoard.column_length > new_X_axis-1 >= 0): #Diagonal Top Left movement
            new_X_axis = new_X_axis - 1
            new_Y_axis = new_Y_axis + 1
            coordinate = chessBoard.cols_Coordinate_NumToLetters.get(new_X_axis) + str(new_Y_axis)
            if(coordinate in position_Of_Opposing_Pieces.values()):
                temp_Tuple = ("Threat",name, team, original_Coord, coordinate) 
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            if(coordinate not in position_Of_Teammates.values()):
                temp_Tuple = ("Movement",name, team, original_Coord, coordinate)
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            else:
                break
        new_X_axis = x_axis
        new_Y_axis = y_axis
        
        while(chessBoard.row_length > new_Y_axis-1 >= 0) and (chessBoard.column_length > new_X_axis-1 >= 0): #Diagonal Bottom Left movement
            new_X_axis = new_X_axis - 1
            new_Y_axis = new_Y_axis - 1
            coordinate = chessBoard.cols_Coordinate_NumToLetters.get(new_X_axis) + str(new_Y_axis)
            if(coordinate in position_Of_Opposing_Pieces.values()):
                temp_Tuple = ("Threat",name, team, original_Coord, coordinate) 
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            if(coordinate not in position_Of_Teammates.values()):
                temp_Tuple = ("Movement",name, team, original_Coord, coordinate)
                dict_Of_Moves[coordinate , name] = temp_Tuple
                break
            else:
                break
        
        return dict_Of_Moves
        
class Queen(Piece):

    def __init__(self, name, team, coordinates, move_Set):
        super().__init__(name, team, coordinates, move_Set)
        self.utility = 90
    
    def queenMoves(name, x_axis, y_axis, position_Of_Opposing_Pieces, position_Of_Teammates, original_Coord,team):
        temp1_Move_Dict = {}
        temp2_Move_Dict = {}
        temp1_Move_Dict = Rook.rookMoves(name, x_axis, y_axis, position_Of_Opposing_Pieces, position_Of_Teammates, original_Coord, team)
        temp2_Move_Dict = Bishop.bishopMoves(name, x_axis, y_axis, position_Of_Opposing_Pieces, position_Of_Teammates, original_Coord, team)
        temp1_Move_Dict.update(temp2_Move_Dict)
        return temp1_Move_Dict
 
class King(Piece):

    def __init__(self, name, team, coordinates, move_Set):
        super().__init__(name, team, coordinates, move_Set)
        self.utility = 900

    def kingMoves(name, x_axis, y_axis, position_Of_Opposing_Pieces, position_Of_Teammates, original_Coord,team):
        dict_Of_Moves = {}
        y_Axis_Movement = [-1, 0, 1, -1, 1, -1, 0, 1]
        x_Axis_Movenemt = [-1, -1, -1, 0, 0, 1, 1, 1]
        for i in range(len(y_Axis_Movement)):
            Y = y_Axis_Movement[i] + y_axis
            X = x_Axis_Movenemt[i] + x_axis
            if (chessBoard.column_length > (X) >= 0) and (chessBoard.row_length > (Y) >= 0):
                newY_axis = y_Axis_Movement[i] + y_axis
                newX_axis = x_Axis_Movenemt[i] + x_axis
                new_coordinate = chessBoard.cols_Coordinate_NumToLetters.get(newX_axis) + str(newY_axis)
                if(new_coordinate in position_Of_Opposing_Pieces.values()):
                    temp_Tuple = ("Threat",name, team, original_Coord, new_coordinate) 
                    dict_Of_Moves[new_coordinate, name] = temp_Tuple
                    continue
                if(new_coordinate not in position_Of_Teammates.values()):
                    temp_Tuple = ("Movement",name, team, original_Coord, new_coordinate)
                    dict_Of_Moves[new_coordinate , name] = temp_Tuple
                    continue
        return dict_Of_Moves
                           
class Pawn(Piece):
    
    def __init__(self, name, team, coordinates, move_Set):
        super().__init__(name, team, coordinates, move_Set)
        self.utility = 10
    
    def pawnMoves(name,x_axis, y_axis, Team, position_Of_Teammates, position_Of_Opposing_Pieces, original_Coord):
        dict_Of_Moves = {}
        if(Team == "White"):
            Y = 1 + y_axis
            X = x_axis
            if (chessBoard.column_length > (X) >= 0) and (chessBoard.row_length > (Y) >= 0):
                newY_axis = 1 + y_axis
                newX_axis = x_axis
                coordinate = chessBoard.cols_Coordinate_NumToLetters.get(newX_axis) + str(newY_axis)
                if(coordinate not in position_Of_Teammates.values()) and (coordinate not in position_Of_Opposing_Pieces.values()):
                    temp_Tuple = ("Movement", name, Team, original_Coord, coordinate)
                    dict_Of_Moves[coordinate , name] = temp_Tuple
                
        else:
            Y = y_axis - 1
            X = x_axis
            if (chessBoard.column_length > (X) >= 0) and (chessBoard.row_length > (Y) >= 0):
                newY_axis = y_axis - 1
                newX_axis = x_axis
                coordinate = chessBoard.cols_Coordinate_NumToLetters.get(newX_axis) + str(newY_axis)
                if(coordinate not in position_Of_Teammates.values()) and (coordinate not in position_Of_Opposing_Pieces.values()):
                    temp_Tuple = ("Movement", name, Team, original_Coord, coordinate)
                    dict_Of_Moves[coordinate , name] = temp_Tuple
        return dict_Of_Moves
    
    def pawnEats(name, x_axis, y_axis, Team, position_Of_Opposing_Pieces, original_Coord):
        threatening_Position_Dict = {}
        if(Team == "White"):
            Y1 = y_axis + 1
            X1 = x_axis - 1
            if (chessBoard.column_length > (X1) >= 0) and (chessBoard.row_length > (Y1) >= 0):
                newY_axis = y_axis + 1
                newX_axis = x_axis - 1
                coordinate = chessBoard.cols_Coordinate_NumToLetters.get(newX_axis) + str(newY_axis)
                if(coordinate in position_Of_Opposing_Pieces.values()): 
                    temp_Tuple = ("Threat", name, Team, original_Coord, coordinate)
                    threatening_Position_Dict[coordinate , name] = temp_Tuple
            Y2 = y_axis + 1
            X2 = x_axis + 1
            if (chessBoard.column_length > (X2) >= 0) and (chessBoard.row_length > (Y2) >= 0):
                newY_axis = y_axis + 1
                newX_axis = x_axis + 1
                coordinate = chessBoard.cols_Coordinate_NumToLetters.get(newX_axis) + str(newY_axis)
                if(coordinate in position_Of_Opposing_Pieces.values()): 
                    temp_Tuple = ("Threat", name, Team, original_Coord, coordinate)
                    threatening_Position_Dict[coordinate , name] = temp_Tuple
                
        else:
            Y1 = y_axis - 1
            X1 = x_axis - 1
            if (chessBoard.column_length > (X1) >= 0) and (chessBoard.row_length > (Y1) >= 0):
                newY_axis = y_axis - 1
                newX_axis = x_axis - 1
                coordinate = chessBoard.cols_Coordinate_NumToLetters.get(newX_axis) + str(newY_axis)
                if(coordinate in position_Of_Opposing_Pieces.values()): 
                    temp_Tuple = ("Threat", name, Team, original_Coord, coordinate)
                    threatening_Position_Dict[coordinate , name] = temp_Tuple
            Y2 = y_axis - 1
            X2 = x_axis + 1
            if (chessBoard.column_length > (X2) >= 0) and (chessBoard.row_length > (Y2) >= 0):
                newY_axis = y_axis - 1
                newX_axis = x_axis + 1
                coordinate = chessBoard.cols_Coordinate_NumToLetters.get(newX_axis) + str(newY_axis)
                if(coordinate in position_Of_Opposing_Pieces.values()): 
                    temp_Tuple = ("Threat", name, Team, original_Coord, coordinate)
                    threatening_Position_Dict[coordinate , name] = temp_Tuple
        return threatening_Position_Dict

class Game:
    dict_Of_all_ChessPieces_Coordinates = {}
    
    black_Overall_Threatening_Pos = {}
    white_Overall_Threatening_Pos = {}
    black_Overall_Movement = {}
    white_Overall_Movement = {}
    
    # gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
    def initGameBoard(gameBoard):
        black_ChessPiece = {}
        white_ChessPiece = {}
        counter_White_Pawn = 0
        counter_Black_Pawn = 0
        for key in gameBoard:
            value = gameBoard.get(key)
            temp = key[1]
            temp1 = key[0]
            coordinate = temp1 + str(temp)
            chessPiece = value[0]
            team = value[1]
            if(team == "White"):
                if(chessPiece == "Pawn"):
                    updated_Chesspiece_Name = "W_" + chessPiece + "," + str(counter_White_Pawn)
                    counter_White_Pawn += 1
                else:
                    updated_Chesspiece_Name = "W_" + chessPiece
                white_ChessPiece[updated_Chesspiece_Name] = coordinate
            else:
                if(chessPiece == "Pawn"):
                    updated_Chesspiece_Name = "B_" + chessPiece + "," + str(counter_Black_Pawn)
                    counter_Black_Pawn += 1
                else:
                    updated_Chesspiece_Name = "B_" + chessPiece
                black_ChessPiece[updated_Chesspiece_Name] = coordinate
        return black_ChessPiece, white_ChessPiece

class Team:

    def __init__(self, team, pieces_Coordinates, Overall_Movement, utility):    #Pieces Coordinates = "King" : "a3". #Overall Movement: (King, Original Coordinate, New Coordinate, Type of movement)
        self.team = team
        self.pieces_Coordinates = pieces_Coordinates
        self.Overall_Movement = Overall_Movement
        self.utility = utility
        pass

    def updateTeam(chessPiece_Dict, opposing_Dict,team):
        overall_Movement = {}
        utility = 0
        for chesspiece in chessPiece_Dict:
            temp = {}
            temp1 = {}
            coordinate = chessPiece_Dict.get(chesspiece)
            x_axis, y_axis = Piece.convertCoordinatesToXY(coordinate)
            if "King" in chesspiece:
                temp = King.kingMoves(chesspiece, x_axis, y_axis, opposing_Dict, chessPiece_Dict, coordinate, team)
                overall_Movement.update(temp)
                #utility += 900
                utility += 20000
            elif "Queen" in chesspiece:
                temp = Queen.queenMoves(chesspiece, x_axis, y_axis, opposing_Dict, chessPiece_Dict, coordinate, team)
                overall_Movement.update(temp)
                #utility += 90
                utility += 900
            elif "Bishop" in chesspiece:
                temp = Bishop.bishopMoves(chesspiece, x_axis, y_axis, opposing_Dict, chessPiece_Dict, coordinate, team)
                overall_Movement.update(temp)
                #utility += 50
                utility += 330
            elif "Rook" in chesspiece:
                temp = Rook.rookMoves(chesspiece, x_axis, y_axis, opposing_Dict, chessPiece_Dict, coordinate, team)
                overall_Movement.update(temp)
                #utility += 50
                utility += 500
            elif "Knight" in chesspiece:
                temp = Knight.knightMoves(chesspiece, x_axis, y_axis, opposing_Dict, chessPiece_Dict, coordinate, team)
                overall_Movement.update(temp)
                #utility += 30
                utility += 320
            else:
                temp = Pawn.pawnMoves(chesspiece, x_axis, y_axis, team, chessPiece_Dict, opposing_Dict, coordinate)
                temp1 = Pawn.pawnEats(chesspiece, x_axis, y_axis, team, opposing_Dict, coordinate)
                overall_Movement.update(temp)
                overall_Movement.update(temp1)
                #utility += 10
                utility += 100
        
        new_Team = Team(team, chessPiece_Dict, overall_Movement, utility)
        return new_Team




class State:
    
    def __init__(self, previousState, blackTeam, whiteTeam):
        self.previousState = previousState
        self.blackTeam = blackTeam
        self.whiteTeam = whiteTeam
        pass
    
    def terminalState(state):
        blackTeam = state.blackTeam
        whiteTeam = state.whiteTeam
        if "B_King" not in blackTeam.pieces_Coordinates:
            return True
        elif "W_King" not in whiteTeam.pieces_Coordinates:
            return True
        else:
            return False
            
    def updateState(parent_State, black_Coordinates_Dict, white_Coordinates_Dict):
        blackTeam = Team.updateTeam(black_Coordinates_Dict, white_Coordinates_Dict, "Black")
        whiteTeam = Team.updateTeam(white_Coordinates_Dict, black_Coordinates_Dict, "White")
        new_State = State(parent_State, blackTeam, whiteTeam)
        return new_State
    
    def evaluationFunction(state, team):
        utility_Black = state.blackTeam.utility
        utility_White = state.whiteTeam.utility
        overall_Utility = 0
        # if(team == "Black"):
        #     overall_Utility = utility_Black - utility_White
        #     #overall_Utility = utility_White - utility_Black
        #     return overall_Utility
        # else:
        overall_Utility = utility_White - utility_Black
            #overall_Utility = utility_Black - utility_White
        return overall_Utility

    def nextMoveSet(state, team):
        if(team == "White"):
            whiteTeam = state.whiteTeam
            move_Dict = whiteTeam.Overall_Movement
            return move_Dict
        else:
            blackTeam = state.blackTeam
            move_Dict = blackTeam.Overall_Movement
            return move_Dict

    def implementNextState(current_State, each_Move):
        action_Type = each_Move[0]
        chesspiece = each_Move[1]
        team = each_Move[2]
        original_Coordinate = each_Move[3]
        next_Coordinate = each_Move[4]

        whiteTeam = current_State.whiteTeam
        whiteTeam_Coordinates = copy.deepcopy(whiteTeam.pieces_Coordinates)
        blackTeam = current_State.blackTeam
        blackTeam_Coordinates = copy.deepcopy(blackTeam.pieces_Coordinates)
        if(team == "White"):
            whiteTeam_Coordinates[chesspiece] = next_Coordinate
            if(action_Type == "Threat"):
                for key in blackTeam_Coordinates:
                    temp = blackTeam_Coordinates.get(key)
                    if(temp == next_Coordinate):
                        chesspiece_To_Remove = key
                        break
                del blackTeam_Coordinates[chesspiece_To_Remove]
            next_State = State.updateState(current_State,blackTeam_Coordinates,whiteTeam_Coordinates)
            return next_State
        else:
            blackTeam_Coordinates[chesspiece] = next_Coordinate
            if(action_Type == "Threat"):
                for key in whiteTeam_Coordinates:
                    temp = whiteTeam_Coordinates.get(key)
                    if(temp == next_Coordinate):
                        chesspiece_To_Remove = key
                        break
                del whiteTeam_Coordinates[chesspiece_To_Remove]
            next_State = State.updateState(current_State,blackTeam_Coordinates,whiteTeam_Coordinates)
            return next_State

    def unimplementNextState(new_State):
        prev_State = State(None,None,None)
        prev_State = new_State.previousState
        return prev_State



def minimax(state, depth, alpha, beta, player, team):
    
    state_Check_Terminal = State.terminalState(state)
    if(depth == 0) or (state_Check_Terminal == True):
        utility_Of_State = State.evaluationFunction(state, team)
        return None, utility_Of_State
    #Get the next set of moves
    move_Dict = State.nextMoveSet(state, team)
    best_Move = random.choice(list(move_Dict.values()))
    
    #positive_infinity = float('inf')
    if player == "Max":
        max_Utility = float('-inf') #-ve Infinity
        for each_Move in move_Dict:
            move = move_Dict.get(each_Move)
            new_State = State.implementNextState(state,move)
            current_Utility = minimax(new_State, depth - 1, alpha, beta, "Min", "Black")[1]
            new_State = State.unimplementNextState(new_State)
            if current_Utility > max_Utility:
                max_Utility = current_Utility
                best_Move = each_Move
            alpha = max(alpha, current_Utility)
            if beta <= alpha:
                break
        return best_Move, max_Utility
    else:
        min_Utility = float('inf')
        for each_Move in move_Dict:
            move = move_Dict.get(each_Move)
            new_State = State.implementNextState(state, move)
            current_Utility = minimax(new_State, depth - 1, alpha, beta, "Max", "White")[1]
            new_State = State.unimplementNextState(new_State)
            if current_Utility < min_Utility:
                min_Utility = current_Utility
                best_Move = each_Move
            beta = min(beta, current_Utility)
            if beta >= alpha:
                break
        return best_Move, min_Utility


#Implement your minimax with alpha-beta pruning algorithm here.
def ab(type):
    pass

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
    alpha = float('-inf')
    beta = float('inf')
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    black_ChessPiece_Dict, white_ChessPiece_Dict = Game.initGameBoard(gameboard)
    state = State.updateState(None, black_ChessPiece_Dict, white_ChessPiece_Dict)
    best_Move, utility = minimax(state, 3, alpha, beta, "Max", "White")
    #print (utility)
    ending_Coordinate = best_Move[0]
    chesspiece = best_Move[1]
    starting_Coordinate = white_ChessPiece_Dict.get(chesspiece)
    temp = list(starting_Coordinate)
    start = (temp[0] , int(temp[1]))
    temp1 = list(ending_Coordinate)
    end = (temp1[0], int(temp1[1]))
    move = (start, end)
    return move #Format to be returned (('a', 0), ('b', 3))
#gameboard = initTestCase()
#studentAgent(gameboard)