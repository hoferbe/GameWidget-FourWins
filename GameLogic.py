import numpy


class GameLogic:

    def __init__(self, playerOneID, playerTwoID):
        self.grid = numpy.zeros((7, 7))

        self.playerOneID = playerOneID
        self.playerTwoID = playerTwoID
        self.currentPlayer = 1

        self.foundWinner = False
        self.winnerID = 0

    def move(self, move, playerID):
        worked = False
        if playerID == self.playerOneID and self.currentPlayer == 1:
            self.makeMove(move, playerID)
            self.currentPlayer = 2
            worked = True
        elif playerID == self.playerTwoID and self.currentPlayer == 2:
            self.makeMove(move, playerID)
            self.currentPlayer = 1
            worked = True
        return worked

    def didFindWinner(self):
        return self.foundWinner

    def makeMove(self, move, playerID):
        column = self.grid[move]
        if column[-1] != 0:
            self.setWinner(False, playerID)
        else:
            moveRow = numpy.count_nonzero(column)
            self.grid[move][moveRow] = playerID
            self.didWin(move, moveRow)
            if self.currentPlayer == 1:
                self.currentPlayer = 2
            else:
                self.currentPlayer = 1

    def didWin(self, column, row):
        return

    def setWinner(self, winner, playerID):
        self.foundWinner = True
        if winner:
            self.winnerID = playerID
        elif self.currentPlayer == 1:
            self.winnerID = self.playerOneID
        else:
            self.winnerID = self.playerTwoID

    def getGrid(self):
        playerGrid = []
        for col in self.grid:
            vec = []
            for el in col:
                if el == self.playerOneID:
                    vec.append(1)
                elif el == self.playerTwoID:
                    vec.append(2)
                else:
                    vec.append(0)
            playerGrid.append(vec)

        return playerGrid
