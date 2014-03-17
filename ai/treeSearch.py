'''
Created on Mar 15, 2014

@author: will
'''
from term2048.board import Board
from term2048.game import Game
from copy import deepcopy

moves = [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]

nodeLookup = dict()


class node():
    def __init__(self, _board, _parent):
        global nodeLookup

        self.board = _board
        self.parent = _parent
        self.children = []

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

                self.children.append((moveScore, child))

    def getParents(self):
        if self.parent is None:
            return []
        else:
            parents = self.parent.getParents()
            parents.append(self.parent)
            return parents

    def getScore(self):
        '''
        maximize the score
        '''
        #get the best child
        if not len(self.children):
            return 0
        bestChild = sorted(self.children, key=lambda c: c[1].getScore())[-1]
        return bestChild[0] * len(self.board.getEmptyCells()) / (self.board.size() ** 2)

    def getDepthScore(self, depth=1.0):
        '''
        maximize the score, and decrement moves further in the future.
        '''
        #get the best child
        if not len(self.children):
            return 0
        depthChildren = [c + (c[1].getDepthScore(depth + 1),) for c in self.children]
        bestChild = sorted(depthChildren, key=lambda c: c[2])[-1]
        return (bestChild[0] * len(self.board.getEmptyCells()) / (self.board.size() ** 2) / depth) + bestChild[2]

    def __eq__(self, other):
        return self.board == other.board

    def __ne__(self, other):
        return not self == other


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
        #moveScore = n.getScore()
        moveScore = n.getDepthScore()
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
