import random
import numpy as np
# values contains two elements, values[0] is my initial value
# values[1] is the competitor's initial value

# ctr1 and ctr2 are the click-through-rates of slots
# If auctionType == SINGLE_ITEM_FIRST_PRICE|SINGLE_ITEM_SECOND_PRICE,
# then only ctr1 is a valid numeric value, ctr2 is 0

# If auctionType == MULTI_ITEM_FIRST_PRICE|GSP|VCG
# then both ctr1 and ctr2 are valid numeric values, i.e.,
# there are two slots and ctr1>ctr2
def strategy(values, auctionType, ctr1, ctr2):
    return random.uniform(0,1)*values[0]