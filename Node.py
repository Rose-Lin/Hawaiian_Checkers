import sys
sys.path.append('./')
import gameBoard
class Node:

    def __init__(self, gameBoard, parentBoard, level,move):
        self.gameBoard = gameBoard
        self.parentBoard = parentBoard
        self.level = level
        self.move = move
