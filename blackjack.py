import array
import random
import math
import signal
import time
import sys

#global constants
DECKSIZE = 8
PENETRATION = 4
DECK_PEN_RATIO = PENETRATION/DECKSIZE

deck = []
runningCount = 0
trueCount = 0


#Basic Strategy https://www.blackjackapprenticeship.com/blackjack-strategy-charts/
#1=Hit, 2=Stand, 3=Double
#                2,3,4,5,6,7,8,9,10,A(11)
strategyHard = [[2,2,2,2,2,2,2,2,2,2],#21
                [2,2,2,2,2,2,2,2,2,2],#20
                [2,2,2,2,2,2,2,2,2,2],#19
                [2,2,2,2,2,2,2,2,2,2],#18
                [2,2,2,2,2,2,2,2,2,2],#17
                [2,2,2,2,2,1,1,1,1,1],#16
                [2,2,2,2,2,1,1,1,1,1],#15
                [2,2,2,2,2,1,1,1,1,1],#14
                [2,2,2,2,2,1,1,1,1,1],#13
                [1,1,2,2,2,1,1,1,1,1],#12
                [3,3,3,3,3,3,3,3,3,3],#11
                [3,3,3,3,3,3,3,3,1,1],#10
                [1,3,3,3,3,1,1,1,1,1],#9
                [1,1,1,1,1,1,1,1,1,1],#8
                [1,1,1,1,1,1,1,1,1,1],#7
                [1,1,1,1,1,1,1,1,1,1],#6
                [1,1,1,1,1,1,1,1,1,1],#5
                [1,1,1,1,1,1,1,1,1,1],#4
                [1,1,1,1,1,1,1,1,1,1],#3
                [1,1,1,1,1,1,1,1,1,1]]#2

                             
h21=strategyHard[0]
h20=strategyHard[1]
h19=strategyHard[2]
h18=strategyHard[3]
h17=strategyHard[4]
h16=strategyHard[5]
h15=strategyHard[6]
h14=strategyHard[7]
h13=strategyHard[8]
h12=strategyHard[9]
h11=strategyHard[10]
h10=strategyHard[11]
h9 =strategyHard[12]
h8 =strategyHard[13]
h7 =strategyHard[14]
h6 =strategyHard[15]
h5 =strategyHard[16]
h4 =strategyHard[17]
h3 =strategyHard[18]
h2 =strategyHard[19]

hardDict = {
    21:h21,
    20:h20,
    19:h19,
    18:h18,
    17:h17,
    16:h16,
    15:h15,
    14:h14,
    13:h13,
    12:h12,
    11:h11,
    10:h10,
    9:h9,
    8:h8,
    7:h7,
    6:h6,
    5:h5,
    4:h4,
    3:h3,
    2:h2
    }

#                2,3,4,5,6,7,8,9,10,A(11)
strategySoft = [[2,2,2,2,2,2,2,2,2,2],#21
                [2,2,2,2,2,2,2,2,2,2],#20
                [2,2,2,2,3,2,2,2,2,2],#19
                [3,3,3,3,3,2,2,1,1,1],#18
                [1,3,3,3,3,1,1,1,1,1],#17
                [1,1,3,3,3,1,1,1,1,1],#16
                [1,1,3,3,3,1,1,1,1,1],#15
                [1,1,1,3,3,1,1,1,1,1],#14
                [1,1,1,3,3,1,1,1,1,1],#13
                [1,1,1,1,1,1,1,1,1,1],#12
                [3,3,3,3,3,3,3,3,3,3]]#11
                
                             
s21=strategySoft[0]
s20=strategySoft[1]
s19=strategySoft[2]
s18=strategySoft[3]
s17=strategySoft[4]
s16=strategySoft[5]
s15=strategySoft[6]
s14=strategySoft[7]
s13=strategySoft[8]
s12=strategySoft[9]
s11=strategySoft[10]

softDict = {
    21:s21,
    20:s20,
    19:s19,
    18:s18,
    17:s17,
    16:s16,
    15:s15,
    14:s14,
    13:s13,
    12:s12,
    11:s11
    }

