import math, random, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# note: can use window properties to pass variables betwwen 

class Window(QWidget):
    out = pyqtSignal()
    def __init__(self, parent = None):
        self.netInfo = 0
        QWidget.__init__(self, parent)        
        self.thread = Worker()

        # Put the widgets here
        self.startButton = QPushButton(self.tr("&Start"))       

        self.thread.finished.connect(self.threadDied)
        self.startButton.clicked.connect(self.startListener)
        self.thread.output.connect(self.success)
        layout = QGridLayout()
        layout.addWidget(self.startButton, 0, 2)
        self.setLayout(layout)        
        self.setWindowTitle(self.tr("Simple Threading Example"))

    def startListener(self):
        self.thread.listen()
      
    def success(self):
        print("we did it")

    def threadDied(self):
        pass
        # ran when thread dies, use as when quit game

class Worker(QThread):
    output = pyqtSignal()       # declare signals
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False
        out.connect()

    def __del__(self):    
        self.exiting = True
        self.wait()

    def listen(self):    
        self.start()        

    def run(self):      
        counter = 0  
        while True:     ##can run paralell to ui
            if counter==100:
                self.output.emit()          # can take parameters if needed and then use args = when triggering
                break
            counter += 1
            print("hey", counter)    
    
    def testPrint():
        print("success")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())