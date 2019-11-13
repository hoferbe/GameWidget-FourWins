from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from GameLogic import *


class GameWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        lay = QGridLayout(self)
        self.buttons = []
        for i in range(7):
            btn = QPushButton(str(i))
            #btn.clicked.connect(getattr(self, "button"+str(i)+"pressed"))
            self.buttons.append(btn)
            lay.addWidget(btn, 1, i)

        self.drawArea = QWidget()
        self.drawArea.setFixedHeight(self.drawArea.width())
        lay.addWidget(self.drawArea, 0, 0, 1, 7)

        self.playerOneColor = Qt.green
        self.playerTwoColor = Qt.red

        self.gameIsRunning = False
        self.game = None
        self.playerOne = -1
        self.playerTwo = -2
        self.currentPlayer = self.playerOne

        self.saveGrid = None

        self.startGame()

        self.drawit = True

    def startGame(self):
        if not self.gameIsRunning:
            for i, btn in enumerate(self.buttons):
                btn.clicked.connect(getattr(self, "button"+str(i)+"pressed"))
            self.gameIsRunning = True
            self.playerOne = -1
            self.playerTwo = -2
            self.game = GameLogic(self.playerOne, self.playerTwo)

    def stopGame(self):
        if self.gameIsRunning:
            for i, btn in enumerate(self.buttons):
                btn.disconnect()
            self.gameIsRunning = False
            self.game = None

    def paintEvent(self, a0: QPaintEvent):
        painter = QPainter(self)
        painter.begin(self)
        self.drawGrid(painter)
        self.drawGame(painter)
        painter.end()

    def drawGrid(self, painter):
        painter.setPen(Qt.black)
        x = self.drawArea.x()
        y = self.drawArea.y()
        height = self.drawArea.height()
        width = self.drawArea.width()
        for i in range(8):
            coordx0 = self.getCoord(0, i-1)
            coordx1 = self.getCoord(7, i-1)
            coordy0 = self.getCoord(i, 0-1)
            coordy1 = self.getCoord(i, 7-1)
            painter.drawLine(coordx0, coordx1)
            painter.drawLine(coordy0, coordy1)

    def drawGame(self, painter):
        if not self.game == None:
            grid = self.game.getGrid()
            self.saveGrid = grid
        elif not self.saveGrid == None:
            grid = self.saveGrid
        for i in range(7):
            for j in range(7):
                if grid[i][j] == 1:
                    painter.setPen(self.playerOneColor)
                    painter.setBrush(self.playerOneColor)
                    painter.drawEllipse(self.getCenter(i, j), self.getCellWidth()*0.4, self.getCellHeight()*0.4)
                elif grid[i][j] == 2:
                    painter.setPen(self.playerTwoColor)
                    painter.setBrush(self.playerTwoColor)
                    painter.drawEllipse(self.getCenter(i, j), self.getCellWidth()*0.4, self.getCellHeight()*0.4)

    def getCoord(self, i, j):
        x = self.drawArea.x() + i*self.getCellWidth()
        y = self.drawArea.y() + (6-j)*self.getCellHeight()
        return QPointF(x, y)

    def getCenter(self, i, j):
        coord = self.getCoord(i, j)
        coord.setX(coord.x() + self.getCellWidth()/2)
        coord.setY(coord.y() + self.getCellHeight()/2)
        return coord

    def getCellWidth(self):
        return self.drawArea.width()/7

    def getCellHeight(self):
        return self.drawArea.height()/7

    def sendMove(self, move):
        if self.game.move(move, self.currentPlayer):
            if self.currentPlayer == self.playerOne:
                self.currentPlayer = self.playerTwo
            else:
                self.currentPlayer = self.playerOne
            self.drawArea.update()
            if self.game.didFindWinner():
                print("Winner found: " + str(self.game.whoWon()))
                self.saveGrid = self.game.getGrid()
                self.stopGame()

    def button0pressed(self):
        print("Button 0 pressed")
        self.sendMove(0)

    def button1pressed(self):
        self.sendMove(1)

    def button2pressed(self):
        self.sendMove(2)

    def button3pressed(self):
        self.sendMove(3)

    def button4pressed(self):
        self.sendMove(4)

    def button5pressed(self):
        self.sendMove(5)

    def button6pressed(self):
        self.sendMove(6)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setCentralWidget(GameWidget())
        self.show()


app = QApplication([])
test = MainWindow()
app.exec_()
