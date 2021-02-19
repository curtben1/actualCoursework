import random
import socket
import pickle
import time
"""
main logic for a poker game, used by the game host

objectives:
    calculate odds of winning
    remember chips
    online use
    spectator mode
    ui
    
    ai
    
Key:
    Diamond 0
    Heart   1
    spade   2
    club    3
    
    ace     1
    jack    11
    queen   12
    king    13
    
    
array/library formats:
    playerChips      = {player:chips
                      player:chips}
    
    players          = {player:card1,card2,chips ,folded,contributed,Won objectives
                      player:card1,card2,chips ,folded,contributed,Won objectives}    
    
    winner           = [player, contributed, beaten        // sorted by beaten
                      player, contributed, beaten]      
todo:
    add some easier network integration by laying a decent foundation

    do a bunch more testing
"""

# ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  == 

def shuffle():
    cards = [[2,0],
             [3,0],
             [4,0],
             [5,0],
             [6,0],
             [7,0],
             [8,0],
             [9,0],
             [10,0],
             [11,0],
             [12,0],
             [13,0],
             [14,0],        #aces are high now as it leads to fewer exceptions, only place where ace needs to be low is a low straight 
             
             [2,1],
             [3,1],
             [4,1],
             [5,1],
             [6,1],
             [7,1],
             [8,1],
             [9,1],
             [10,1],
             [11,1],
             [12,1],
             [13,1],
             [14,1],
             
             [2,2],
             [3,2],
             [4,2],
             [5,2],
             [6,2],
             [7,2],
             [8,2],
             [9,2],
             [10,2],
             [11,2],
             [12,2],
             [13,2],
             [14,2],
             
             [2,3],
             [3,3],
             [4,3],
             [5,3],
             [6,3],
             [7,3],
             [8,3],
             [9,3],
             [10,3],
             [11,3],
             [12,3],
             [13,3],
             [14,3],
    ]
    random.shuffle(cards)
    return cards

class Table:                                    # class created to run and store logic about the current game and everyone at the "table" 
    
              #some globalish variables I can then more easily inherit without passing to init and creating a bigger mess down the line

    def __init__(self, connected, gameSocket):
        Table.totalPlayers = len(connected)
        self.totalPlayers = 0
        self.playerChips = []
        self.hands = 0
        self.gameSocket = gameSocket
        for i in range(0,Table.totalPlayers):
            self.playerChips.append(500)
        self.blind = 50
        self.playerObjs = []
        for i in range(len(connected)):
            temp = Player()
            temp.socket = connected[i]["socket"]
            self.playerObjs.append(temp)


    def playHand(self):
        print(self.playerChips)
        self.hands = self.hands+1
        
        self.newhand = Hand(self.blind,self.playerObjs, self.gameSocket,self.playerChips,self.totalPlayers)
        self.blind = self.blind+100
        self.newhand.deal()
        self.newhand.bettingRound()
        if self.newhand.remaining > 1:
            print(self.newhand.flop())
            self.newhand.bettingRound()
            if self.newhand.remaining > 1:
                print(self.newhand.turn())
                self.newhand.bettingRound()
                if self.newhand.remaining > 1:
                    print(self.newhand.river())
                    self.newhand.bettingRound()
        winners = self.newhand.findWinner()
        self.newhand.allocateChips(winners)
        handRes = self.newhand.players
        for i in range(0, len(handRes)):
            self.playerChips[i] = handRes[i].chips
        print(self.playerChips)
# ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  ==  == 

