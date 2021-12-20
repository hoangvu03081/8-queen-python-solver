from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
import utils as Utils
import copy
import textwrap
import style
from Astar.queen_solver import QueenSolver
from Astar.utils import generate_cnf_clauses

class StateType:
    INITIAL = 1 # App has just started, no file selected
    LOADING = 2 # A file is selected, the file's content is being processed
    LOADED = 3 # The algorithm has finished processing
    VISUALIZE_EXPANDED_LIST = 4 # The state which program will automatically visualize expanded list step by step
class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.state = { "type": StateType.INITIAL }
        self.setFixedSize(1039, 720)
        self.setWindowTitle("8-queen solvers")
        self.setStyleSheet("background-color: #FFFFFE;")

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
        self.initControlPanel()

    def initControlPanel(self):
        self.controlPanel = QtWidgets.QLabel(self)
        self.controlPanel.setGeometry(679, 0, 360, 720)
        self.controlPanel.setStyleSheet("background-color: #232323;")

        self.timeOuterContainer = QtWidgets.QLabel(self)
        self.timeOuterContainer.setGeometry(727, 44, 264, 42)
        self.timeOuterContainer.setStyleSheet(style.timeOuterContainerStyle)

        self.timeInnerContainer = QtWidgets.QLabel(self)
        self.timeInnerContainer.setGeometry(734, 49, 75, 31)
        self.timeInnerContainer.setStyleSheet(style.timeInnerContainerStyle)
        self.timeInnerContainer.setText("TIME")
        self.timeInnerContainer.setAlignment(Qt.AlignCenter)

        self.timeLabel = QtWidgets.QLabel(self)
        self.timeLabel.setGeometry(835, 57, 137, 16)
        self.timeLabel.setStyleSheet(style.timeLabelStyle)
        self.timeLabel.setAlignment(Qt.AlignRight)

        self.visualizePathButton = QtWidgets.QPushButton(self)
        self.visualizePathButton.setGeometry(734, 109, 249, 41)
        self.visualizePathButton.setStyleSheet(style.visualizePathButtonStyle)
        self.visualizePathButton.setText("VISUALIZE PATH")
        self.visualizePathButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.visualizePathButton.clicked.connect(self.chooseVisualPath)
        self.visualizePathButton.setEnabled(False)

        self.visualizeExpandedListButton = QtWidgets.QPushButton(self)
        self.visualizeExpandedListButton.setGeometry(768, 171, 181, 31)
        self.visualizeExpandedListButton.setStyleSheet(style.visualizeExpandedListButtonStyle)
        self.visualizeExpandedListButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.visualizeExpandedListButton.setText("VISUALIZE EXPANDED LIST")
        self.visualizeExpandedListButton.clicked.connect(self.chooseExpandedList)
        self.visualizeExpandedListButton.setEnabled(False)

        self.saveCNFButton = QtWidgets.QPushButton(self)
        self.saveCNFButton.setGeometry(734, 604, 249, 41)
        self.saveCNFButton.setStyleSheet(style.saveCNFButtonStyle)
        self.saveCNFButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.saveCNFButton.setText("SAVE CNF TO TEXT FILE")
        self.saveCNFButton.clicked.connect(self.saveCNF)
        self.saveCNFButton.setEnabled(False)

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.updateExpandedList)

    
    def initBoard(self):
        self.board = QtWidgets.QLabel(self)
        self.board.setGeometry(99, 44, 522, 522)
        self.board.setPixmap(QtGui.QPixmap("./assets/board.jpeg"))
        self.board.setScaledContents(True)
    
    def initChooseFileButton(self):
        self.button = QtWidgets.QPushButton(self)
        self.button.setGeometry(274, 603, 172, 44)
        self.button.setText("CHOOSE A FILE")
        self.button.setStyleSheet(style.chooseFileButtonStyle)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.clicked.connect(self.chooseFile)

    def createNavigateButton(self, x, y, w, h, iconPath):
        tempButton = QtWidgets.QPushButton(self)
        tempButton.setGeometry(x, y, w, h)
        tempButton.setIcon(QtGui.QIcon(iconPath))
        tempButton.setIconSize(QSize(28,28))
        tempButton.setStyleSheet(style.navigateButtonStyle)
        tempButton.setCursor(QCursor(Qt.PointingHandCursor))
        tempButton.setEnabled(False)
        return tempButton

    def initLeftButton(self):
        self.leftButton = self.createNavigateButton(213, 611, 28, 28, "./assets/left-arrow.png")
        self.leftButton.clicked.connect(self.decreaseStateIndex)

    def initRightButton(self):
        self.rightButton = self.createNavigateButton(479, 611, 28, 28, "./assets/right-arrow.png")
        self.rightButton.clicked.connect(self.increaseStateIndex)

    def chooseFile(self):
        rollbackState = copy.deepcopy(self.state)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"File Explorer", "","Text files (*.txt)", options=options)
        if fileName:
            self.updateState({"type": StateType.LOADING})
            inputData = Utils.load(fileName)
            if not isinstance(inputData, tuple):
                return self.updateState(rollbackState)
            queenSolver = QueenSolver(initial_state=inputData[0], remain=8-inputData[1])
            path, expanded_list, time = queenSolver.solve()
            return self.updateState(
                {"type": StateType.LOADED, 
                "path": path, 
                "expanded_list": expanded_list, 
                "time": int(time*1000), 
                "index": 0, 
                "maxIndex":len(path)-1 })
        return self.updateState(self.state)

    def initQueenList(self):
        self.queenList = []
        for i in range(0, 64):
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
        self.updateTimeLabel()
        self.updateVisualPathButton()
        self.updateVisualizeExpandedListButton()
        self.updateSaveCNFButton()
        self.updateTimer()

    def updateTimer(self):
        stateType = self.state.get("type")
        if stateType == StateType.VISUALIZE_EXPANDED_LIST:
            if self.state.get("index") >= len(self.state.get("expanded_list"))-1:
                self.timer.stop()
        else: 
            self.timer.stop()

    def updateVisualPathButton(self):
        stateType = self.state.get("type")
        if stateType == StateType.INITIAL or stateType == StateType.LOADING:
            self.visualizePathButton.setEnabled(False)
        else:
            self.visualizePathButton.setEnabled(True)

    def updateVisualizeExpandedListButton(self):
        stateType = self.state.get("type")
        if stateType == StateType.INITIAL or stateType == StateType.LOADING:
            self.visualizeExpandedListButton.setEnabled(False)
        else:
            self.visualizeExpandedListButton.setEnabled(True)

    def updateSaveCNFButton(self):
        stateType = self.state.get("type")
        if stateType == StateType.INITIAL or stateType == StateType.LOADING:
            self.saveCNFButton.setEnabled(False)
        else:
            self.saveCNFButton.setEnabled(True)

    def updateTimeLabel(self):
        stateType = self.state.get("type")
        if stateType == StateType.LOADING:
            self.timeLabel.setText("")
        if stateType == StateType.LOADED:
            self.timeLabel.setText("{}ms".format(str(self.state.get("time"))))

    def updateLeftButton(self):
        stateType = self.state.get("type")
        if stateType == StateType.LOADING:
            self.leftButton.setEnabled(False)
        if stateType == StateType.LOADED:
            self.leftButton.setEnabled(True)
        if stateType == StateType.VISUALIZE_EXPANDED_LIST:
            self.leftButton.setEnabled(False)
                

    def updateRightButton(self):
        stateType = self.state.get("type")
        if stateType == StateType.LOADING:
            self.rightButton.setEnabled(False)
        if stateType == StateType.LOADED:
            self.rightButton.setEnabled(True)
        if stateType == StateType.VISUALIZE_EXPANDED_LIST:
            self.rightButton.setEnabled(False)
                
    def decreaseStateIndex(self):
        if (self.state.get("index") > 0):
            self.updateState({"index": self.state.get("index") - 1})

    def increaseStateIndex(self):
        if (self.state.get("index") < self.state.get("maxIndex")):
            self.updateState({"index": self.state.get("index") + 1})
        
    def updateChooseFileButton(self):
        stateType = self.state.get("type")
        if stateType == StateType.INITIAL:
            self.button.setEnabled(True)
            self.button.setStyleSheet(style.chooseFileButtonStyle)
        if stateType == StateType.LOADING:
            self.button.setEnabled(False)
            self.button.setStyleSheet(style.loadingButtonStyle)
        elif stateType == StateType.LOADED:
            self.button.setEnabled(True)
            self.button.setStyleSheet(style.chooseFileButtonStyle)
            
    def updateBoard(self):
        stateType = self.state.get("type")

        if stateType == StateType.LOADED:
            self.clearQueen()
            currentBoard = self.state.get("path")[self.state.get("index")]
            queenIndexList = [i for i, ltr in enumerate(currentBoard) if ltr == "1"]
            for queenIndex in queenIndexList:
                self.spawnQueen(queenIndex)

        elif stateType == StateType.VISUALIZE_EXPANDED_LIST:
            self.clearQueen()
            currentBoard = self.state.get("expanded_list")[self.state.get("index")]
            queenIndexList = [i for i, ltr in enumerate(currentBoard) if ltr == "1"]
            for queenIndex in queenIndexList:
                self.spawnQueen(queenIndex)

    def clearQueen(self):
        for queen in self.queenList:
            queen.hide()
                
    def spawnQueen(self, queenIndex):
        self.queenList[queenIndex].move(self.pos[queenIndex][0], self.pos[queenIndex][1])
        self.queenList[queenIndex].show()

    def saveCNF(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save CNF","","Text files (*.txt)", options=options)
        if fileName:
            if not fileName.endswith(".txt"):
                fileName = fileName + ".txt"
            stateType = self.state.get("type")
            if stateType == StateType.LOADED:
                cnf = generate_cnf_clauses(self.state.get("path")[self.state.get("index")])
                with open(fileName, "w") as fileStream:
                    fileStream.writelines(cnf)
            elif stateType == StateType.VISUALIZE_EXPANDED_LIST:
                cnf = generate_cnf_clauses(self.state.get("path")[self.state.get("maxIndex")])
                with open(fileName, "w") as fileStream:
                    fileStream.writelines(cnf)

    def chooseVisualPath(self):
        stateType = self.state.get("type")
        if stateType == StateType.LOADED or stateType == StateType.VISUALIZE_EXPANDED_LIST:
            if self.timer.isActive():
                self.timer.stop()
            self.updateState({"type": StateType.LOADED, "index": 0})
    
    def chooseExpandedList(self):
        if self.timer.isActive():
            self.timer.stop()
        self.updateState({"type": StateType.VISUALIZE_EXPANDED_LIST, "index": 0})
        self.timer.start(500)

    def updateExpandedList(self):
        stateType = self.state.get("type")
        if stateType == StateType.VISUALIZE_EXPANDED_LIST and self.state.get("index") < len(self.state.get("expanded_list"))-1:
            self.updateState({"type": StateType.VISUALIZE_EXPANDED_LIST, "index": self.state.get("index") + 1})



def run():
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('./assets/Roboto-Bold.ttf')
    window = App()

    window.show()
    sys.exit(app.exec_())

run()