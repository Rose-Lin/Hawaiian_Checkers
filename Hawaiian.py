import sys
sys.path.append('./')
from gameBoard import *
from darkPlayer import *
import random

game = gameBoard.gameBoard()
d = Player(DARKPLAYER,1,[])
l = Player(LIGHTPLAYER,1,[])
game.startState()
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
game.updateBoard((6,6), None, DARK)
print "--------"
game.drawBoard()
moveable = game.getDarkCell()
unmoveable = game.getLightCell()
emptyCells = game.getEmptyCell()
p = d.generatePossibleMoves(game, DARKPLAYER)
pl = l.generatePossibleMoves(game, LIGHTPLAYER)
print "DARKPLAYER"
print p
print "LIGHTPLAYER"
print pl
print "----------"
result = d.availableMoves(game,DARKPLAYER)
print result
#game.updateBoard((6,4),(6,2),DARK)
#game.drawBoard()
print "#DARK: " + str(len(moveable))
print "#LIGHT: " + str(len(unmoveable))
print d.minimax(DARK,game,2)
