import sys
sys.path.append('./')
from gameBoard import *
from darkPlayer import *
import random

#get agent's identity based on my choice
def getIdentity():
    opponent_piece = raw_input("Choose your color, light or dark? ")
    if opponent_piece.upper() == "DARK":
        opponent = DARKPLAYER
        identity = LIGHTPLAYER
        return identity
    elif opponent_piece.upper() == "LIGHT":
        opponent = LIGHTPLAYER
        identity = DARKPLAYER
        return identity
    else:
        print "Invalid input. Please enter again: "
        return getIdentity()

def firstRound(agent, opponent, gameboard):
    if not agent.identity :
        s = raw_input("Which piece do you want to remove? (Format: row, col)")
        pieces = s.split(",")
        darkmove = (int (pieces[0]), int (pieces[1]))
        print "You want to remove: "+ str(darkmove)
        gameboard.updateBoard(darkmove, None, opponent.identity)
        gameboard.drawBoard()
        firstmove = agent.generateFirstMove_Light(darkmove, gameboard)
        print "I want to remove: " + str(firstmove)
        gameboard.updateBoard(firstmove,None, agent.identity)
        gameboard.drawBoard()
    else:
        firstmove = agent.generateFirstMove_Dark()
        print "I want to remove: " + str(firstmove)
        gameboard.updateBoard(firstmove, None, agent.identity)
        gameboard.drawBoard()
        s = raw_input("Which piece do you want to remove? (Format: row, col)")
        pieces = s.split(",")
        darkmove = (int (pieces[0]), int (pieces[1]))
        print "You want to remove: "+ str(darkmove)
        gameboard.updateBoard(darkmove, None, opponent.identity)
        gameboard.drawBoard()

def askForMove(opponent, gameboard):
    s = raw_input("Which piece do you want to move? (Format: row, col)")
    pieces = s.split(",")
    start = (int (pieces[0]), int (pieces[1]))
    s = raw_input("which position do you want to jump to: ")
    pieces = s.split(",")
    end = (int (pieces[0]), int (pieces[1]))
    legal = opponent.testLegatMove(gameboard,opponent.identity,start, end)
    if legal:
        return (start, end)
    else:
        print "Invalid move. Try again."
        return askForMove(opponent, gameboard)

def main():
    identity = getIdentity()
    agent = Player(identity, 1)
    opponent = Player(not identity, 1)
    gameboard = gameBoard.gameBoard()
    gameboard.startState()
    firstRound(agent, opponent, gameboard)
    while not agent.win(gameboard) and not opponent.win(gameboard):
        if agent.identity:
            move = agent.minimax(agent.identity, gameboard,4)[1]
            print "This is my move: "+ str(move)
            gameboard.updateBoard(move[0], move[1], DARK)
            gameboard.drawBoard()
            if not agent.win(gameboard):
                move = askForMove(opponent, gameboard)
                print "This is your move: " + str(move)
                gameboard.updateBoard(move[0], move[1], LIGHT)
                gameboard.drawBoard()
            else:
                break
            agent.roundIncrement()
            opponent.roundIncrement()
        else:
            move = askForMove(opponent, gameboard)
            print "This is your move: " + str(move)
            gameboard.updateBoard(move[0], move[1] , DARK)
            gameboard.drawBoard()
            if not opponent.win(gameboard):
                move = agent.minimax(agent.identity, gameboard, 4)[1]
                print "This is my move: "+ str(move)
                gameboard.updateBoard(move[0], move[1], LIGHT)
                gameboard.drawBoard()
            else:
                break
            agent.roundIncrement()
            opponent.roundIncrement()
    if agent.win(gameboard):
        print "I win!\n\n\n"
    if opponent.win(gameboard):
        print "You win!\n\n\n"

main()
# game = gameBoard.gameBoard()
# d = Player(DARKPLAYER,1)
# l = Player(LIGHTPLAYER,1)
# game.startState()
# move = d.generateFirstMove_Dark()
# game.updateBoard(move, None, DARK)
# move = l.generateFirstMove_Light(move, game)
# game.updateBoard(move, None, LIGHT)
#
# for i in range (1,8):
#     for j in range (1,9):
#         game.board[i-1][j-1] = EMPTY
# for j in range(3,9):
#     game.board[7][j-1] = EMPTY
# print d.win(game)
# game.updateBoard((6,2), None, DARK)
# game.updateBoard((4,2), None, DARK)
# game.updateBoard((2,2), None, DARK)
# for i in range (6,9):
#     for j in range(4,9):
#         game.board[i-1][j-1] = EMPTY
#
# game.updateBoard((6,2), None, DARK)
# game.updateBoard((6,3), None, DARK)
# game.updateBoard((7,3), None, DARK)
# game.updateBoard((6,3), None, DARK)
# game.updateBoard((8,4), None, DARK)
# game.updateBoard((4,8), None, DARK)
# game.updateBoard((6,4), None, DARK)
# game.updateBoard((4,6), None, DARK)
# print "--------"
# game.drawBoard()
# result = d.availableMoves(game,DARKPLAYER)
# print result
# print "********"
# game.drawBoard()
# print "#DARK: " + str(len(moveable))
# print "#LIGHT: " + str(len(unmoveable))
# print d.minimax(DARKPLAYER, game, 2)
