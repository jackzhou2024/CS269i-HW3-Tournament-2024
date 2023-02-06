import random
import numpy as np


# value is your initial value in this round, you should not bid a higher price than value
# because in that way you will get a negative utility (score) in this round

# We also provide the history for you and the competitor
# The length of myHistory and competitorHistory are equal
# During round n, you receive the history for the past (n-1) rounds, i.e.,
# The length of myHistory is n-1
# myHistory[i] is a 4-element list, including 
# (1) your initial value in round i
# (2) your bid price in round i
# (3) your allocation result (whether or not you get the item) in round i
# (4) your payment in round i

# We are using the Multiplicative weight update method
# Refer to https://en.wikipedia.org/wiki/Multiplicative_weight_update_method [Weighted majority algorithm]
# We define three experts to predict whether you should increase your bid price or not
# Surely, you can use the framework and define more smart experts to help you make the decision


def expert1(value, myHistory):
    # This expert is always optimistic and believe the bid price should always go up
    return True 

def expert2(value, myHistory):
    # This expert checks the history, if you loses more frequently, then he agrees to bid higher to win the item
    winCnt = 0
    for i in range(1, len(myHistory)):
        if myHistory[i][2] ==1:
            winCnt += 1
    if winCnt <= len(myHistory)/2:
        return True 
    else:
        return False

def expert3(value, myHistory):
    paymentGoUpCnt = 0
    for i in range(1, len(myHistory)):
        if myHistory[i][3] > myHistory[i-1][3]:
            paymentGoUpCnt += 1
    if paymentGoUpCnt > (len(myHistory)-1)/2:
        # In the past history, if payment goes up more frequently, then I believe it will go up
        return True 
    else:
        return False


yita = 0.01
stepSize = 0.01
expertWeights = [1.0,1.0,1.0]
expertDecisions = [True, False, True]
expertFunc = [expert1, expert2, expert3]
bidPrice = 0.5  # Initial Bid Price
lastDecision = True

def strategy(value, myHistory):
    global yita
    global stepSize
    global expertWeights
    global expertFunc
    global bidPrice
    global lastDecision
    # Update expertWeights
    goUp = False
    if(len(myHistory)>1):
        if myHistory[-1][2] == 1:
            # You win, the last Decision is right
            # Those experts who has different decision should be decreased
            for i in range(len(expertWeights)):
                # This expert makes wrong prediction, decrease its weight
                if not expertDecisions[i] == lastDecision:
                    expertWeights[i] = expertWeights[i] * (1.0-yita)
        else:
            # You lose, the last Decision is wrong
            # Those experts who has made the decision should be decreased
            for i in range(len(expertWeights)):
                # This expert makes wrong prediction, decrease its weight
                if expertDecisions[i] == lastDecision:
                    expertWeights[i] = expertWeights[i] * (1.0-yita)

    upWeights = 0
    totalWeights = 0
    for i in range(len(expertFunc)):
        expertDecisions[i] = (expertFunc[i])(value, myHistory)
        if expertDecisions[i] is True:
            upWeights += expertWeights[i]
        totalWeights += expertWeights[i]
            
    # initially, we decide to bid with half of our initial value
    if upWeights > totalWeights/2:
        # Most experts believe the bid should increase 
        # Add a StepSize amount based on your last bid
        lastDecision = True
        bidPrice += stepSize 
    else:
        # Most experts believe the bid should decrease 
        # Minus a StepSize amount based on your last bid
        lastDecision = False
        bidPrice -= stepSize 
    
    # print(bidPrice, " upWeights=", upWeights, " totalWeight=", totalWeights)
    # for i in range(len(expertWeights)):
    #     print(expertDecisions[i],"\t", expertWeights[i])
    # if bidPrice <0:
    #     exit(0)
    # Chunk
    if bidPrice > value:
        bidPrice = value
    if bidPrice < 0 :
        bidPrice = 0
    return bidPrice