'''
Created on Mar 15, 2014

@author: will
'''
from term2048.board import Board
from term2048.game import Game
from copy import deepcopy

moves = [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]


def treeSearch(b, score, depth=4):
    #return the score if we've won or if there is only one cell of each value left
    if b.won() or not b.canCollapse() or depth == 0:
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
        moveScore = score + boardCopy.move(m, add_tile=False)
        #do our move - don't add a tile, so its not stochastic
        moveScore = treeSearch(boardCopy, moveScore, depth - 1)
        moveScore = moveScore * len(boardCopy.getEmptyCells())# / depth
        #print "depth %d move %d:%d\n%s" % (depth, m, moveScore, boardCopy)
        bestScore = max(bestScore, moveScore)
    return bestScore


def chooseMove(g):
    #based on the board, choose the best move
    bestScore = float('-inf')
    for m in moves:
        boardCopy = deepcopy(g.board)
        score = treeSearch(boardCopy,
                           g.score + boardCopy.move(m, add_tile=False))
        #print "move %d: score %d\n%s" % (m, score, boardCopy)
        if boardCopy == g.board:
            continue
        if score > bestScore:
            bestMove = m
            bestScore = score
    print "Chose move %d" % bestMove
    return bestMove


def start_ai():
    #make a game to use
    g = Game(scores_file='./score.txt')
    #start the ai loop
    try:
        while True:
            print "\n"
            print g.__str__(margins={'left': 4, 'top': 4, 'bottom': 4})
            if g.board.won() or not g.board.canMove():
                break
            m = chooseMove(g)
            g.incScore(g.board.move(m))
        g.saveBestScore()
    except KeyboardInterrupt:
        g.saveBestScore()
