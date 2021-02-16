import math
import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import socket
import pickle
from sys import getsizeof

# note: can use window properties to pass variables betwwen


class Window(QWidget):
    out = pyqtSignal()

    def __init__(self, parent=None):
        self.netInfo = 0
        QWidget.__init__(self, parent)
        self.setGeometry(100, 100, 1280, 720)
        self.chips = 0
        self.players = None
        self.username = "laptop"  # get from accounts system
        self.potSize = 0
        
        

        # Put the widgets here
        self.opponentBox = QGroupBox()
        self.startButton = QPushButton(self.tr("&Start"))
        self.statsButton = QPushButton("statisitics")
        self.optionsButton = QPushButton("settings")
        self.quitButton = QPushButton("Quit Game")

        self.printerLabel = QLabel("placeholder")
        self.outputLabel = QLabel("placeholder")
        self.selectionCRdo = QRadioButton("Call/check")
        self.selectionRRdo = QRadioButton("Raise")
        self.selectionFRdo = QRadioButton("Fold")
        self.buttonConfirm = QPushButton("Enter")
        self.flop1 = QLabel("card1")
        self.flop2 = QLabel("card2")
        self.flop3 = QLabel("card3")
        self.flop4 = QLabel("card4")
        self.flop5 = QLabel("card5")
        self.hand1 = QLabel("hand1")
        self.hand2 = QLabel("hand2")
        self.potLabel = QLabel("0")
        self.chipLabel = QLabel('0')

        self.raiseGroup = QGroupBox()
        self.raiseTxt = QSpinBox()
        self.raiseTxt.setValue(0)
        self.raiseSlider = QSlider(Qt.Horizontal)
        self.raiseTxt.setMaximum(self.chips)
        self.raiseSlider.setRange(0, self.chips)
        self.raiseTxt.setSingleStep(1)
        self.raiseSlider.setSingleStep(1)
        self.raiseConfirm = QPushButton("Enter")
        self.raiseLabel = QLabel("How much do you want to raise the bet by")
        self.back = QPixmap("assetts/gray_ba0k.png")
        self.back3 = QPixmap("assetts/folded.png")

        self.back = self.back.scaledToWidth(96)
        self.back2 = self.back.scaledToWidth(48)
        self.back3 = self.back3.scaledToWidth(48)
        self.resetCards()

        self.raiseLayout = QVBoxLayout()
        self.subRaiseLayout = QHBoxLayout()
        self.subRaiseLayout.addWidget(self.raiseTxt)
        self.subRaiseLayout.addWidget(self.raiseConfirm)
        self.raiseLayout.addWidget(self.raiseLabel)
        self.raiseLayout.addWidget(self.raiseSlider)
        self.raiseLayout.addLayout(self.subRaiseLayout)
        self.raiseGroup.setLayout(self.raiseLayout)
        self.raiseRow = QHBoxLayout()
        self.raiseRow.addStretch(1)
        self.raiseRow.addWidget(self.raiseGroup)
        self.raiseRow.addStretch(1)
        self.raiseGroup.hide()

        centerLayout = QHBoxLayout()
        centerRow = QHBoxLayout()
        centerLayout.addWidget(self.flop1)
        centerLayout.addWidget(self.flop2)
        centerLayout.addWidget(self.flop3)
        centerLayout.addWidget(self.flop4)
        centerLayout.addWidget(self.flop5)

        self.centerGroup = QGroupBox()
        self.centerGroup.setLayout(centerLayout)
        centerRow.addStretch(1)
        centerRow.addWidget(self.centerGroup)
        centerRow.addWidget(self.potLabel)
        centerRow.addStretch(1)

        handLayout = QHBoxLayout()
        handrow = QHBoxLayout()
        handLayout.addWidget(self.hand1)
        handLayout.addWidget(self.hand2)

        self.handGroup = QGroupBox()
        self.handGroup.setLayout(handLayout)
        handrow.addStretch(3)
        handrow.addWidget(self.handGroup)
        handrow.addWidget(self.chipLabel)
        handrow.addStretch(3)

        self.radioGroup = QButtonGroup()
        self.radioGroup.addButton(self.selectionCRdo)
        self.radioGroup.addButton(self.selectionRRdo)
        self.radioGroup.addButton(self.selectionFRdo)
        self.radioGroup.addButton(self.buttonConfirm)

        self.thread = Worker(self)

        self.thread.finished.connect(self.threadDied)
        self.startButton.clicked.connect(self.startListener)

        self.thread.printTime.connect(self.printer)
        self.thread.drawOps.connect(self.drawOpponents)
        self.thread.inputTake.connect(self.takeInput)
        self.raiseConfirm.clicked.connect(self.returnRaiseValue)
        self.raiseTxt.editingFinished.connect(self.updateRaiseSlider)
        self.raiseSlider.sliderReleased.connect(self.updateRaiseTxt)
        self.quitButton.clicked.connect(self.exitGame)

        self.gamelayout = QVBoxLayout()
        self.windowLayout = QVBoxLayout()
        self.menuLayout = QVBoxLayout()

        self.menuLayout.addWidget(self.startButton)
        self.menuLayout.addWidget(self.optionsButton)
        self.menuLayout.addWidget(self.quitButton)

        self.gamelayout.addWidget(self.printerLabel)
        self.gamelayout.addWidget(self.opponentBox)
        self.gamelayout.addStretch(1)
        self.gamelayout.addLayout(centerRow)
        self.gamelayout.addStretch(1)
        self.gamelayout.addLayout(handrow)
        self.gamelayout.addLayout(self.raiseRow)
        self.gamelayout.addWidget(self.selectionCRdo)
        self.gamelayout.addWidget(self.selectionRRdo)
        self.gamelayout.addWidget(self.selectionFRdo)
        self.gamelayout.addWidget(self.buttonConfirm)

        self.menuFrame = QFrame()
        self.menuFrame.setLayout(self.menuLayout)
        self.windowLayout.addWidget(self.menuFrame)

        self.gameFrame = QFrame()
        self.gameFrame.setLayout(self.gamelayout)
        self.windowLayout.addWidget(self.gameFrame)
        self.gameFrame.hide()

        # layout.addLayout(self.inputLayout)
        self.selectionCRdo.hide()
        self.selectionRRdo.hide()
        self.selectionFRdo.hide()
        self.buttonConfirm.hide()

        self.setLayout(self.windowLayout)
        self.setWindowTitle(self.tr("Poker Game"))

    def exitGame(self):
        sys.exit()

    def startListener(self):
        # show all of the stuff
        self.createStats()
        self.gameFrame.show()
        self.thread.listen()

    def createStats(self):
        self.stats = {
            "chipsInvested":0,  # amount of chips invested in any round including blinds
            "chipsWon":0,       # amount of chips won
            "roundsInvested":0, # number of rounds (betting rounds) where a voluntary investment is made
            "handsWon":0,       # number of hands won
            "preFlopVol":0,     # pre flop rounds where any voluntary investment is made (calls raises bets) preflop
            "preFlopRaise":0,   # number of rounds with pre flop raise
            "preFlopAmount":[], # how much is invested pre flop (relative to big blind)    
            "raises":0,         # number of raises/bets, used to calculate af and agg(raises/calls)
            "calls":0,          # number of calls(not checks), used to calculate af and agg(raises/calls)
            "checks":0,         # number of checks
            "folds":0,          # number of rounds folded
            "rounds":0,         # number of rounds, used almost exclusively in calculation
            "raisedRel":[],     # raised relative to big blind
            "handsPlayed":0,    # number of hands played
            "invWhenFolded":[], # amount invested (excluding blinds) when folded"      
            "balance":0         # total balnce (overwritten at end of game)
            }

    def resetCards(self):
        self.flop1.setPixmap(self.back)
        self.flop2.setPixmap(self.back)
        self.flop3.setPixmap(self.back)
        self.flop4.setPixmap(self.back)
        self.flop5.setPixmap(self.back)
        self.hand1.setPixmap(self.back)
        self.hand2.setPixmap(self.back)
        self.potLabel.setText('0')
        self.potSize = 0

    def drawOpponents(self):
        layouts = []
        for i in range(len(self.players)):
            tempCardLayout = QHBoxLayout()
            tempBoxLayout = QVBoxLayout()
            layouts.append({"cardLayout": tempCardLayout,
                            "boxLayout": tempBoxLayout})
        self.oppenentLayout = QHBoxLayout()
        j = 0
        for player in self.players:
            if player["username"] != self.username:
                tempGrp = QGroupBox(player["username"])
                tempLbl = QLabel("chips: 0")
                tempActn = QLabel("Yet to Act")
                tempCard1 = QLabel()
                tempCard2 = QLabel()
                tempCard1.setPixmap(self.back2)
                tempCard2.setPixmap(self.back2)

                player["widgets"] = {"group": tempGrp, "card1": tempCard1,
                                     "card2": tempCard2, "chips": 0, "chipLabel": tempLbl, "action": tempActn}
                layouts[j]["boxLayout"].addWidget(tempActn)
                layouts[j]["cardLayout"].addWidget(tempCard1)
                layouts[j]["cardLayout"].addWidget(tempCard2)
                layouts[j]["boxLayout"].addLayout(layouts[j]["cardLayout"])
                layouts[j]["boxLayout"].addWidget(tempLbl)
                tempGrp.setLayout(layouts[j]["boxLayout"])
                self.oppenentLayout.addWidget(tempGrp)
            else:
                self.myPos = j

            j += 1
        self.opponentBox.setLayout(self.oppenentLayout)
        print(self.players)

    def updateRaiseSlider(self):
        self.raiseSlider.setValue(int(self.raiseTxt.value()))

    def updateRaiseTxt(self):
        self.raiseTxt.setValue(int(self.raiseSlider.value()))

    def returnRaiseValue(self):
        retVal = pickle.dumps(self.raiseTxt.value())
        self.raiseGroup.hide()
        self.stats["raises"] += 1
        self.stats["raisedRel"].append(int(retval)/self.thread.blind)
        if self.gameStage == '2':
            self.stats["preFlopVol"] +=1   # if you call raise or raise re raise this will count twice, add variable to check if this has been incremented
            self.stats["preFlopAmount"].append(retVal)
        self.thread.gamesocket.send(retVal)

    def createPixmap(self, cardNum=None):
        if cardNum == None:
            fileName = "assetts/" + \
                str(window.printvalue[1][0]) + \
                str(window.printvalue[1][1])+".png"
        else:
            fileName = "assetts/" + \
                str(window.printvalue[1][cardNum][0]) + \
                str(window.printvalue[1][cardNum][1])+".png"
        cardPic = QPixmap(fileName)
        cardPic = cardPic.scaledToWidth(96)
        return cardPic

    def printer(self):
        print("printer")
        if isinstance(window.printvalue, list):
            if isinstance(window.printvalue[0], dict) == False:
                self.gameStage = window.printvalue[0]
                if window.printvalue[0] == '2':
                    self.resetCards()
                    
                    self.hand1.setPixmap(self.createPixmap(0))
                    self.hand2.setPixmap(self.createPixmap(1))

                    chipinfo = window.printvalue[3]
                    print(chipinfo)
                    if chipinfo[1] == 0:
                        print("small blind")
                        self.chips = int(chipinfo[0] - ((1/3)*int(window.printvalue[2])))
                        self.stats["invested"] = ((1/3)*int(window.printvalue[2]))
                    elif chipinfo[1] == 1:
                        print("big blind")
                        self.chips = int(chipinfo[0] - ((2/3)*int(window.printvalue[2])))
                        self.stats["invested"] = ((2/3)*int(window.printvalue[2]))
                    else:
                        self.chips = int(chipinfo[0])
                    self.chipLabel.setText(str(self.chips))

                elif window.printvalue[0] == '3':

                    self.flop1.setPixmap(self.createPixmap(0))
                    self.flop2.setPixmap(self.createPixmap(1))
                    self.flop3.setPixmap(self.createPixmap(2))
                elif window.printvalue[0] == '4':
                    self.flop4.setPixmap(self.createPixmap())
                elif window.printvalue[0] == '5':
                    self.flop5.setPixmap(self.createPixmap())
                

                else:
                    printval = str(window.printvalue)
                    self.printerLabel.setText(printval)
            else:
                print("dickt")
                printval = str(window.printvalue)

                self.printerLabel.setText(printval)
        else:
            printval = str(window.printvalue)
            self.printerLabel.setText(printval)

    def takeInput(self):
        print("taking input")
        window.selectionCRdo.show()
        window.selectionRRdo.show()
        window.selectionFRdo.show()
        window.buttonConfirm.show()

    def threadDied(self):
        print("thread died")
        self.gameFrame.hide()
        pass
        # ran when thread dies, use as when quit game


