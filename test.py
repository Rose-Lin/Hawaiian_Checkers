from gameBoard import *
from darkPlayer import *
import random

game = gameBoard.gameBoard()
game.startState()
game.drawBoard()
game.updateBoard((6,2), None, DARK)
game.updateBoard((4,2), None, DARK)
game.updateBoard((2,2), None, DARK)
print "------"
game.drawBoard()
d = Player(DARKPLAYER,1,[], game.startState())
move = (8,2)
unmoveable = game.getLightCell()
empty = game.getEmptyCell()
moveable = game.getDarkCell()
possibleMoves = d.generatePossibleMoves(game, DARK)
print possibleMoves
j = d.generateMultipleJumps_Helper(possibleMoves, game, move, unmoveable, empty, DARK, 2)
print j
