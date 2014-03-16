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

nodeLookup = dict()


class node():
    def __init__(self, _board, _parent):
        global nodeLookup

        self.board = _board
        self.parent = _parent
        children = []

        self.score = 0

        if not self.board.won() and \
                self.board.canMove() and \
                self.board.canCollapse() and \
                not self in self.getParents():
            for m in moves:
                boardCopy = deepcopy(self.board)
                moveScore = boardCopy.move(m, add_tile=False)
                try:
                    child = nodeLookup[str(boardCopy)]
                except KeyError:
                    child = node(boardCopy, self)
                    nodeLookup[str(boardCopy)] = child

                children.append(child)
                totMoveScore = (moveScore * (len(self.board.getEmptyCells()) / float(self.board.size() ** 2))) + child.score
                self.score = max(self.score, totMoveScore)

    def getParents(self):
        if self.parent is None:
            return []
        else:
            parents = self.parent.getParents()
            parents.append(self.parent)
            return parents

    def __eq__(self, other):
        return self.board == other.board

    def __ne__(self, other):
        return not self == other

def treeSearch(b, score, depth=8):
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
        moveScore = moveScore * len(boardCopy.getEmptyCells())
        #print "depth %d move %d:%d\n%s" % (depth, m, moveScore, boardCopy)
        bestScore = max(bestScore, moveScore)
    return bestScore


'''
def testMove(q, m, b, g,):
    incScore = b.move(m, add_tile=False)
    if b == g.board:
        q.put((m, b, 0))
    q.put((m, b, treeSearch(b, g.score + incScore)))
'''


def chooseMove(g):
    global nodeLookup
    nodeLookup.clear()

    #based on the board, choose the best move
    bestScore = float('-inf')
    #q = Queue.Queue()
    for m in moves:
        '''
        boardCopy = deepcopy(g.board)
        t = threading.Thread(target=testMove, args=(q, m, boardCopy, g))
        t.daemon = True
        t.start()

    for _ in moves:
        m, _, score = q.get()
        if score > bestScore or bestScore < 0:
            bestMove = m
            bestScore = score
        '''
        boardCopy = deepcopy(g.board)
        incScore = boardCopy.move(m, add_tile=False)
        if boardCopy == g.board:
            continue
        n = node(boardCopy, None)
        moveScore = n.score
        print "Score for %d is %f" % (m, moveScore)
        if moveScore > bestScore:
            bestMove = m
            bestScore = moveScore

    print "Chose move %d" % bestMove
    return bestMove


def start_ai():
    #make a game to use
    g = Game(scores_file='./score.txt')
    #start the ai loop
    numMoves = 0
    try:
        while True:
            numMoves += 1
            print "\nMove %d\n" % numMoves
            print g.__str__(margins={'left': 4, 'top': 1, 'bottom': 1})
            if g.board.won() or not g.board.canMove():
                break
            m = chooseMove(g)
            g.incScore(g.board.move(m))
        g.saveBestScore()
    except KeyboardInterrupt:
        g.saveBestScore()