class Worker(QThread):
    inputTake = pyqtSignal()
    printTime = pyqtSignal()
    drawOps = pyqtSignal()

    def __init__(self, window, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        window.buttonConfirm.clicked.connect(self.getInput)
        

    def __del__(self):
        self.exiting = True
        self.wait()

    def listen(self):
        self.start()

    def getInput(self):
        if window.selectionCRdo.isChecked():
            window.chips -= self.currentBet
            if window.chips < 0:
                window.chips = 0
            window.chipLabel.setText(str(window.chips))
            val = 'C'
            if self.currentBet !=0:
                window.stats["calls"] +=1
                window.stats["chipsInvested"] += self.currentBet
                if window.gameStage == '2':     # chacks if preflop
                    window.stats["preFlopVol"] += 1
                    if len(window.stats["preFlopAmount"]) == window.stats["handsPlayed"]:
                        window.stats["preFlopAmount"][-1] += self.currentBet
                    else:
                        window.stats["preFlopAmount"].append(self.currentBet)

            else:
                window.stats["checks"] += 1
                window.stats["preFlopAmount"].append(self.currentBet)
        elif window.selectionRRdo.isChecked():
            val = 'R'
            # stats updating will be done once raise amount is known which happens later
        elif window.selectionFRdo.isChecked():
            val = 'F'
            if window.gameStage == '2':
                window.stats["preFlopAmount"].append(0)
                window.stats["invWhenFolded"].append(self.investedRound)


        val = pickle.dumps(val)
        window.selectionCRdo.hide()
        window.selectionRRdo.hide()
        window.selectionFRdo.hide()
        window.buttonConfirm.hide()
        self.gamesocket.send(val)

    def run(self):
        window.printvalue = "connecting..."

        print("rerun")
        self.printTime.emit()
        self.gamesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """for row in serverList:
            if row[0]  == serverNum:
                host = row[2]
                break"""
        port = 6060         # port forwarded this on servers router
        self.gamesocket.connect(("81.135.23.12", port))
        playerInfo = [window.username, "playerNum"]  # use actual info here
        msg = pickle.dumps(playerInfo)
        self.gamesocket.send(msg)
        while True:

            data2 = self.gamesocket.recv(1024)
            if data2:
                data2 = pickle.loads(data2)
                if isinstance(data2, list):
                    print(data2)
                    break   # here for testing
                    start = input(
                        "do you want to start the game now (YES/OTHER)")
                    if start == "YES":
                        msg = pickle.dumps(start)
                        self.gamesocket.send(msg)
                else:
                    print(data2)
                    print("game starting")
                    break
        window.players = data2
        self.drawOps.emit()
        self.gameLoop()

    def gameLoop(self):
        self.blind = 0
        while True:
            data = self.gamesocket.recv(1024)
            # http://acbl.mybigcommerce.com/52-playing-cards/ connect incoming data to labels with these cards
            data = pickle.loads(data)

            try:
                data = data.split('#')
                if data[0] == '1':
                    try:
                        pot = int(data[1])
                        pickled = pickle.dumps("None")
                        self.gamesocket.send(pickled)
                        if self.blind == 0:
                            self.blind = (2/3)*pot
                        window.potLabel.setText(str(pot))
                    except Exception as error:
                        print(error, "from 349")
                        if len(data) == 3:
                            print("length 2")
                            self.currentBet = int(data[2])
                            window.printvalue = "the current bet to call is " + \
                                str(data[2])
                            self.printTime.emit()
                            print("emitted")
                        self.inputTake.emit()
                        print("input taken")
                elif data[0] == '6':
                    self.getRaise()
                else:
                    window.printvalue = data[1]
                    self.printTime.emit()
            except Exception as erroragain:
                print(erroragain, "error again from 340")
                try:
                    if data[0] == "ended":
                        response = input("play again Y/N")
                        if response == "Y":
                            response = True
                        else:
                            response = False
                        response = pickle.dumps(response)
                        self.gamesocket.send(response)
                    pot = window.potSize
                    for i in range(len(data)):
                        player = data[i]
                        self.investedRound = player["contributed"]
                        pot += player["contributed"]
                        if i != window.myPos:
                            window.players[i]["widgets"]["chips"] = player["chips"]
                            window.players[i]["widgets"]["chipLabel"].setText(
                                "chips: " + str(player["chips"]))
                            if player["stillIn"] == False:
                                window.players[i]["widgets"]["card1"].setPixmap(
                                    window.folded)
                                window.players[i]["widgets"]["card2"].setPixmap(
                                    window.folded)
                                window.players[i]["widgets"]["action"].setText(
                                    "Folded")
                            else:
                                action = player["action"]
                                if action == 'C':
                                    window.players[i]["widgets"]["action"].setText(
                                        "Called/Checked")
                                elif action == 'R':
                                    window.players[i]["widgets"]["action"].setText(
                                        "Raised")
                        else:
                            window.chipLabel.setText(str(player["chips"]))
                    window.potLabel.setText(str(pot))
                    var = pickle.dumps("None")
                    self.gamesocket.send(var)

                except Exception as error1:
                    print(error1, "from 365")
                    window.printvalue = data
                    self.printTime.emit()
                    if data == "game over":
                        return "Game Over"

    def testPrint(self):
        print("success")

    def getRaise(self):
        window.raiseTxt.setRange(self.blind, window.chips)
        window.raiseSlider.setRange(self.blind, window.chips)
        window.raiseGroup.show()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
