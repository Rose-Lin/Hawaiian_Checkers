import sys
sys.path.append('./')
from gameBoard import *
from darkPlayer import *
import random

game = gameBoard.gameBoard()
d = Player(DARKPLAYER,1,[])
l = Player(LIGHTPLAYER,1,[])
game.startState()
move = d.generateFirstMove_Dark()
game.updateBoard(move, None, DARK)
move = l.generateFirstMove_Light(move, game)
game.updateBoard(move, None, LIGHT)
for i in range (1,6):
    for j in range (1,9):
        game.board[i-1][j-1] = EMPTY
game.updateBoard((6,2), None, DARK)
# game.updateBoard((4,2), None, DARK)
# game.updateBoard((2,2), None, DARK)
# for i in range (6,9):
#     for j in range(4,9):
#         game.board[i-1][j-1] = EMPTY

game.updateBoard((6,2), None, DARK)
game.updateBoard((6,3), None, DARK)
game.updateBoard((7,3), None, DARK)
# game.updateBoard((6,3), None, DARK)
# game.updateBoard((8,4), None, DARK)
# game.updateBoard((4,8), None, DARK)
# game.updateBoard((6,4), None, DARK)
# game.updateBoard((4,6), None, DARK)
# print "--------"
game.drawBoard()
moveable = game.getDarkCell()
unmoveable = game.getLightCell()
emptyCells = game.getEmptyCell()
p = d.generatePossibleMoves(game, DARKPLAYER)
pl = l.generatePossibleMoves(game, LIGHTPLAYER)
#print "DARKPLAYER"
#print p
#print "LIGHTPLAYER"
#print pl
#print "----------"
result = d.availableMoves(game,DARKPLAYER)
print result
# print p
print "********"
var = raw_input("Which piece do you want to move:")
pieces = var.split(",")
start = (int (pieces[0]), int (pieces[1]))
var = raw_input("which position do you want to jump to: ")
pieces = var.split(",")
end = (int (pieces[0]), int (pieces[1]))
print d.testLegatMove(game, LIGHTPLAYER, start, end)

#print result
#game.updateBoard((6,4),(6,2),DARK)
#game.drawBoard()
# print "#DARK: " + str(len(moveable))
# print "#LIGHT: " + str(len(unmoveable))
# print d.minimax(DARKPLAYER, game, 2)
