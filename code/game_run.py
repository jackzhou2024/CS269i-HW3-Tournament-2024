import os
import itertools
import importlib
import numpy as np
import random
import json

RESULTS_FILE = "results.txt"
STRATEGY_FOLDER = "exampleStrats"
CONTEXT_FILE = "context.json"

# Enum
SINGLE_ITEM_FIRST_PRICE = 1
SINGLE_ITEM_SECOND_PRICE = 2
SINGLE_ITEM_ALL_PAY = 3

NUM_ROUNDS = 10000

def gen_context():
    f = open(CONTEXT_FILE, 'w')
    jsonArr = []
    valueArr1 = []
    valueArr2 = []
    for i in range(NUM_ROUNDS):
        v1 = random.uniform(0,1)
        valueArr1.append(v1)
        v2 = random.uniform(0,1)
        valueArr2.append(v2)  
    valueArr1.sort()
    valueArr2.sort()

    for i in range(NUM_ROUNDS):
        jsonItem = {}
        jsonItem["v1"] = valueArr1[i]
        jsonItem["v2"] = valueArr2[i]
        jsonArr.append(jsonItem)
    
    json.dump(jsonArr, f, indent=4)


# gen_context()       
# exit(0)




def calcScores(bid1, bid2, v1, v2, atp):
    score1, score2 = 0, 0
    # if bid1==bid2, it is a tie, just give each one 0 score
    if atp==SINGLE_ITEM_FIRST_PRICE:
        if bid1 > bid2:
            score1 = (v1 - bid1) 
            score2 = 0-bid1
        elif bid1 < bid2:
            score1 = 0-bid2
            score2 = (v2-bid2)
        return score1, score2 
    elif atp == SINGLE_ITEM_SECOND_PRICE:
        if bid1 > bid2:
            score1 = v1 - bid2
            score2 = 0 - bid2
        elif bid1 < bid2:
            score1 = 0 - bid1
            score2 = v2-bid1
        return score1, score2 
    elif atp == SINGLE_ITEM_ALL_PAY:
        if bid1 > bid2:
            score1 = v1 - bid1
            score2 = v2-bid2 - bid1
        elif bid1 < bid2:
            score1 = v1 - bid1 - bid2  
            score2 = v2 -bid2
        return score1, score2 
  
    else:
        raise Exception("Unreognized auction type")

def runRound(pair):
    # print("modulea:",STRATEGY_FOLDER+"."+pair[0])
    moduleA = importlib.import_module(STRATEGY_FOLDER+"."+pair[0])
    moduleB = importlib.import_module(STRATEGY_FOLDER+"."+pair[1])
    contextJson = json.load(open(CONTEXT_FILE, 'r'))
    
    LENGTH_OF_GAME =len(contextJson)
    totalScore1, totalScore2 = 0, 0
    # In the gradescope test, we will not simply run following the order
    # SINGLE_ITEM_FIRST_PRICE->SINGLE_ITEM_SECOND_PRICE->SINGLE_ITEM_ALL_PAY
    # Therefore, you'd better not hard-code three sub-strategy to cater to 
    # the order  SINGLE_ITEM_FIRST_PRICE->SINGLE_ITEM_SECOND_PRICE->SINGLE_ITEM_ALL_PAY 
    for auctionType in [SINGLE_ITEM_FIRST_PRICE, SINGLE_ITEM_SECOND_PRICE, SINGLE_ITEM_ALL_PAY]:
        history1 = []
        history2 = []
        for turn in range(LENGTH_OF_GAME):
            contextItem = contextJson[turn]
            v1 = contextItem["v1"]
            v2 = contextItem["v2"]
            bid1 = moduleA.strategy([v1,v2], history1, history2)
            bid2 = moduleB.strategy([v2,v1], history2, history1)
            score1, score2 = calcScores(bid1, bid2, v1, v2, auctionType)
            totalScore1 += score1
            totalScore2 += score2
            history1.append([v1, bid1, score1])
            history2.append([v2, bid2, score2])
    return totalScore1, totalScore2


def pad(stri, leng):
    result = stri
    for i in range(len(stri),leng):
        result = result+" "
    return result
    
def runFullPairingTournament(inFolder, outFile):
    print("Starting tournament, reading files from "+inFolder)
    scoreKeeper = {}
    STRATEGY_LIST = []
    for file in os.listdir(inFolder):
        if file.endswith(".py"):
            STRATEGY_LIST.append(file[:-3])
            
            
    for strategy in STRATEGY_LIST:
        scoreKeeper[strategy] = 0
    
    f = open(outFile,"w+")
    for pair in itertools.combinations(STRATEGY_LIST, r=2):
        score1, score2 = runRound(pair)
        scoreKeeper[pair[0]] += score1
        scoreKeeper[pair[1]] += score2
    
        
    scoresNumpy = np.zeros(len(scoreKeeper))
    for i in range(len(STRATEGY_LIST)):
        scoresNumpy[i] = scoreKeeper[STRATEGY_LIST[i]]
    rankings = np.argsort(scoresNumpy)

    f.write("\n\nTOTAL SCORES\n")
    print("\n\nTOTAL SCORES\n")
    for rank in range(len(STRATEGY_LIST)):
        i = rankings[-1-rank]
        score = scoresNumpy[i]
        scorePer = score/(len(STRATEGY_LIST)-1)
        f.write("#"+str(rank+1)+": "+pad(STRATEGY_LIST[i]+":",16)+' %.3f'%score+'  (%.3f'%scorePer+" average)\n")
        print("#"+str(rank+1)+": "+pad(STRATEGY_LIST[i]+":",16)+' %.3f'%score+'  (%.3f'%scorePer+" average)\n")
    f.flush()
    f.close()
    print("Done with everything! Results file written to "+RESULTS_FILE)
    
    
runFullPairingTournament(STRATEGY_FOLDER, RESULTS_FILE)
