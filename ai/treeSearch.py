'''
Created on Mar 15, 2014

@author: will
'''
from term2048.board import Board
from term2048.game import Game
from copy import deepcopy

moves = [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]


def treeSearch(b, score, depth=10):
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
        if not boardCopy == b:
            #do our move - don't add a tile, so its not stochastic
            moveScore = treeSearch(boardCopy, moveScore, depth=depth - 1)
        print "After move %d:%d\n%s" % (m, moveScore, boardCopy)
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
        print "Done with %d, " % m,
    print "Chose move %d" % bestMove
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