#Split strategy, 0=No, 1=Yes
#                2,3,4,5,6,7,8,9,10,A(11)
strategySplit =[[1,1,1,1,1,1,1,1,1,1],#A
                [0,0,0,0,0,0,0,0,0,0],#10
                [1,1,1,1,1,0,1,1,0,0],#9
                [1,1,1,1,1,1,1,1,1,1],#8
                [1,1,1,1,1,1,0,0,0,0],#7
                [1,1,1,1,1,0,0,0,0,0],#6
                [0,0,0,0,0,0,0,0,0,0],#5
                [0,0,0,1,1,0,0,0,0,0],#4
                [1,1,1,1,1,1,0,0,0,0],#3
                [1,1,1,1,1,1,0,0,0,0]]#2
                             
ss11=strategySplit[0]
ss10=strategySplit[1]
ss9=strategySplit[2]
ss8=strategySplit[3]
ss7=strategySplit[4]
ss6=strategySplit[5]
ss5=strategySplit[6]
ss4=strategySplit[7]
ss3=strategySplit[8]
ss2=strategySplit[9]

splitDict = {
    1:ss11,
    10:ss10,
    9:ss9,
    8:ss8,
    7:ss7,
    6:ss6,
    5:ss5,
    4:ss4,
    3:ss3,
    2:ss2
    }

#pop a number from deck, assign a value based on number drawn e.g. 1=Ace=1/11, 11=Jack=10
def deckToValue(number):
    value= number%13 + 1
    return value if value<=10 else 10

def shuffleDeck():
    global deck
    global runningCount
    global trueCount
    deck = [i for i in range(0,DECKSIZE*4*13)]
    deck = [deckToValue(i) for i in deck]
    random.shuffle(deck)
    runningCount = 0
    trueCount = 0

#evaluateHand returns (total,soft?)
def evaluateHand(hand):
    ace = False
    total = 0
    for card in hand:
        if card==1 and total<=10 and not ace:
            ace = True
            total = total + 11
        else:
            total = total + card
        if total>21 and ace:
            ace = False
            total = total - 10
    return (total,ace)

def isPair(hand):
    length = len(hand)
    s = set(hand)
    if len(s)==1 and length==2:
        return True
    else:
        return False
    
def drawCard():
    card = deck.pop()
    global runningCount
    global trueCount
    if card<=6 and card>1:
        runningCount = runningCount + 1
    elif card==10 or card==1:
        runningCount = runningCount - 1
    trueCount = runningCount/(round(len(deck)/52)) #truecount = running count / number of decks left
    return card

