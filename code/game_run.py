import os
import itertools
import importlib
import numpy as np
import random
import json

RESULTS_FILE = "results.txt"
STRATEGY_FOLDER = "exampleStrats"
CONTEXT_FILE = "context.json"

# ENum
SINGLE_ITEM_FIRST_PRICE = 1
SINGLE_ITEM_SECOND_PRICE = 2
MULTI_ITEM_FIRST_PRICE = 3
GSP = 4
VCG = 5




def gen_context():
    f = open(CONTEXT_FILE, 'w')
    jsonArr = []
    valueArr1 = []
    valueArr2 = []
    actionTypeArr = []
    ctrArr1 = []
    for i in range(200):
        v1 = random.uniform(0,1)
        valueArr1.append(v1)
        v2 = random.uniform(0,1)
        valueArr2.append(v2)  
        atp = random.randint(1,5)
        actionTypeArr.append(atp)
        ctr1 = random.uniform(0,0.5)
        ctrArr1.append(ctr1)
    valueArr1.sort()
    valueArr2.sort()
    ctrArr1.sort()

    for i in range(200):
        jsonItem = {}
        jsonItem["v1"] = valueArr1[i]
        jsonItem["v2"] = valueArr2[i]
        jsonItem["auctionType"] = actionTypeArr[i]
        jsonItem["ctr1"] = ctrArr1[i]
        if(actionTypeArr[i]==SINGLE_ITEM_FIRST_PRICE or actionTypeArr[i]==SINGLE_ITEM_SECOND_PRICE):
            jsonItem["ctr2"] = 0
        else:
            ctr2 = ctr1* random.uniform(0,1)
            jsonItem["ctr2"] = ctr2
        jsonArr.append(jsonItem)
    
    json.dump(jsonArr, f, indent=4)


# gen_context()       
# exit(0)




def calcScores(bid1, bid2, v1, v2, atp, ctr1, ctr2):
    score1, score2 = 0, 0
    # if bid1==bid2, it is a tie, just give each one 0 score
    if atp==SINGLE_ITEM_FIRST_PRICE:
        if bid1 > bid2:
            score1 = (v1 - bid1)* ctr1 
            score2 = 0
        elif bid1 < bid2:
            score1 = 0
            score2 = (v2-bid2)* ctr1 
        return score1, score2 
    elif atp == SINGLE_ITEM_SECOND_PRICE:
        if bid1 > bid2:
            score1 = (v1 - bid2)* ctr1 
            score2 = 0
        elif bid1 < bid2:
            score1 = 0
            score2 = (v2-bid1)* ctr1 
        return score1, score2 
    elif atp == MULTI_ITEM_FIRST_PRICE:
        if bid1 > bid2:
            # player 1 wins the first slot, player 2 gets the second slot
            score1 = (v1 - bid1)* ctr1 
            score2 = (v2 - bid2) * ctr2
        elif bid1 < bid2:
            # player 1 gets the first slot, player 2 wins the first slot
            score1 = (v1 - bid1)* ctr2 
            score2 = (v2 - bid2) * ctr1
        return score1, score2 
    elif atp == GSP:
        if bid1 > bid2:
            # player 1 wins the first slot, but pays bid2
            # player 2 gets the second slot, and pays 0 since we do not have the third player, i.e., bid3=0
            score1 = (v1 - bid2)* ctr1 
            score2 = (v2 - 0) * ctr2
        elif bid1 < bid2:
            # player 2 wins the first slot, but pays bid1
            # player 1 gets the second slot, and pays 0 since we do not have the third player, i.e., bid3=0
            score1 = (v1 - 0)* ctr2 
            score2 = (v2 - bid1) * ctr1
        return score1, score2
    elif atp == VCG:
        if bid1 > bid2:
            # player 1 wins the first slot, it pays p1; player 2 pays p2=0
            p1 = bid2* (ctr1 - ctr2)
            p2 = 0 
            score1 = (v1-p1)*ctr1 
            score2 = (v2-p2)*ctr2
        elif bid1 < bid2: 
            # player 2 wins the first slot, it pays p2; player 1 pays p1=0
            p1 = 0
            p2 = bid1 * (ctr1-ctr2) 
            score1 = (v1-p1)*ctr2 
            score2 = (v2-p2)*ctr1
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
    for turn in range(LENGTH_OF_GAME):
        contextItem = contextJson[turn]
        v1 = contextItem["v1"]
        v2 = contextItem["v2"]
        atp = contextItem["auctionType"]
        # print(contextItem)
        ctr1 = contextItem["ctr1"]
        ctr2 = contextItem["ctr2"]
        
        bid1 = moduleA.strategy([v1,v2], atp, ctr1, ctr2)
        bid2 = moduleB.strategy([v2,v1], atp, ctr1, ctr2)
        score1, score2 = calcScores(bid1, bid2, v1, v2, atp, ctr1, ctr2)
        totalScore1 += score1
        totalScore2 += score2
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
