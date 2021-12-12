from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
import utils as Utils
import copy
import textwrap
from Astar.queen_solver import QueenSolver

class StateType:
    INITIAL = 1 # App has just started, no file selected
    LOADING = 2 # A file is selected, the file's content is being processed
    LOADED = 3 # The state is ready
class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.state = { "type": StateType.INITIAL }
        self.setFixedSize(720, 720)
        self.setWindowTitle("8-queen solvers")
        self.setStyleSheet("background-color: #FFFFFE;")

        self.initStyle()
        self.initUI()
        self.initBoardMapping()
        self.initQueenList()

    def initBoardMapping(self):
        self.pos = []
        for i in range(0,64):
            self.pos.append((99 + 65*(i % 8), 44 + 65*(i//8)))

    def initUI(self):
        self.initBoard()
        self.initChooseFileButton()
        self.initLeftButton()
        self.initRightButton()
    
    def initStyle(self):
        self.navigateButtonStyle = """
            QPushButton {
                background-color: white;
                border: none;
                font-size: 20px;
            }

            QPushButton:pressed {
                border: 2px solid #078080;
                border-radius: 12px;
            }
        """
        self.chooseFileButtonStyle = """
            QPushButton {
                background-color: #078080; 
                border-radius: 17px;
                color: white;
                text-align: center;
                font-family: 'Tahoma';
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: white;
                border: 2px solid #078080;
                color: #078080;
            }
        """

        self.loadingButtonStyle = """
            QPushButton {
                background-color: grey; 
                border-radius: 17px;
                color: white;
                text-align: center;
                font-family: 'Tahoma';
                font-size: 12px;
                font-weight: bold;
            }
        """
    
    def initBoard(self):
        self.board = QtWidgets.QLabel(self)
        self.board.setGeometry(99, 44, 522, 522)
        self.board.setPixmap(QtGui.QPixmap("./assets/board.jpeg"))
        self.board.setScaledContents(True)
    
    def initChooseFileButton(self):
        self.button = QtWidgets.QPushButton(self)
        self.button.setGeometry(274, 603, 172, 44)
        self.button.setText("CHOOSE A FILE")
        self.button.setStyleSheet(self.chooseFileButtonStyle)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.clicked.connect(self.chooseFile)

    def createButton(self, x, y, w, h, iconPath):
        tempButton = QtWidgets.QPushButton(self)
        tempButton.setGeometry(x, y, w, h)
        tempButton.setIcon(QtGui.QIcon(iconPath))
        tempButton.setIconSize(QSize(28,28))
        tempButton.setStyleSheet(self.navigateButtonStyle)
        tempButton.setCursor(QCursor(Qt.PointingHandCursor))
        return tempButton

    def initLeftButton(self):
        self.leftButton = self.createButton(213, 611, 28, 28, "./assets/left-arrow.png")
        self.leftButton.clicked.connect(self.decreaseStateIndex)

    def initRightButton(self):
        self.rightButton = self.createButton(479, 611, 28, 28, "./assets/right-arrow.png")
        self.rightButton.clicked.connect(self.increaseStateIndex)

    def chooseFile(self):
        rollbackState = copy.deepcopy(self.state)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"File Explorer", "","Text files (*.txt)", options=options)
        if fileName:
            self.updateState({"type": StateType.LOADING})
            inputData = Utils.load(fileName)
            queenSolver = QueenSolver(initial_state=inputData[0], remain=8-inputData[1])
            path, expanded_list, time = queenSolver.solve()
            return self.updateState({"type": StateType.LOADED, "path": path, "expanded_list": expanded_list, "time": time, "index": 0, "maxIndex":8-inputData[1] })
        return self.updateState(self.state)

    def initQueenList(self):
        self.queenList = []
        for i in range(0, 8):
            tempQueen = QtWidgets.QLabel(self)
            tempQueen.setGeometry(0, 0, 65, 65)
            tempQueen.setPixmap(QtGui.QPixmap("./assets/queen.png"))
            tempQueen.setScaledContents(True)
            tempQueen.setStyleSheet("background-color: transparent;")
            tempQueen.hide()
            self.queenList.append(tempQueen)

    def updateState(self, stateChange):
        self.state.update(stateChange)
        self.updateUI()

    # map new event to state
    def updateUI(self):
        self.updateLeftButton()
        self.updateRightButton()
        self.updateChooseFileButton()
        self.updateBoard()

    def updateLeftButton(self):
        stateType = self.state.get("type")
        if stateType == StateType.LOADING:
            self.leftButton.setEnabled(False)
        if stateType == StateType.LOADED:
            self.leftButton.setEnabled(True)
                

    def updateRightButton(self):
        stateType = self.state.get("type")
        if stateType == StateType.LOADING:
            self.rightButton.setEnabled(False)
        if stateType == StateType.LOADED:
            self.rightButton.setEnabled(True)
                
    def decreaseStateIndex(self):
        if (self.state.get("index") > 0):
            self.updateState({"index": self.state.get("index") - 1})

    def increaseStateIndex(self):
        if (self.state.get("index") < self.state.get("maxIndex")):
            self.updateState({"index": self.state.get("index") + 1})
        
    def updateChooseFileButton(self):
        stateType = self.state.get("type")
        if stateType == StateType.LOADING:
            self.button.setEnabled(False)
            self.button.setStyleSheet(self.loadingButtonStyle)
        elif stateType == StateType.LOADED:
            self.button.setEnabled(True)
            self.button.setStyleSheet(self.chooseFileButtonStyle)
            

    def updateBoard(self):
        stateType = self.state.get("type")
        if stateType == StateType.LOADED:
            self.clearQueen()
            currentBoard = self.state.get("path")[self.state.get("index")]
            queenIndexList = [i for i, ltr in enumerate(currentBoard) if ltr == "1"]
            for queenIndex in queenIndexList:
                self.spawnQueen(queenIndex)

    def clearQueen(self):
        for queen in self.queenList:
            queen.hide()
                
    def spawnQueen(self, queenIndex):
        if(queenIndex < 8):
            self.queenList[0].move(self.pos[queenIndex][0], self.pos[queenIndex][1])
            self.queenList[0].show()
        elif(queenIndex < 16):
            self.queenList[1].move(self.pos[queenIndex][0], self.pos[queenIndex][1])
            self.queenList[1].show()
        elif(queenIndex < 24):
            self.queenList[2].move(self.pos[queenIndex][0], self.pos[queenIndex][1])
            self.queenList[2].show()
        elif(queenIndex < 32):
            self.queenList[3].move(self.pos[queenIndex][0], self.pos[queenIndex][1])
            self.queenList[3].show()
        elif(queenIndex < 40):
            self.queenList[4].move(self.pos[queenIndex][0], self.pos[queenIndex][1])
            self.queenList[4].show()
        elif(queenIndex < 48):
            self.queenList[5].move(self.pos[queenIndex][0], self.pos[queenIndex][1])
            self.queenList[5].show()
        elif(queenIndex < 56):
            self.queenList[6].move(self.pos[queenIndex][0], self.pos[queenIndex][1])
            self.queenList[6].show()
        elif(queenIndex < 64):
            self.queenList[7].move(self.pos[queenIndex][0], self.pos[queenIndex][1])
            self.queenList[7].show()
        

def run():
    app = QApplication(sys.argv)
    window = App()

    window.show()
    sys.exit(app.exec_())

run()