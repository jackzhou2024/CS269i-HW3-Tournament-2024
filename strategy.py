import random
import numpy as np
# values contains two elements, values[0] is my initial value
# values[1] is the competitor's initial value



# we also provide the history for you and the competitor
# The length of myHistory and competitorHistory are equal
# During round n, you receive the history for the past (n-1) rounds, i.e.,
# The length of myHistory and competitorHistory are both n-1
# myHistory[i] is a 3-element list, including your initial value, your bid price, and your score at round i
# competitorHistory[i] is a 3-element list, including the competitor's initial value, bid price, and score at round i


def strategy(values, myHistory, competitorHistory):
    return values[0]*0.5