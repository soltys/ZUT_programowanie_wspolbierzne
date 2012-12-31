import sys
class Board():
    
    def __init__(self, boardHeight, boardWidth):
        self.boardRows = boardHeight 
        self.boardColumns  = boardWidth
        self.board = [[0 for x in xrange(boardHeight)] for y in xrange(boardWidth )]

    def printBoard(self):
        for col in xrange(self.boardColumns):
            for row in xrange(self.boardRows):
                if self.board[col][row] == 0 :
                    sys.stdout.write("_")

            print ""
        print "_ nothing"
        print "* miss"
        print "X hit"

if __name__ == "__main__":
    b = Board(8,8);
    b.printBoard();