#return 
def game():
    handActive = False
    stakesPlaced = 1
    payout = 0
    dealerFaceup = drawCard()
    dealerHand = [dealerFaceup]
    dealerFaceup = dealerFaceup - 2 #to accomodate strategy table lookup
    #print("Dealer has {}".format(dealerHand))
    playerHand = [drawCard()]
    dealerHand.append(drawCard())
    playerHand.append(drawCard())
    #Case where player/dealer has BJ
    if evaluateHand(dealerHand)[0] == 21 and ((dealerHand==[1,10]) or (dealerHand==[10,1])):
        if evaluateHand(playerHand)[0] == 21 and ((playerHand==[1,10]) or (playerHand==[10,1])):
            #print("Both player and dealer Blackjack, push")
            return (1,1)
        else:
            #print("Dealer Blackjack")
            return (1,0)
    elif evaluateHand(playerHand)[0] == 21 and ((playerHand==[1,10]) or (playerHand==[10,1])):
        #print("Player Blackjack")
        return (1,2.5)
    
    playerHands = [(playerHand)]
    handStakes = [2] #array of stakes for each hand held
    for hand in playerHands:
        while True: #loop for drawing cards
            a = evaluateHand(hand)
            #print("Player has {} Value: {}".format(hand, a))
            current = a[0]
            if current>21:
                #print("Player Bust")
                break
            softHand = a[1]
            play = 0; #1=Hit, 2=Stand, 3=Double
            #when to split pairs
            if isPair(hand):
                split = splitDict.get(hand[0])[dealerFaceup]
                if split==1:
                    #print("Player Splits")
                    stakesPlaced = stakesPlaced + 1
                    secondHand = [hand.pop()]
                    playerHands.append(secondHand)
                    handStakes.append(2)
                    current = hand[0]
                    if current == 1: #if split aces we need to make the current value 11
                        current = 11
                    #print("Player has {} Value: {}".format(hand, evaluateHand(hand)))
            
            if not softHand:
                play = hardDict.get(current)[dealerFaceup]
            elif softHand:
                play = softDict.get(current)[dealerFaceup]
                
            if play==1:
                #print("Player hits")
                hand.append(drawCard())
                continue
            if play==2:
                #print("Player stands")
                handActive = True
                break
            if play==3: #check if hand size is ==2 (for original hand) or ==1 (for splits) to see if doublable
                if (len(hand)==2 and len(playerHands)==1) or (len(hand)==1 and len(playerHands)>1):
                    #print("Player doubles")
                    stakesPlaced = stakesPlaced + 1
                    #handStake[0].append(drawCard())
                    #handStake[1]=2
                    handStakes[playerHands.index(hand)]=4
                    hand.append(drawCard())
                    val = evaluateHand(hand)
                    #print("Player has {} Value: {}".format(hand, val))
                    if val[0]>21:
                        #print("Player bust")
                        continue
                    else:
                        handActive = True
                    break
                else:
                    #print("Player hits")
                    hand.append(drawCard())
                    continue
    #dealer draw
    dealerBust = False
    if handActive:
        while True:
            b = evaluateHand(dealerHand)
            dealerValue = b[0]
            #print("Dealer has {} Value: {}".format(dealerHand, b))
            if dealerValue<17:
                #print("Dealer draws")
                dealerHand.append(drawCard())
                continue
            break
        if dealerValue>21:
            dealerBust = True
            #print("Dealer busts")

        #go through player hands to see if win
        for hand in playerHands:
            playerValue = evaluateHand(hand)[0]
            #print("Player hand {}".format(hand))
            if (playerValue>dealerValue or dealerBust) and playerValue<=21:
                #print("Wins against dealer.")
                payout = payout + handStakes[playerHands.index(hand)]                
            elif (playerValue==dealerValue) and playerValue<=21:
                if handStakes[playerHands.index(hand)]==2:
                    payout = payout + 1
                else: #tie on a doubled hand so return 2
                    payout = payout + 2
                #print("Push against dealer")
            else:
                #print("Loses against dealer.")
                continue
    #print("Stakes placed: {}. Payout: {}".format(stakesPlaced,payout))
    return (stakesPlaced,payout)

bankroll = 10000
wager = 10
flatbankroll = 10000
flatwager = 1
totalStakesPlaced = 0
totalStakesWon = 0

def exit_gracefully(signum, frame):
    global bankroll
    global wager
    global flatbankroll
    global flatwager
    global totalStakesPlaced
    global totalStakesWon
    
    print("totalStakesPlaced: {}, totalStakesWon: {}, bankroll: {}, flatbankroll: {}".format(totalStakesPlaced,totalStakesWon,bankroll,flatbankroll))
    sys.exit()


            
def main():
    print("Simulating, ctrl-c to stop...")
    signal.signal(signal.SIGINT, exit_gracefully)
    global bankroll
    global wager
    global flatbankroll
    global flatwager
    global totalStakesPlaced
    global totalStakesWon

    global deck
    shuffleDeck()

    bankroll = 100000
    wager = 10
    flatbankroll = 100000
    flatwager = 1
    totalStakesPlaced = 0
    totalStakesWon = 0
    while True:
        if (DECKSIZE-PENETRATION)*52 <= len(deck):
            if trueCount >= 1:
                wager = round((bankroll/1000) * trueCount)
            else:
                wager = round((bankroll/20000))
            
            #flatwager = round(flatbankroll/1000)
            flatwager = 1
            result = game()
            bankroll = bankroll - (wager*result[0]) + (wager*result[1])
            flatbankroll = flatbankroll - (flatwager*result[0]) + (flatwager*result[1])
            totalStakesPlaced = totalStakesPlaced + result[0]
            totalStakesWon = totalStakesWon + result[1]
            #print("totalStakesPlaced: {}, totalStakesWon: {}, bankroll: {}, flatbankroll: {}".format(totalStakesPlaced,totalStakesWon,bankroll,flatbankroll))
        else:
            #print("shuffled deck")
            shuffleDeck()


        
main()
