import os
import itertools
import importlib
import numpy as np
import random
import json

AUCTION_FOLDER = "auctionStrats"
STRATEGY_FOLDER = "exampleStrats"
CONTEXT_FILE = "context.json"


NUM_ROUNDS = 10000 # You can reduce the num round when you debug
TOTAL_BUDGET = 0.25 * NUM_ROUNDS

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

    for i in range(NUM_ROUNDS):
        jsonItem = {}
        jsonItem["v1"] = valueArr1[i]
        jsonItem["v2"] = valueArr2[i]
        jsonArr.append(jsonItem)
    
    json.dump(jsonArr, f, indent=4)


gen_context()       
# exit(0)




def calcScore(value, allocationResult):
    if allocationResult == 1:
        # winner, score is value
        return value
    else:
        # loser:  score 0
        return 0
    

def runRound(pair, auction):
    # print("modulea:",STRATEGY_FOLDER+"."+pair[0])
    moduleA = importlib.import_module(STRATEGY_FOLDER+"."+pair[0])
    moduleB = importlib.import_module(STRATEGY_FOLDER+"."+pair[1])
    moduleAuction = importlib.import_module(AUCTION_FOLDER +"."+auction)
    contextJson = json.load(open(CONTEXT_FILE, 'r'))
    
    LENGTH_OF_GAME =len(contextJson)
    totalScore1, totalScore2 = 0, 0

    history1 = []
    history2 = []
    budget1 = TOTAL_BUDGET
    budget2 = TOTAL_BUDGET
    
    for turn in range(LENGTH_OF_GAME):
        contextItem = contextJson[turn]
        v1 = contextItem["v1"]
        v2 = contextItem["v2"]
        bid1 = moduleA.strategy(v1, budget1, LENGTH_OF_GAME - turn, history1)
        bid2 = moduleB.strategy(v2, budget2, LENGTH_OF_GAME - turn, history2)
        bid1 = min(bid1, budget1)
        bid2 = min(bid2, budget2)
        if(bid1 < 0):
            raise Exception("bid1 price is not valid (< 0) ", bid1)
        if(bid2 < 0):
            raise Exception("bid2 price is not valid (< 0)  ", bid2)

        # print("bid1=", bid1, " bid2=",bid2)
        auctionResult = moduleAuction.auctionStrategy(bid1, bid2)

        score1 = calcScore(v1, auctionResult[0][0])
        score2 = calcScore(v2, auctionResult[1][0])
        budget1 -= auctionResult[0][1]
        budget2 -= auctionResult[1][1]
        totalScore1 += score1
        totalScore2 += score2
        history1.append([v1, bid1, auctionResult[0][0], auctionResult[0][1] ])
        history2.append([v2, bid2, auctionResult[1][0], auctionResult[1][1] ])
    return totalScore1, totalScore2


def pad(stri, leng):
    result = stri
    for i in range(len(stri),leng):
        result = result+" "
    return result
    
def runFullPairingTournament(auctionFolder, stratsFolder):
    print("Starting tournament, reading files from "+stratsFolder)
    scoreKeeper = {}
    STRATEGY_LIST = []
    for file in os.listdir(stratsFolder):
        if file.endswith(".py"):
            STRATEGY_LIST.append(file[:-3])

    print("Reading Auction modes from "+auctionFolder)
    AUCTION_LIST = []
    for file in os.listdir(auctionFolder):
        if file.endswith(".py"):
            AUCTION_LIST.append(file[:-3])
            
    for strategy in STRATEGY_LIST:
        scoreKeeper[strategy] = 0

    for auction in AUCTION_LIST:
        for pair in itertools.combinations(STRATEGY_LIST, r=2):
            score1, score2 = runRound(pair, auction)
            scoreKeeper[pair[0]] += score1
            scoreKeeper[pair[1]] += score2
    
        
    scoresNumpy = np.zeros(len(scoreKeeper))
    for i in range(len(STRATEGY_LIST)):
        scoresNumpy[i] = scoreKeeper[STRATEGY_LIST[i]]
    rankings = np.argsort(scoresNumpy)

    print("\n\nTOTAL SCORES\n")
    for rank in range(len(STRATEGY_LIST)):
        i = rankings[-1-rank]
        score = scoresNumpy[i]
        scorePer = score/(len(STRATEGY_LIST)-1)
        print("#"+str(rank+1)+": "+pad(STRATEGY_LIST[i]+":",16)+' %.3f'%score+'  (%.3f'%scorePer+" average)\n")
    print("Done with everything!")
    
    
runFullPairingTournament(AUCTION_FOLDER, STRATEGY_FOLDER)
