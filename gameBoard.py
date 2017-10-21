DARK = 'X'
LIGHT = 'O'
EMPTY = '.'
import sys
sys.path.append('./')

class gameBoard:

    def __init__(self, width = 8):
        self.width = width

    def startState(self):
        self.board = [[LIGHT for x in range(self.width)]for y in range(self.width)]
        for j in range (len(self.board)):
            if j % 2 :
                i = 1
            else:
                i = 0
            while i < len(self.board) :
                self.board[j][i] = DARK
                i += 2
        return self.board

    def drawBoard(self):
        for row in self.board:
            print row

    def updateBoard(self, remove, add, identity):
        self.board[remove[0]-1][remove[1]-1] = EMPTY
        if add:
            self.board[add[0]-1][add[0]-1] = identity
        return self.board

    def getGameState(self):
        return self.board

    def getCellInfo (self, position):
        return self.board[position[0]][position[1]]

    def getEmptyCell(self):
        emptyCells = []
        for i in range (len(self.board)):
            for j in range (len(self.board[0])):
                if self.board[i][j] == EMPTY:
                    position = (i+1, j+1)
                    emptyCells.append(position)
        return emptyCells

    def getDarkCell(self):
        darkCells = []
        for i in range (len(self.board)):
            for j in range (len(self.board[0])):
                if self.board[i][j] == DARK:
                    position = (i+1, j+1)
                    darkCells.append(position)
        return darkCells

    def getLightCell(self):
        lightCells = []
        for i in range (len(self.board)):
            for j in range (len(self.board[0])):
                if self.board[i][j] == LIGHT:
                    position = (i+1, j+1)
                    lightCells.append(position)
        return lightCells
