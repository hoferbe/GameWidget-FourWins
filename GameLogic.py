import numpy as np


class GameLogic:

    def __init__(self, playerOneID, playerTwoID):
        self.grid = np.zeros((7, 7))

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

    def currentPlayerID(self):
        if self.currentPlayer == 1:
            return self.playerOneID
        else:
            return self.playerTwoID

    def changePlayer(self):
        if self.currentPlayer == 1:
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

    def didFindWinner(self):
        return self.foundWinner

    def makeMove(self, move, playerID):
        column = self.grid[move]
        if column[-1] != 0:
            self.setWinner(False, playerID)
        else:
            moveRow = np.count_nonzero(column)
            self.grid[move][moveRow] = playerID
            self.didWin(move, moveRow)
            if self.currentPlayer == 1:
                self.currentPlayer = 2
            else:
                self.currentPlayer = 1

    def didWin(self, column, row):
        x = column
        y = row
        for i in range(4):
            if i <= x <= 3+i:
                checkingArr = self.getLine(x-i, y, 1, 0)
                if np.all(checkingArr == checkingArr[0]):
                    self.setWinner(True, self.currentPlayerID())
            if i <= x <= 3+i and i <= y <= 3+i:
                checkingArr = self.getLine(x-i, y-i, 1, 1)
                if np.all(checkingArr == checkingArr[0]):
                    self.setWinner(True, self.currentPlayerID())
            if i <= y <= 3+i:
                checkingArr = self.getLine(x, y-i, 0, 1)
                if np.all(checkingArr == checkingArr[0]):
                    self.setWinner(True, self.currentPlayerID())
            if i <= y <= 3+i and 3-i <= x <= 6-i:
                checkingArr = self.getLine(x+i, y-i, -1, 1)
                if np.all(checkingArr == checkingArr[0]):
                    self.setWinner(True, self.currentPlayerID())
        return

    def getLine(self, x, y, changeX, changeY):
        arr = np.empty(4)
        for i in range(4):
            arr[i] = self.grid[x+i*changeX][y + i*changeY]
        return arr

    def setWinner(self, winner, playerID):
        self.foundWinner = True
        if not winner:
            self.changePlayer()
        self.winnerID = self.currentPlayerID()

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
