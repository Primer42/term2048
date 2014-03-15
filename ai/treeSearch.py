'''
Created on Mar 15, 2014

@author: will
'''
from term2048.board import Board
from term2048.game import Game
from copy import deepcopy
import Queue
import threading

moves = [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]


def treeSearch(b, score, depth=5):
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

        #do our move - don't add a tile, so its not stochastic
        moveScore = score + boardCopy.move(m, add_tile=False)

        #boardCopy.move(m, add_tile=False)
        #moveScore = max([b.getCell(x, y) for x, y in combinations_with_replacement(range(b.size()), 2)])

        moveScore = treeSearch(boardCopy, moveScore, depth - 1)
        moveScore = moveScore * len(boardCopy.getEmptyCells()) * depth
        #print "depth %d move %d:%d\n%s" % (depth, m, moveScore, boardCopy)
        bestScore = max(bestScore, moveScore)
    return bestScore


def testMove(q, m, b, g,):
    incScore = b.move(m, add_tile=False)
    if b == g.board:
        q.put((m, b, 0))
    q.put((m, b, treeSearch(b, g.score + incScore)))


def chooseMove(g):
    #based on the board, choose the best move
    bestScore = float('-inf')
    q = Queue.Queue()
    for m in moves:
        boardCopy = deepcopy(g.board)
        t = threading.Thread(target=testMove, args=(q, m, boardCopy, g))
        t.daemon = True
        t.start()

    for _ in moves:
        m, b, score = q.get()
        if b == g.board:
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
