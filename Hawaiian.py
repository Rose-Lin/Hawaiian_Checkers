from gameBoard import *
from darkPlayer import *
import random

game = gameBoard.gameBoard()
d = Player(DARKPLAYER,1,[], game.startState())
l = Player(LIGHTPLAYER,1,[], game.startState())
game.drawBoard()
move = d.generateFirstMove_Dark()
print move
game.updateBoard(move, None, DARK)
game.drawBoard()
move = l.generateFirstMove_Light(move, game)
print move
game.updateBoard(move, None, LIGHT)
game.drawBoard()

game.updateBoard((6,2), None, DARK)
game.updateBoard((4,2), None, DARK)
game.updateBoard((2,2), None, DARK)
game.updateBoard((4,4), None, DARK)
game.updateBoard((8,4), None, DARK)
game.updateBoard((8,6), None, DARK)
print "--------"
game.drawBoard()
movable = game.getDarkCell()
unmoveable = game.getLightCell()
emptyCells = game.getEmptyCell()
p = d.generatePossibleMoves(game, DARK)
#j = d.generateMultipleJumps_Helper(p, game, (8,2), unmoveable, emptyCells, DARK, 2)
#j = d.generateMultipleJumps(DARK,p, game, unmoveable, emptyCells)
print "******"
print p
