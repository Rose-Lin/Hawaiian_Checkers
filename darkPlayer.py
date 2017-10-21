import sys
sys.path.append("./")
import gameBoard
import copy
from random import randint

DARKPLAYER = 1
LIGHTPLAYER = 0
POSSIBLE_FIRST_MOVE_DARK = [(8,8),(1,1),(5,5),(4,4)]

class Player:

    def __init__(self, identity, round, moves, gameState):
        self.identity = identity
        self.moves = moves
        self.round = round
        self.gameState = gameState

    def search(self, gameState):
        #search algorithm
        mover = ()
        return move

    #The first move for DARKPLAYER
    def generateFirstMove_Dark(self):
        i = randint(0,3)
        return POSSIBLE_FIRST_MOVE_DARK[i]

    #The first move for LIGHTPLAYER
    #The LIGHTPLAYER can remove a check adjacent to the check DARKPLAYER removed
    def generateFirstMove_Light(self, darkMove, gameBoard):
        adjs = [1,-1]
        light_moves = []
        light_move = ()
        for adj in adjs:
            if (not darkMove[0] + adj == gameBoard.width + 1) and darkMove[0] + adj:
                light_move = (darkMove[0]+adj, darkMove[1])
                light_moves.append(light_move)
            if (not darkMove[1] + adj == gameBoard.width + 1) and darkMove[1] + adj:
                light_move = (darkMove[0], darkMove[1]+adj)
                light_moves.append(light_move)
        i = randint(0,len(light_moves)-1)
        return light_moves[i]

    def generatePossibleMoves(self, gameBoard, identity):
        if identity:
            moveable = gameBoard.getDarkCell()
            unmoveable = gameBoard.getLightCell()
        else:
            movable = gameBoard.getLightCell()
            unmoveable = gameBoard.getDarkCell()
        emptyCells = gameBoard.getEmptyCell()
        possibleMoves = self.__generatePossibleMoves_Helper(gameBoard, moveable, unmoveable, emptyCells)
        possibleMoves = self.__generateMultipleJumps(identity, possibleMoves, gameBoard, unmoveable, emptyCells)
        return possibleMoves
        #return self.__generateMultipleJumps(identity, possibleMoves, gameBoard, moveable, unmoveable, emptyCells)

    def __generateMultipleJumps(self, identity, possibleMoves, gameBoard, unmoveable, emptyCells):
        game = copy.deepcopy(gameBoard)
        empty = copy.deepcopy(emptyCells)
        p = copy.deepcopy(possibleMoves)
        for move in possibleMoves.keys():
            p = self.__generateMultipleJumps_Helper(p, game, move, unmoveable, empty, identity, 2)
        return p

    #change the endPositions in possibleMoves, if the check can jump over multiple times
    #Since the check cannot turn, the maximun number of jump is 3
    #The count variable counts the time the check jumps [0:2]
    def __generateMultipleJumps_Helper(self,possibleMoves, game, move, unmoveable, empty, identity, count = 2):
        if not count:
            return possibleMoves
        for m in possibleMoves[move]:
            game.updateBoard(move, m, identity)
            if m in empty:
                empty.remove(m)
            new_move = self.__generatePossibleMoves_Helper(game, [m], unmoveable,empty)
            if new_move:
                for nm in new_move[m]:
                    if not self.__ifTurned(move, nm):
                        possibleMoves[move] = [nm] + possibleMoves[move]
                        possibleMoves[move].remove(m)
        return self.__generateMultipleJumps_Helper(possibleMoves,game, move,unmoveable,empty,identity,count-1)


    def __ifTurned(self, startPosition, endPosition):
        if startPosition[0] == endPosition[0] or startPosition[1] == endPosition[1]:
            return False
        return True

    def __generatePossibleMoves_Helper(self, gameBoard, moveable, unmoveable, emptyCells):
        result = {}
        desiredEmptyList = []
        for moveChecker in moveable:
            for unmoveChecker in unmoveable:
                if self.ifAdjacent(moveChecker, unmoveChecker):
                    desiredEmpty =self.__desiredEmpty(gameBoard, moveChecker, unmoveChecker)
                    if desiredEmpty in emptyCells:
                        desiredEmptyList.append(desiredEmpty)
                        result[moveChecker] = desiredEmptyList
            desiredEmptyList = []
        return result

    #The function returns the position tuple of an emptyCell
    def __desiredEmpty(self, gameBoard, moveable, unmoveable):
        if moveable[0] == unmoveable[0]:
            if moveable[1] < unmoveable[1]:
                if unmoveable[1] < gameBoard.width:
                    return (unmoveable[0], unmoveable[1]+1)
            else:
                if unmoveable[1] > 1:
                    return (unmoveable[0], unmoveable[1]-1)
        elif moveable[1] == unmoveable[1]:
            if moveable[0] < unmoveable[0]:
                if unmoveable[0] < gameBoard.width:
                    return (unmoveable[0]+1, unmoveable[1])
            else:
                if unmoveable[1] > 1:
                    return (unmoveable[0]-1, unmoveable[1])
        return None

    #check if two positions are adjacent to each other
    def ifAdjacent(self, position1, position2):
        if position1[0] == position2[0]:
            if abs(position1[1]-position2[1]) == 1:
                return True
        elif position1[1] == position2[1]:
            if abs(position1[0]-position2[0]) == 1:
                return True
        return False

    #not finished
    #determines who wins
    def win(self, identity, gameBoard):
        if not self.generatePossibleMoves(gameBoard, identity):
            return False

#missing multiple jumps situation
