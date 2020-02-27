import random
"""
main logic for a poker game

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
    playerChips     ={player:chips
                      player:chips}
    
    players         ={player:card1,card2,chips ,folded,contributed,Won objectives
                      player:card1,card2,chips ,folded,contributed,Won objectives}    
    
todo:
add a issinstance(winner, list) to check if there is multiple winners and divide up accordingly

    add a pot distributing function that takes findWinners returns and actually calculates stuff

    add split pot checking on each betting round



    make some random bs validation to keep ocr happy

"""

#================================================================================================================================================================================

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
             
             [1,3],
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
    totalPlayers=0
    playerChips={}
    def __init__(self):
        Table.totalPlayers=int(input("how many players"))
        ##self.playerChips={}
        
        for i in range(0,Table.totalPlayers):
            self.playerChips[i]=500
            
    pass

    def playHand(self):
        self.newhand=Hand()
        self.newhand.deal()
        self.newhand.bettingRound()
        print(self.newhand.flop())
        self.newhand.bettingRound()
        print(self.newhand.turn())
        self.newhand.bettingRound()
        print(self.newhand.river())
        self.newhand.bettingRound()
        print(self.newhand.findWinner())
        
#==================================================================================================================================================================================

class Hand(Table):                              # class created for each hand of the game, calculates winners and makes changes to chips, child of Table()

    def __init__(self):                         # shuffles the deck, initialises the player library and deals the cards
        self.deck=shuffle()                     
        self.players={}
        self.centre=[]
        print(Table.totalPlayers)
        for i in range(0,Table.totalPlayers):
            self.players[i]=[]
  
    def deal(self):                             # no return
            
        for i in range(0,2):
            for j in range(0,Table.totalPlayers):
                self.players[j].append(self.deck.pop(len(self.deck)-1))     ##make a dictionary of players which has cards and chips and player id same as one below so that it Player class can later inherit at the end of a hand
            j=0
            
        for e in range(0,5):
            self.centre.append(self.deck.pop(len(self.deck)-1))
            
        for y in range(0,len(self.players)):
            self.players[y].append(Table.playerChips[y])
            self.players[y].append(True)
            self.players[y].append(0)
        print(self.players,'\n', self.centre)
        
    def bettingRound(self):                     # no return, acts on self variable only
        # also add some validation and make this ready for network use by abstracting some of the get input fuctionality 
        currentBet=0
        again=True
        raiser=len(self.players)
        while again== True:
            remaining=len(self.players)
            i=0
            for j in range(0,len(self.players)-1):
                if self.players[j][3]==True:
                    remaining += 1
            while   i < len(self.players) and i<raiser and self.players[i][3]==True and remaining>1: 
                print(i)
                if currentBet != 0:
                    action=input("Do you want to \nCall(C)\nRaise(R)\nFold(F)\n ")
                else:
                    action=input("Do you want to \nCheck(C)\nRaise(R)\nFold(F)\n ")
                if action == 'C':
                    again=False
                    if currentBet > self.players[i][2]-self.players[i][4]:
                        splitPot = True # currently unused but needs doing soon before network integration
                    else:
                        bet=currentBet
                elif action == 'R':
                    again=True
                    raiser=i
                    if currentBet > self.players[i][2]-self.players[i][4]:
                        print("you can't afford to call so have been put all in")
                        splitPot = True
                    else:
                        bet=currentBet+int(input("How much do you want to raise it by? "))
                        while bet > self.players[i][2]-self.players[i][4]:
                            print("You can't afford the bet")
                            bet=currentBet+int(input("How much do you want to raise it by? "))
                        currentBet=bet
                elif action == 'F':
                    again=False
                    bet = 0
                    self.players[i][3]= False

                #if splitPot == True:
                #   pass        
                #else:
                self.players[i][4]= self.players[i][4] + bet        #alters ther individual players contribution
                i += 1
                
    def flop(self):                             # returns [[card1],[card2],[card3]]
        flopCards=[self.centre[0],self.centre[1],self.centre[2]]
        return flopCards
    
    def turn(self):                             # returns [card4] 
        turnCard=self.centre[3]
        return turnCard
    
    def river(self):                            # returns [card5]
        riverCard=self.centre[4]
        return riverCard
      
    def findWinner(self):                       # returns either the index of a single winner or a list of index of tied winners
        print("finding winner")
        winner= None
        for i in range(0,len(self.players)):
            print("checking P",i)
            print(self.players[i][3])
            if self.players[i][3]==True:
                cards=[self.players[i][0],self.players[i][1],self.centre[0],self.centre[1],self.centre[2],self.centre[3],self.centre[4]]
                cards.sort()

                straightFlush=self.checkStraightFlush(cards)
                if straightFlush == False:
                    print("no str flush")
                    quad=self.checkQuad(cards)
                    if quad ==False:
                        print("no quads")
                        fullHouse=self.checkFull(cards)
                        if fullHouse==False:
                            print("no fullhouse")
                            flush=self.checkFlush(cards)
                            if flush ==False:
                                print("no flush")
                                straight=self.checkStraight(cards)
                                if straight==False:
                                    print("no straight")
                                    triple=self.checkSet(cards)
                                    if triple==False:
                                        print("no triple")
                                        twoPair=self.check2Pair(cards)
                                        if twoPair==False:
                                            print("no 2pair")
                                            pair=self.checkPair(cards)
                                            if pair==False:
                                                print("no pair")
                                                high=self.getHighest(cards)
                                                self.players[i].append([0,high])
                                                print("high card")
                                            else:
                                                self.players[i].append([1,pair])
                                                print("pair")
                                        else:
                                            self.players[i].append([2,twoPair])
                                            print("twopair")
                                    else:
                                        self.players[i].append([3,triple])
                                        print("set")
                                else:
                                    self.players[i].append([4,straight])
                                    print("straight")
                            else:
                                self.players[i].append([5,flush])
                                print("flush")
                        else:
                            self.players[i].append([6, fullHouse])
                            print("full house")
                    else:
                        self.players[i].append([7,quad])
                        print("4 of kind")
                else:
                    self.players[i].append([8,straightFlush])
                    print("sf")
        
        tie=[-1]
        print(self.players)
        for j in range(0,len(self.players)):
            beaten=0
            for y in range(0,len(self.players)):
                if y == j:
                    pass
                elif self.players[j][5][0] > self.players[y][5][0]:
                    beaten = beaten + 1
                    print(beaten)
                    if beaten == len(self.players)-1:
                        winner=j
                        print("winner is", j)
                elif self.players[j][5][0]==self.players[y][5][0]:        #edgecases start here, good luck
                    print("no clear winner, calculating tie conditions")
                    same=True 
                    draw=False
                    counter=1
                    while (same ==True and  draw == False) and (counter<len(self.players[y][5]) and counter< len(self.players[j][5])):
                        if self.players[j][5][counter]>self.players[y][5][counter]:
                            beaten += 1
                            same=False
                            if beaten == len(self.players)-2:
                                winner=j
                        if counter == len(self.players[j][5][1])-1 or counter == len(self.players[j][5][1])-1:
                            draw = True
                            if tie[0]<self.players[j][5] or tie[0] ==-1:
                                tie=[self.players[j][5][0],i,j]                                     #format= tie[card ranking, 1st person tied, second person tied]
                            elif (tie[1]==y and tie[2]!=y) or (tie[2] ==y and tie[1]!=y):           
                                tie.append(j)
                            
                            #  add tied pot code noting we need more than 2 way split pots, & a tie doesnt mean a win they could be tied losers
                            #  so this fact must be stored somewhere with how many in the draw and what they drew on 
                        counter += 1
        if tie[0] ==  -1:       # and no split pot
            print("no tie")
            return winner        
        else:
            print("multiple winners, splitting pot...")
            winner=[]
            for index in range (1,len(tie)-1):
                winner.append(tie[index])
            return winner

    def checkFlush(self,cards):                 # returns [card1, card2, crad3, card4, card5]
        flush=False
        for i in range (0,4):
            suit=self.sortBySuit(cards,i)       #returns a 5 card array of the same suit
            if len(suit)>=5:
                flush=True
                suit.sort(reverse=True)
                while len(suit)> 5:
                    del suit[len(suit)-1]
                flushCards=suit
        if flush == True:
            return flushCards
        else:
            return False
        
    def checkStraight(self,cards):              # returns highest card in the run or false
        cards.sort(reverse=True)
        if cards[0][0]==14 and cards [len(cards)-1][0]==2 and cards [len(cards)-2][0]==3 and cards [len(cards)-3][0]==4 and cards [len(cards)-4][0]==5:
            return cards[len(cards)-4]
        else:
            gap=0
            i=0
            while i <len(cards)-4 and gap !=1:
                gap = int(cards[i][0]) - int(cards[i+1][0])    
                i=i+1
            if gap == 1:
                straight=2                          # you have now found 2 cards in a row despite only doing 1 explict check so this is correct 
                highCard=cards[i-1]
                while gap==1 and i < len(cards)-1:
                    gap= int(cards[i][0]) - int(cards[i+1][0])
                    straight=straight+1
                    if straight >=5:
                        return highCard             # 5 most relevant cards are the straight so no extra info is needed
                    i=i+1                                           
                else:                               # a while else loop because legacy version used break to escape while loop rather than appropriate condition                                                                                fuck you thats why
                    return False
            else:
                return False
        
    def checkStraightFlush(self, cards):        # returns the highest card in the run or false
        flush= self.checkFlush(cards)
        if flush != False:
            straight= self.checkStraight(flush)
            if straight != False and flush != False:
                return straight                     # straight only returns the highest card and the suit of the cards is now irrelevant
            else:
                return False
        else:
            return False
        
    def checkPair(self,cards):                  # returns [the paired card, highest, 2nd hghest, 3rd highest] or false
        cards.sort()
        pair=False
        for i in range(0,len(cards)-1):
            if cards [i][0]==cards [i+1][0]:
                pair=True
                others=[]
                for j in range(0,len(cards)-1):
                    if j !=i:
                        others.append(cards[j])
                others.sort(reverse=True)
                if len(cards)==4:
                    return  [cards[i],others[0]]
                else:
                    return [cards[i],others[0],others[1],others[2]]
        if pair==False:
            return False
        
    def check2Pair(self,cards):                 # returns [pair1,pair2,highest other card] or false
        cards.sort()
        i=0
        pair=False
        twopair=False
        while i <len(cards)-1 and pair ==False:
            if cards [i][0]==cards [i+1][0]:
                pair= True
                pair1=i
                break
            i += 1
        if pair == True:
            i += 2
            while i <len(cards)-1:
                if cards [i][0]==cards [i+1][0]:
                    twopair = True
                    pair2=i
                    break
                i+=1
            if twopair == True:
                others=[]
                values=[cards[pair1],cards[pair2]]
                for j in range(0,len(cards)):
                    if j != pair1 and j!=pair1+1 and j!=pair2 and j!=pair2+1:
                        others.append(cards[j])
                others.sort(reverse=True)
                values=[cards[pair1],cards[pair2],others[0]]            
                return values
        else:
            return False
       
    def checkSet(self,cards):                   # returns [set card, next highest, next highest] or false
        cards.sort()
        three=False
        for i in range(0,len(cards)-2):
            if cards [i][0]==cards [i+1][0] and cards [i][0]==cards [i+2][0]:
                three=True
                others=[]
                for j in range(0,len(cards)-1):
                    if j !=i:
                        others.append(cards[j])
                others.sort(reverse=True)
                retValues=[cards[i],others[0],others[1]]
                return retValues
        if three == False:
            return three
            
    def checkQuad(self,cards):                  # returns : [quad card, low other, high other]
        cards.sort()
        quads=False
        for i in range(0,len(cards)-3):
            if cards [i][0]==cards [i+1][0] and cards [i][0]==cards [i+2][0] and cards [i][0]==cards [i+3][0]:
                quads=True
                others=[]
                for j in range(0,len(cards)-1):
                    if j !=i:
                        others.append(cards[j])
                others.sort(reverse=True)
                return [cards[i],others[0]]
        if quads==False:
            return False
                
    def checkFull(self,cards):                  # returns either false or a 2 card array=[3s,2s]
        trip=self.checkSet(cards)
        if trip != False:
            newCards=[]
            for i in range(0,len(cards)):
                if cards[i][0]!=trip[0][0]:
                    newCards.append(cards[i])
            pair=self.checkPair(newCards)
            if pair != False:
                trip=trip[0]
                pair=pair[0]
                if trip !=pair:
                    House=[trip,pair]
                    return House
                else:
                    return False
            else:
                return False
        else:
            return False
            
    def getHighest(self,cards):                 # returns the highest card in a given array
        cards.sort(reverse=True)
        return cards[0]
            
    def sortBySuit(self,cards,suit):            # returns an array of all cards in the given array of the same suit as the parameter
        newArray=[]
        for i in range(0,len(cards)):
            if cards[i][1]==suit:
                newArray.append(cards[i])
        return newArray