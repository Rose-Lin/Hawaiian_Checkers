import sys
sys.path.append("./")
import gameBoard
import copy
from random import randint
import math
from Node import *
import util

DARKPLAYER = 1
LIGHTPLAYER = 0
DARK = 'X'
LIGHT = 'O'
EMPTY = '.'
MAX = 1
MIN = 0
POSSIBLE_FIRST_MOVE_DARK = [(8,8),(1,1),(5,5),(4,4)]

class Player:

    def __init__(self, identity, round, moves):
        self.identity = identity
        self.moves = moves
        self.round = round

    def minimax(self, identity, gameBoard,depth_limit,alpha = -9999, beta = 9999, move=None,level=0 ):
        if identity:
            cell = DARK
        else:
            cell = LIGHT
        if level == depth_limit:
            return self.evaluation(gameBoard,identity), move
        possibleMoves = self.availableMoves(gameBoard, identity)
        print possibleMoves
        frontier = util.Queue()
        currentState = Node(gameBoard,None,level,move)
        for start in possibleMoves.keys():
            for end in possibleMoves[start]:
                if end:
                    game = copy.deepcopy(gameBoard)
                    game.board = game.updateBoard(start,end,cell)
                    newNode = Node(game, currentState, currentState.level+1,(start,end))
                    frontier.push(newNode)
        if self.tellMinMax(level+1) :
            currentBestValue = -9999
            currentState.gameBoard.drawBoard()
            bestMove = currentState.move
            while not frontier.isEmpty():
                currentNode = frontier.pop()
                if identity:
                    newID = LIGHTPLAYER
                else:
                    newID = DARKPLAYER
                bestValue, move = self.minimax(newID, currentNode.gameBoard,depth_limit, alpha, beta, currentNode.move,currentNode.level)
                move = currentNode.move
                if self.win(identity,currentNode.gameBoard):
                    bestValue = -9999
                if bestValue > alpha:
                    alpha = bestValue
                    bestMove = move
                if alpha >= beta:
                    return beta, bestMove
            return alpha, bestMove
        else:
            currentBestValue = 9999
            currentState.gameBoard.drawBoard()
            bestMove = currentState.move
            while not frontier.isEmpty():
                currentNode = frontier.pop()
                if identity:
                    newID = LIGHTPLAYER
                else:
                    newID = DARKPLAYER
                bestValue, move = self.minimax(newID,currentNode.gameBoard,depth_limit,alpha, beta,currentNode.move,currentNode.level)
                move =currentNode.move
                if self.win(identity,currentNode.gameBoard):
                    bestValue = 9999
                if bestValue < beta:
                    beta = bestValue
                    bestMove = move
                if beta <= alpha:
                    return alpha, bestMove
            return beta, bestMove

    def tellMinMax(self, level):
        if level % 2 == 0 and level:
            return MIN
        return MAX

    def evaluation(self, gameBoard,identity):
        darkCells = gameBoard.getDarkCell()
        lightCells = gameBoard.getLightCell()
        darkScore = len(darkCells)
        lightScore = len(lightCells)
        if not identity:
            return darkScore - lightScore
        else:
            return lightScore - darkScore

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
            moveable = gameBoard.getLightCell()
            unmoveable = gameBoard.getDarkCell()
        emptyCells = gameBoard.getEmptyCell()
        possibleMoves = self.__generatePossibleMoves_Helper(gameBoard, moveable, unmoveable, emptyCells)
        possibleMoves = self.__generateMultipleJumps(identity, possibleMoves, gameBoard, unmoveable, emptyCells)
        return possibleMoves

    def __generateMultipleJumps(self, identity, possibleMoves, gameBoard, unmoveable, emptyCells):
        game = copy.deepcopy(gameBoard)
        empty = copy.deepcopy(emptyCells)
        p = copy.deepcopy(possibleMoves)
        for move in possibleMoves.keys():
            p = self.__generateMultipleJumps_Helper(p, game, move, unmoveable, empty, identity,int (math.log(gameBoard.width,2)) )
        return p

    #change the endPositions in possibleMoves, if the check can jump over multiple times
    #Since the check cannot turn, the maximun number of jump is 3
    #The count variable counts the time the check jumps [0:2]
    def __generateMultipleJumps_Helper(self,possibleMoves, game, move, unmoveable, empty, identity, count = 2):
        empty_copy = copy.deepcopy(empty)
        if not count:
            return possibleMoves
        for m in possibleMoves[move]:
            game.updateBoard(move, m, identity)
            if m in empty_copy:
                empty_copy.remove(m)
            new_move = self.__generatePossibleMoves_Helper(game, [m], unmoveable,empty_copy)
            if new_move:
                for nm in new_move[m]:
                    if not self.__ifTurned(move, nm):
                        possibleMoves[move] += [nm]
        return self.__generateMultipleJumps_Helper(possibleMoves,game, move,unmoveable,empty_copy,identity,count-1)


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
    #gameBoard already updated based on the move
    def win(self, identity, gameBoard):
        if identity:
            newID = LIGHTPLAYER
        else:
            newID = DARKPLAYER
        otherP_possibleMoves = self.availableMoves(gameBoard, newID)
        if not otherP_possibleMoves:
            return True
        return False

    #for a given move, return the features of cell east to it
    #return (check, celPosition)
    def getEast (self, gameBoard, move):
        if not move[1] == gameBoard.width:
            eastMove = (move[0], move[1]+1)
            return gameBoard.getCellInfo(eastMove), eastMove
        return None, None

    def getWest (self, gameBoard, move):
        if not move[1] == 1:
            westMove = (move[0], move[1]-1)
            return gameBoard.getCellInfo(westMove), westMove
        return None, None

    def getNorth(self, gameBoard, move):
        if not move[0] == 1:
            northMove = (move[0]-1, move[1])
            return gameBoard.getCellInfo(northMove), northMove
        return None, None

    def getSouth(self, gameBoard, move):
        if not move[0] == gameBoard.width:
            southMove = (move[0]+1, move[1])
            return gameBoard.getCellInfo(southMove), southMove
        return None, None

    def availableMoves(self, gameBoard, identity):
        result = {}
        if identity:
            moveable = gameBoard.getDarkCell()
            jumpOver = LIGHT
        else:
            moveable = gameBoard.getLightCell()
            jumpOver = DARK
        for move in moveable:
            eastMove = []
            westMove = []
            northMove = []
            southMove = []
            eastMove = self.jumpToEast(eastMove, gameBoard, identity, jumpOver, move)
            westMove = self.jumpToWest(westMove, gameBoard, identity, jumpOver, move)
            northMove = self.jumpToNorth(northMove, gameBoard, identity, jumpOver, move)
            southMove = self.jumpToSouth(southMove, gameBoard, identity, jumpOver, move)
            result[move] = eastMove + westMove + northMove + southMove
        return result

    #jump to east for a single check
    #return a list of possible end position for the check
    def jumpToEast(self, result, gameBoard, identity, jumpOver, moveable):
        game = copy.deepcopy(gameBoard)
        eastCell, eastPosition = self.getEast(gameBoard, moveable)
        #if the cell in the east is opponent's check
        if  eastCell == jumpOver:
            emptyCell, emptyPosition = self.getEast(gameBoard, eastPosition)
            if  emptyCell == EMPTY:
                result.append(emptyPosition)
                game.updateBoard(eastPosition, emptyPosition, identity)
                self.jumpToEast(result, game, identity, jumpOver, emptyPosition)
        return result

    def jumpToWest (self, result, gameBoard, identity, jumpOver, moveable):
        game = copy.deepcopy(gameBoard)
        westCell, westPosition = self.getWest(gameBoard, moveable)
        #if the cell in the east is opponent's check
        if  westCell == jumpOver:
            emptyCell, emptyPosition = self.getWest(gameBoard, westPosition)
            if  emptyCell == EMPTY:
                result.append(emptyPosition)
                game.updateBoard(westPosition, emptyPosition, identity)
                self.jumpToWest(result, game, identity, jumpOver, emptyPosition)
        return result

    def jumpToNorth(self, result, gameBoard, identity, jumpOver, moveable):
        game = copy.deepcopy(gameBoard)
        northCell, northPosition = self.getNorth(gameBoard, moveable)
        #if the cell in the east is opponent's check
        if  northCell == jumpOver:
            emptyCell, emptyPosition = self.getNorth(gameBoard, northPosition)
            if  emptyCell == EMPTY:
                result.append(emptyPosition)
                game.updateBoard(northPosition, emptyPosition, identity)
                self.jumpToNorth(result, game, identity, jumpOver, emptyPosition)
        return result

    def jumpToSouth(self, result, gameBoard, identity, jumpOver, moveable):
        game = copy.deepcopy(gameBoard)
        southCell, southPosition = self.getSouth(gameBoard, moveable)
        #if the cell in the east is opponent's check
        if  southCell == jumpOver:
            emptyCell, emptyPosition = self.getSouth(gameBoard, southPosition)
            if  emptyCell == EMPTY:
                result.append(emptyPosition)
                game.updateBoard(southPosition, emptyPosition, identity)
                self.jumpToSouth(result, game, identity, jumpOver, emptyPosition)
        return result

    #given a move of a player, return true if the move is legal and false otherwise
    def testLegatMove(self, gameBoard, identity, start, end):
        availableMoves = self.availableMoves(gameBoard, identity)
        if start in availableMoves.keys():
            if end in availableMoves[start]:
                return True
        return False
