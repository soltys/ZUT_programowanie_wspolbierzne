import sys
import random
import threading
       
    
class Orientation():
    HORIZONTAL = 0
    VERTICAL = 1


    
class Board():
    NOTHING = 0
    MISS = 1
    SHIP = 2
    HIT = 3
    def __init__(self, boardHeight, boardWidth):
        self.boardRows = boardHeight 
        self.boardColumns  = boardWidth
        self.board = [[0 for x in xrange(boardWidth )] for y in xrange(boardHeight )]

    def getValue(self,row,col):
        return self.board[row][col]
    
    def placeShip(self, row, col):
        self.board[row][col] = Board.SHIP
        
    def printBoard(self):
        for row in xrange(self.boardRows):
            for col in xrange(self.boardColumns):            
                if self.board[row][col] == Board.NOTHING :
                    sys.stdout.write("_")
                if self.board[row][col] == Board.MISS :
                    sys.stdout.write("*")
                if self.board[row][col] == Board.SHIP :
                    sys.stdout.write("#")
                if self.board[row][col] == Board.HIT :
                    sys.stdout.write("X")

            print ""
        print "_ nothing"
        print "* miss"
        print "# ship"
        print "X hit"

class Player(threading.Thread):
    BOARD_HEIGHT = 10
    BOARD_WIDTH = 10
    def __init__(self, playerName):
          threading.Thread.__init__(self)
          self.playerName = playerName
          self.board = Board(Player.BOARD_HEIGHT,Player.BOARD_WIDTH)
          for x in xrange(4):
              self.placeShip(2,random.randint(0,1))
          for x in xrange(3):
              self.placeShip(3,random.randint(0,1))
          for x in xrange(2):
              self.placeShip(4,random.randint(0,1))
          self.placeShip(1,random.randint(0,1))            
        
    def placeShip(self, shipSize, orientation):
        placed = False
        if orientation == Orientation.HORIZONTAL:
            while not placed:
                row = random.randint(0, Player.BOARD_HEIGHT-1)
                col = random.randint(0, Player.BOARD_WIDTH-1)
                if col+shipSize > Player.BOARD_WIDTH:
                    continue
                
                emptySpot = True
                for i in xrange(col, col+shipSize):
                    if  not self.board.getValue(row, i) == Board.NOTHING:
                        emptySpot = False
                if emptySpot:
                    placed = True
                    for i in xrange(col, col+shipSize):
                        self.board.placeShip(row,i)
        if orientation == Orientation.VERTICAL:
            while not placed:
                row = random.randint(0, Player.BOARD_HEIGHT-1)
                col = random.randint(0, Player.BOARD_WIDTH-1)
                if row+shipSize > Player.BOARD_HEIGHT:
                    continue
                
                emptySpot = True
                for i in xrange(row, row+shipSize):
                    if  not self.board.getValue(i, col) == Board.NOTHING:
                        emptySpot = False
                if emptySpot:
                    placed = True
                    for i in xrange(row, row+shipSize):
                        self.board.placeShip(i,col)
                        
    def printPlayerBoard(self):
        print "Player: ", self.playerName
        self.board.printBoard();

if __name__ == "__main__":
    p = Player("JacK")
    p.printPlayerBoard();
