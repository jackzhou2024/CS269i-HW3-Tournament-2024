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


def strategy(value, myHistory):
    return random.uniform(0,1)*value