# Auction Auto-bidding Tournament

This tournament code is developed by Jinkun Geng. 


How this works:
Your task is to write a bidding strategy, following the template in exampleStrats; i.e., you will implement a function called strategy.

We will run your strategy in a 10,000-times-repeated auction against both baseline auto-bidders (as shown in exampleStrats), and classmates' auto-bidders. 
We are not specifying the auction format a-priori (see restrictions on auction format below), so your auto-bidder will have to learn how to bid based on feedback (value, bid, payment, and allocation) from previous rounds. 

There are three example auction modes in the code (e.g., SINGLE_ITEM_FIRST_PRICE, SINGLE_ITEM_SECOND_PRICE,
SINGLE_ITEM_ALL_PAY), but your auto-bidder should be robust to other auctions as well. The auction mode will determine how to calculate the scores for bots (please refer to calcScores function in game_run.py). During the gradescope competition, we might add more auction modes.


During each round, both your bot and the baseline will be given an initial value independently chosen from [0,1]. At the beginning of round i, your are also provided with the history in the past i-1 rounds (refer to the comments in exampleStrats/random_bid.py). The history might be helpful for you to derive the auction mode used in this 10000 rounds, so that you can better design your strategy. 

Regardless of the auction mode, you can assume that:
(1) Your auto-bidder's payment is never more than the bid; and
(2) The allocations and payments are monotone in the bid (but they may be randomized).


# Score Calculation
Your score is your total utility across 10000 rounds of the auction.
You can refer to calcScore function in game_run.py for the methods of score calculation.

For example, say $v_w$, $v_L$ are values of winner/loser, $b_W$, $b_L$ are bids. $u_W$, $u_L$ are the scores.
Then:


(1) SINGLE_ITEM_FIRST_PRICE, 
$u_W = v_W - b_W$,
$u_L = 0$

(2) SINGLE_ITEM_SECOND_PRICE, 
$u_W = v_W - b_L$,
$u_L = 0$

(3) SINGLE_ITEM_ALL_PAY, 
$u_W = v_W - b_W$,
$u_L = -b_L$




# Tasks
You are expected to write a python file named strategy.py (Please keep this name!). In this file you are expected to implement a function named strategy. After you finish you code, put the strategy.py to the folder exampleStrats, run the dilemma_run.py.

# Tips

To start from a clean Python enviornment, I suggest you use conda 

https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html

First, install conda

Second, create a clean python enviornment (say python 3.7) with conda

Third, install any deps and execute your script in that conda enviornment 

The major commands are as below. 

```
conda create --name [NAME]

conda activate [NAME]

conda install pip

pip install -r requirements.txt
```

After you have successfully create the environment, enter the code environment, and run game_run.py

```
cd code 

python game_run.py
```

Without writing any code, you should be able to run the competition for the existing strategies in the exampleStrats folder. Then, you write your own strategy.py and put the file into the folder, rerun dilemma_run.py to see whether you can beat these baselines.


# Note

All you need to do is to write a strategy.py file and add it to exampleStrats. No need to change any existing files.

When submitting to gradescope, you only submit strategy.py, no other files are needed.

For any questions, feel free to make a post on edstem.
