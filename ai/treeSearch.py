'''
Created on Mar 15, 2014

@author: will
'''
from term2048.board import Board
from term2048.game import Game
import sys
from copy import deepcopy

moves = [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]


def treeSearch(b, score):
    #return the score if we've won or if there is only one value left
    if b.won() or len(b.getEmptyCells()) == b.size() ** 2:
        return score
    #return 0 if we've lost
    if not b.canMove():
        return 0
    #recurse
    #assuming that UP, DOWN, LEFT and RIGHT are the only moves
    bestScore = float('-inf')
    for m in moves:
        #copy the board
        boardCopy = deepcopy(b)
        #do our move - don't add a tile, so its not stochastic
        moveScore = treeSearch(boardCopy,
                            score + boardCopy.move(m, add_tile=False))
        if moveScore > bestScore:
            bestScore = moveScore
    return bestScore


def chooseMove(g):
    #based on the board, choose the best move
    bestScore = float('-inf')
    for m in moves:
        boardCopy = deepcopy(g.board)
        score = treeSearch(boardCopy,
                           g.score + boardCopy.move(m, add_tile=False))
        if score > bestScore:
            bestMove = m
            bestScore = score
    return bestMove


def start_ai():
    #make a game to use
    g = Game()
    #start the ai loop
    try:
        while True:
            print "\n"
            print g.__str__(margins={'left': 4, 'top': 4, 'bottom': 4})
            if g.board.won() or not g.board.canMove():
                break
            m = chooseMove(g)
            g.incScore(g.board.move(m))
    except KeyboardInterrupt:
        return
