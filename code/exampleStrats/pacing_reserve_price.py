import random
import numpy as np


# value is your initial value in this round.
# budget is your remaining budget, you never bid a higher price than remaining budget.
# remainingRound is the number of remaining rounds (including the current one).
# We also provide the history for you
# During round n, you receive the history for the past (n-1) rounds, i.e.,
# The length of myHistory is n-1
# myHistory[i] is a 4-element list, including 
# (0) your initial value in round i
# (1) your bid price in round i
# (2) your allocation result (whether or not you get the item) in round i
# (3) your payment in round i

AVG_SPEND = 0.25 # you expect to spend 0.25 per round
EPS = 0.05 # learning rate
r = 0 # reserve price

def update_pacing_factor(payment):
    global r
    r += EPS * (payment - AVG_SPEND)
    r = max(0, r)
    r = min(1, r)

def strategy(value, budget, remainingRound, myHistory):
    global r
    if (len(myHistory) > 0):
        update_pacing_factor(myHistory[-1][3])
    else:
        r = 0
    if (value > r):
        return min(value, budget)
    else:
        return 0