class Hand:                              # class created for each hand of the game, calculates winners and makes changes to chips, child of Table()

    def __init__(self,sBlind,playerObjs, gameSocket,playerChips,totalPlayers):    # shuffles the deck, initialises the player library and deals the cards
        self.playerChips = playerChips
        self.totalPlayers = totalPlayers
        self.sBlind = sBlind
        self.bBlind = sBlind*2
        self.deck = shuffle()                     
        self.players = playerObjs
        self.centre = []
        self.round = 0
        self.gameSocket = gameSocket
        
        print(self.totalPlayers)
        for player in self.players:
            player.reset()

    def deal(self):                             # no return
             
        for player in self.players:
            player.card1 = (self.deck.pop(len(self.deck)-1))   
        
        for player in self.players:
            player.card2 = (self.deck.pop(len(self.deck)-1)) 
        
        """for ii in range(0, len(self.players)):
            self.sendText(ii,['2',[self.players[ii].card1,self.players[ii].card2],self.bBlind+self.sBlind,[self.players[ii].chips,ii]])"""
        
        for e in range(0,5):
            self.centre.append(self.deck.pop(len(self.deck)-1))
            
        for y in range(0,len(self.players)):
            self.players[y].chips = self.playerChips[y]        # might need to use super and make this a child
            self.players[y].stillIn = True
            self.players[y].contributed = 0

        for ii in range(0, len(self.players)):
            self.sendText(ii,['2',[self.players[ii].card1,self.players[ii].card2],self.bBlind+self.sBlind,[self.players[ii].chips,ii]])

        for hand in self.players:
            print(hand.card1, hand.card2)
        print(self.centre)

    def sendText(self,i, message):                # no return, sends message to the ip listed on port 8080
        message = pickle.dumps(message)
        self.players[i].socket.send(message)

    def getPotSize(self):
        potsize = 0
        for player in self.players:
            potsize += player.contributed
        print(potsize)
        return potsize
    
    def recvText(self, i, message,tag = 1):            #returns the response to the question ask
        if isinstance(message,str):
            message = str(tag)+'#'+message
            message = pickle.dumps(message)
            self.players[i].socket.send(message)
            print("sent")
            data = self.players[i].socket.recv(1024)
            data = pickle.loads(data)
            print("recieved")
        else:
            message1 = pickle.dumps(message)
            self.players[i].socket.send(message1)
            print("sent", message)
            data = self.players[i].socket.recv(1024)
            data = pickle.loads(data)
            print("recieved")
        return data

    def playerPrinter(self):
        for player in self.players:
            print(player.card1,player.card2,player.chips,player.contributed,player.socket,player.wonObjectives,player.stillIn)

    def sendToAll(self, message):
        message = pickle.dumps(message)
        for player in self.players:
            player.socket.send(message)

    def createDict(self):
        tempDict = []
        for i in range(0,len(self.players)):
            player = self.players[i]
            tempDict.append({"chips": player.chips-player.contributed,"stillIn":player.stillIn,"contributed":player.contributed, "action": player.action})
            print(tempDict)
        return tempDict

    def bettingRound(self):                     # no return, acts on self variable only
        # make this ready for network use by abstracting some of the get input fuctionality 
        currentBet = 0
        again = True
        raiser = len(self.players)
        counter = 0
        raised = 0
        blinds = False
        self.round = self.round +1
        while again  == True:
            again = False
            self.remaining = 0
            i = 0
            for j in range(0,len(self.players)):
                if self.players[j].stillIn == True:
                    self.remaining += 1
            if self.round == 1 and blinds == False:           #code that facillitates small and big blind
                self.players[i].contributed = self.sBlind
                i += 1
                self.players[i].contributed = self.bBlind
                self.playerPrinter()
                currentBet = self.bBlind
                raiser = i+1
                raised = counter
                again = True
                i+= 1
                blinds = True

            while i < len(self.players) and ((i<raiser and counter == raised+1) or raised  == counter) and self.remaining>1:
                for iii in range(len(self.players)):
                    time.sleep(0.1)
                    self.recvText(iii,str(self.bBlind))
                    self.recvText(iii,self.createDict())   # recvText() is better for synchronisation reasons, without client hasnt fully processed this therefor blocking next message
                    
                print("progressed")
                if blinds == True and i == 0:
                    currentBet = currentBet-self.sBlind 
                elif blinds == True and i == 1:
                    currentBet = currentBet-self.sBlind
                if self.players[i].stillIn == True and self.players[i].chips>0:
                    print(i)
                    if currentBet != 0:
                        output = "Do you want to \nCall(C)\nRaise(R)\nFold(F)\n " + '#' + str(currentBet)
                        action = self.recvText(i, output)                        # ask for over network and take answer                                                       
                    else:
                        output = "Do you want to \nCheck(C)\nRaise(R)\nFold(F)\n " + '#' + str(currentBet)
                        action = self.recvText(i, output)                     # ask for over network and take answer
                    if action  == 'C':
                        if currentBet > self.players[i].chips-self.players[i].contributed:
                            output = "you can't afford to call so have been put all in"
                            self.sendText(i, output)                                                # send over network
                            bet = self.players[i].chips-self.players[i].contributed
                        else:
                            bet = currentBet
                    elif action  == 'R':
                        again = True
                        raiser = i
                        raised = counter
                        if currentBet > self.players[i].chips-self.players[i].contributed:
                            output = "you can't afford to call so have been put all in"
                            self.sendText(i, output)                                                # send over network
                        else:
                            output = "How much do you want to raise it by? "
                            amount = int(self.recvText(i, output,'6'))                                    # send over network and take answer
                            bet = currentBet+ amount
                            while bet > self.players[i].chips-self.players[i].contributed or amount<self.bBlind:
                                if bet> self.players[i].chips-self.players[i].contributed:
                                    output = "You can't afford the bet"
                                    self.sendText(i, output)                                        # send over network
                                else:
                                    output = "that is below the minimum raise of the big blind"
                                    self.sendText(i, output)                                        # send over network
                                output = "How much do you want to raise it by? "
                                amount = int(self.recvText(i, output),'6')                                              # send and recieve over the network
                                bet = currentBet+amount
                            currentBet = bet
                    elif action  == 'F':
                        bet = 0
                        self.players[i].stillIn = False
                    self.players[i].action = action
                    self.players[i].contributed = self.players[i].contributed + bet        #alters ther individual players contribution
                i += 1
                self.remaining = 0
                for j in range(0,len(self.players)):
                    if self.players[j].stillIn == True and self.players[j].chips > 0:
                        self.remaining += 1
            counter = counter+1

    def flop(self):                             # returns [[card1],[card2],[card3]]
        flopCards = [self.centre[0],self.centre[1],self.centre[2]]
        retval = ['3']
        retval.extend([flopCards])
        self.sendToAll(retval)
        return flopCards

    def turn(self):                             # returns [card4] 
        turnCard = self.centre[3]
        retval = ['4']
        retval.extend([turnCard])
        self.sendToAll(retval)
        return turnCard

    def river(self):                            # returns [card5]
        riverCard = self.centre[4]
        retval = ['5']
        retval.extend([riverCard])
        self.sendToAll(retval)
        return riverCard

    def allocateChips(self,winners):            # no return, change players chips
        for i in range(0,len(winners)):
            total = winners[i][1]
            self.players[winners[i][0]].chips-= self.players[winners[i][0]].contributed
            for j in range(0,len(winners)):
                if i == j:
                    pass
                elif winners[i][1]>= winners[j][1]:
                    total = total+winners[j][1]
                    winners[j][1] = 0
                else:
                    total = total+winners[i][1]
                    winners[j][1] = winners[j][1]-winners[i][1]
            winners[i][1] = 0
            self.players[winners[i][0]].chips+= total
        print("after allocation: ")
        for player in self.players:
            player.contributed = 0
        self.playerPrinter()
        self.endGame()

    def endGame(self):
        myDict = self.createDict()
        myDict = ["ended",myDict]
        for iii in range(len(self.players)):
            time.sleep(0.1)
            again = self.recvText(iii,myDict)
            if again == False:
                del self.players[iii]
    
    def findWinner(self):                       # returns either the index of a single winner or a list of indexs of tied winners
        print("finding winner")
        winner = None
        for i in range(0,len(self.players)):
            print("checking P",i)
            print(self.players[i].stillIn)
            if self.players[i].stillIn == True:
                cards = [self.players[i].card1,self.players[i].card2,self.centre[0],self.centre[1],self.centre[2],self.centre[3],self.centre[4]]
                cards.sort()

                straightFlush = self.checkStraightFlush(cards)
                if straightFlush  == False:
                    print("no str flush")
                    quad = self.checkQuad(cards)
                    if quad  == False:
                        print("no quads")
                        fullHouse = self.checkFull(cards)
                        if fullHouse == False:
                            print("no fullhouse")
                            flush = self.checkFlush(cards)
                            if flush  == False:
                                print("no flush")
                                straight = self.checkStraight(cards)
                                if straight == False:
                                    print("no straight")
                                    triple = self.checkSet(cards)
                                    if triple == False:
                                        print("no triple")
                                        twoPair = self.check2Pair(cards)
                                        if twoPair == False:
                                            print("no 2pair")
                                            pair = self.checkPair(cards)
                                            if pair == False:
                                                print("no pair")
                                                high = self.getHighest(cards)
                                                self.players[i].wonObjectives=[0,high]
                                                print("high card")
                                            else:
                                                self.players[i].wonObjectives=[1,pair]
                                                print("pair")
                                        else:
                                            self.players[i].wonObjectives=[2,twoPair]
                                            print("twopair")
                                    else:
                                        self.players[i].wonObjectives=[3,triple]
                                        print("set")
                                else:
                                    self.players[i].wonObjectives=[4,straight]
                                    print("straight")
                            else:
                                self.players[i].wonObjectives=[5,flush]
                                print("flush")
                        else:
                            self.players[i].wonObjectives=[6, fullHouse]
                            print("full house")
                    else:
                        self.players[i].wonObjectives=[7,quad]
                        print("4 of kind")
                else:
                    self.players[i].wonObjectives=[8,straightFlush]
                    print("sf")

        for player in self.players:
            print(player.wonObjectives)
        winner = []
        for j in range(0,len(self.players)):
            beaten = 0
            if self.players[j].stillIn == False:
                beaten = -1   #ensures that folded players never get any money back, maybe unnecesary but shouldnt hurt
            else:
                for y in range(0,len(self.players)):
                    if y  == j:
                        pass
                    elif self.players[y].stillIn == False:
                        pass
                    elif self.players[j].wonObjectives[0] > self.players[y].wonObjectives[0]:
                        beaten = beaten + 1
                        print(beaten)
                    elif self.players[j].wonObjectives[0] == self.players[y].wonObjectives[0]:        #edgecases start here, good luck
                        print("no clear winner, calculating tie conditions")
                        same = True 
                        draw = False
                        counter = 1
                        while (same  == True and  draw  == False) and (counter<len(self.players[y].wonObjectives) and counter< len(self.players[j].wonObjectives)):
                            if self.players[j].wonObjectives[counter]>self.players[y].wonObjectives[counter]:
                                beaten += 1
                                same = False
                            counter += 1
            winner.append([j,self.players[j].contributed,beaten])        #an array of how many people they have beaten and how much they contriputed which will be used when calculating split and normal pots
        winner = sorted(winner, key = lambda row: row[2],reverse = True)
        print(winner)
        return winner

    def checkFlush(self,cards):                 # returns [card1, card2, crad3, card4, card5]
        flush = False
        for i in range (0,4):
            suit = self.sortBySuit(cards,i)       #returns a 5 card array of the same suit
            if len(suit)>= 5:
                flush = True
                suit.sort(reverse = True)
                while len(suit)> 5:
                    del suit[len(suit)-1]
                flushCards = suit
        if flush  == True:
            return flushCards
        else:
            return False
        
    def checkStraight(self,cards):              # returns highest card in the run or false
        cards.sort(reverse = True)
        if cards[0][0] == 14 and cards [len(cards)-1][0] == 2 and cards [len(cards)-2][0] == 3 and cards [len(cards)-3][0] == 4 and cards [len(cards)-4][0] == 5:
            return cards[len(cards)-4]
        else:
            gap = 0
            i = 0
            while i <len(cards)-4 and gap != 1:
                gap = int(cards[i][0]) - int(cards[i+1][0])    
                i = i+1
            if gap  == 1:
                straight = 2                          # you have now found 2 cards in a row despite only doing 1 explict check so this is correct 
                highCard = cards[i-1]
                while gap == 1 and i < len(cards)-1:
                    gap = int(cards[i][0]) - int(cards[i+1][0])
                    straight = straight+1
                    if straight >= 5:
                        return highCard             # 5 most relevant cards are the straight so no extra info is needed
                    i = i+1                                           
                else:                               # a while else loop because legacy version used break to escape while loop rather than appropriate condition                                                                                fuck you thats why
                    return False
            else:
                return False
        
    def checkStraightFlush(self, cards):        # returns the highest card in the run or false
        flush = self.checkFlush(cards)
        if flush != False:
            straight = self.checkStraight(flush)
            if straight != False and flush != False:
                return straight                     # straight only returns the highest card and the suit of the cards is now irrelevant
            else:
                return False
        else:
            return False
        
    def checkPair(self,cards):                  # returns [the paired card, highest, 2nd hghest, 3rd highest] or false
        cards.sort()
        pair = False
        for i in range(0,len(cards)-1):
            if cards [i][0] == cards [i+1][0]:
                pair = True
                others = []
                for j in range(0,len(cards)-1):
                    if j != i and j!= i+1:
                        others.append(cards[j])
                others.sort(reverse = True)
                if len(cards) == 4:
                    return  [cards[i],others[0]]
                else:
                    return [cards[i],others[0],others[1],others[2]]
        if pair == False:
            return False
        
    def check2Pair(self,cards):                 # returns [pair1,pair2,highest other card] or false
        cards.sort()
        i = 0
        pair = False
        twopair = False
        while i <len(cards)-1 and pair  == False:
            if cards [i][0] == cards [i+1][0]:
                pair = True
                pair1 = i
                break
            i += 1
        if pair  == True:
            i+= 2
            while i <len(cards)-1:
                if cards [i][0] == cards [i+1][0]:
                    twopair = True
                    pair2 = i
                    break
                i += 1
            if twopair  == True:
                others = []
                values = [cards[pair1],cards[pair2]]
                for j in range(0,len(cards)):
                    if j != pair1 and j!= pair1+1 and j!= pair2 and j!= pair2+1:
                        others.append(cards[j])
                others.sort(reverse = True)
                values = [cards[pair1],cards[pair2],others[0]]            
                return values
            else:
                return False
        else:
            return False
       
    def checkSet(self,cards):                   # returns [set card, next highest, next highest] or false
        cards.sort()
        three = False
        for i in range(0,len(cards)-2):
            if cards [i][0] == cards [i+1][0] and cards [i][0] == cards [i+2][0]:
                three = True
                others = []
                for j in range(0,len(cards)-1):
                    if j != i and j!= i+1 and j!= i+2:
                        others.append(cards[j])
                others.sort(reverse = True)
                retValues = [cards[i],others[0],others[1]]
                return retValues
        if three  == False:
            return three
            
    def checkQuad(self,cards):                  # returns : [quad card, low other, high other]
        cards.sort()
        quads = False
        for i in range(0,len(cards)-3):
            if cards [i][0] == cards [i+1][0] and cards [i][0] == cards [i+2][0] and cards [i][0] == cards [i+3][0]:
                quads = True
                others = []
                for j in range(0,len(cards)-1):
                    if j != i and j!= i+1 and j!= i+2 and j!= i+3:
                        others.append(cards[j])
                others.sort(reverse = True)
                return [cards[i],others[0]]
        if quads == False:
            return False
                
    def checkFull(self,cards):                  # returns either false or a 2 card array = [3s,2s]
        trip = self.checkSet(cards)
        if trip != False:
            newCards = []
            for i in range(0,len(cards)):
                if cards[i][0]!= trip[0][0]:
                    newCards.append(cards[i])
            pair = self.checkPair(newCards)
            if pair != False:
                trip = trip[0]
                pair = pair[0]
                if trip != pair:
                    House = [trip,pair]
                    return House
                else:
                    return False
            else:
                return False
        else:
            return False
            
    def getHighest(self,cards):                 # returns the highest card in a given array
        cards.sort(reverse = True)
        return cards[0:6]
            
    def sortBySuit(self,cards,suit):            # returns an array of all cards in the given array of the same suit as the parameter
        newArray = []
        for i in range(0,len(cards)):
            if cards[i][1] == suit:
                newArray.append(cards[i])
        return newArray

class Player:
    def __init__(self):
        self.stillIn = True
        self.contributed = 0
        self.wonObjectives = list
        self.chips = 0
        self.socket = None
        self.action = ""

    def setCards(self,card1,card2):
        self.card1 = card1
        self.card2 = card2

    def reset(self):
        self.stillIn = True
        self.contributed = 0
        self.wonObjectives = None
        self.chips = 0
