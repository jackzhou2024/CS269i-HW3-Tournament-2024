# Auction Auto-bidding Tournament

This tournament code is developed by Jinkun Geng. 


How this works:
Your task is to write a bidding strategy, following the template in exampleStrats; i.e., you will implement a function called strategy.

We will run your strategy in a 10,000-round-repeated auction against both baseline auto-bidders (as shown in exampleStrats), and classmates' auto-bidders. 
We are not specifying the auction format a-priori (see restrictions on auction format below), so your auto-bidder will have to learn how to bid based on feedback (value, bid, payment, and allocation) from previous rounds. 

There are three example auction modes in the code (e.g., singleItemFirstPrice, singleItemSecondPrice,
singleItemAllPay), but your auto-bidder should be robust to other auctions as well. The auction mode will determine how to calculate the scores for bots (please refer to calcScores function in game_run.py). During the gradescope competition, we might add more auction modes.


During each round, both your bot and the baseline will be given an initial value independently chosen from [0,1]. At the beginning of round i, your are also provided with the history in the past i-1 rounds (refer to the comments in exampleStrats/random_bid.py). The history might be helpful for you to derive the auction mode used in this 10000 rounds, so that you can better design your strategy. 

Regardless of the auction mode, you can assume that your auto-bidder's payment is never more than the bid.


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


You can check the auctionStrats folder to see how we implement these three modes to decide the allocation result (i.e., who is the winner) and the payment.

In our gradescope test, we may include new auction modes.


# Tasks
You are expected to write a python file named strategy.py (Please keep this name!). In this file you are expected to implement a function named strategy. After you finish you code, put the strategy.py to the folder exampleStrats, run the game_run.py.


We have made three examples in exampleStrats, the simpler one is random_bid_shade.py, which simply bids with a price by multiplying a factor with the value; the other is a more complicated Multi-Armed-Bandit (MAB) algorithm, we are using MABWiser lib to implement it, and you can read more info at  https://fidelity.github.io/mabwiser/about.html and implement your MAB algorithm following the example, and we have provided both contextual MAB and context-free MAB for your reference.

While designing your strategy function, you will receive the history of your past bids, which is represented as myHistory list (refer to the comments in random_bid_shade.py/context-free-multi-armed-bandit.py/contextual-multi-armed-bandit.py). You can choose to use/not use the history information to help you design better algorithms.


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
