from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
import utils as Utils
from Astar.queen_solver import QueenSolver

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.state = { "isLoading": False, "board": None }
        self.setFixedSize(720, 720)
        self.setWindowTitle("8-queen solvers")
        self.setStyleSheet("background-color: #FFFFFE;")
        self.initUI()

    def initUI(self):
        self.initBoard()
        self.initChooseFileButton()
        self.initLeftButton()
        self.initRightButton()

        # self.b1 = QtWidgets.QPushButton(self)
        # self.b1.setText("Choose file from directory")
        # self.b1.setGeometry(370, 270, 300, 80)
        # self.b1.clicked.connect(self.clicked)
    
    def initBoard(self):
        self.board = QtWidgets.QLabel(self)
        self.board.setGeometry(99, 44, 522, 522)
        self.board.setPixmap(QtGui.QPixmap("./assets/board.jpeg"))
        self.board.setScaledContents(True)
    
    def initChooseFileButton(self):
        self.button = QtWidgets.QPushButton(self)
        self.button.setGeometry(274, 603, 172, 44)
        self.button.setText("CHOOSE A FILE")
        self.button.setStyleSheet("""
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
        """)

        self.button.clicked.connect(self.chooseFileTest)

    def initLeftButton(self):
        self.leftButton = QtWidgets.QPushButton(self)
        self.leftButton.setGeometry(213, 611, 28, 28)
        self.leftButton.setIcon(QtGui.QIcon("./assets/left-arrow.png"))
        self.leftButton.setIconSize(QSize(28,28))
        self.leftButton.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: none;
                font-size: 30px;
            }

            QPushButton:pressed {
                border: 2px solid #078080;
                border-radius: 12px;
            }
        """)

    def initRightButton(self):
        self.leftButton = QtWidgets.QPushButton(self)
        self.leftButton.setGeometry(479, 611, 28, 28)
        self.leftButton.setIcon(QtGui.QIcon("./assets/right-arrow.png"))
        self.leftButton.setIconSize(QSize(28,28))
        self.leftButton.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: none;
                font-size: 30px;
            }

            QPushButton:pressed {
                border: 2px solid #078080;
                border-radius: 12px;
            }
        """)

    def chooseFileTest(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"File Explorer", "","Text files (*.txt)", options=options)
        if fileName:
            inputData = Utils.load(fileName)
            print(inputData)
            # queenSolver = QueenSolver(initial_state=inputData[0], remain=8-inputData[1])

            
        

    def chooseFile(self):
        self.updateState({"isLoading": True})
        print("OK")
        self.updateState({"isLoading": False})

    def updateState(self, stateChange):
        self.state = self.state.update(stateChange)
        self.updateUI()

    # map new event to state
    def updateUI(self):
        self.updateLeftButton()
        self.updateRightButton()
        self.updateChooseFileButton()
        self.updateBoard()

    def updateLeftButton(self):
        print("LEFT BUTTON")
    def updateRightButton(self):
        print("RIGHT BUTTON")
    def updateChooseFileButton(self):
        print("CHOOSE FILE BUTTON")
    def updateBoard(self):
        print("BOARD")


def run():
    app = QApplication(sys.argv)
    window = App()

    window.show()
    sys.exit(app.exec_())

run()